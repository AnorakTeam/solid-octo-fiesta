from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='PlayerUpgrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(db_index=True)),
                ('upgrade_type', models.CharField(choices=[('clicker', 'Clicker'), ('static', 'Static'), ('spammer', 'Spammer')], max_length=20)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'constraints': [
                    models.UniqueConstraint(fields=('user_id', 'upgrade_type'), name='unique_shop_player_upgrade')
                ],
            },
        ),
    ]
