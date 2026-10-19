from django.db import migrations

from tracker.seed_data import seed


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
