# Generated by Django 2.2 on 2022-01-11 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0009_auto_20220111_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='rilis',
            field=models.DateField(blank=True, null=True),
        ),
    ]