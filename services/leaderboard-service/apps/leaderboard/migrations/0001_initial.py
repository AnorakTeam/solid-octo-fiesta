from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='LeaderboardEntry',
            fields=[
                ('user_id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('nickname', models.CharField(db_index=True, max_length=40)),
                ('profile_icon', models.CharField(blank=True, max_length=500, null=True)),
                ('score', models.PositiveBigIntegerField(db_index=True, default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-score', 'nickname'],
            },
        ),
    ]
