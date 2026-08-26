from .models import PlayerUpgrade

# NOTE: No se ha agregado aún a la BD, porque se implementaron las upgrades sólo
# como concepto, tocaría primero nivelarlas y verificar que no estén... rotas? 
UPGRADE_CATALOG = {
    PlayerUpgrade.Type.CLICKER: {
        'name': 'Clicker',
        'description': 'Suma 1 punto cada 10 segundos.',
        'cost': 15,
        'clicks_per_second': 0.1,
    },
    PlayerUpgrade.Type.STATIC: {
        'name': 'Static',
        'description': 'Suma 1 punto por segundo.',
        'cost': 120,
        'clicks_per_second': 1,
    },
    PlayerUpgrade.Type.SPAMMER: {
        'name': 'Spammer',
        'description': 'Suma 5 puntos por segundo.',
        'cost': 300,
        'clicks_per_second': 5,
    },
}


def serialize_upgrades(user):
    quantities = dict(
        PlayerUpgrade.objects.filter(user=user).values_list('upgrade_type', 'quantity')
    )
    upgrades = [
        {
            'key': key,
            **definition,
            'quantity': quantities.get(key, 0),
        }
        for key, definition in UPGRADE_CATALOG.items()
    ]
    total_clicks_per_second = sum(
        upgrade['clicks_per_second'] * upgrade['quantity']
        for upgrade in upgrades
    )

    return {
        'upgrades': upgrades,
        'total_clicks_per_second': total_clicks_per_second,
    }
