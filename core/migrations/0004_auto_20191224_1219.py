# Generated by Django 3.0.1 on 2019-12-24 12:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20191224_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repo',
            name='creation_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]