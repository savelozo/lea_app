# Generated by Django 3.1.7 on 2021-04-25 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0009_auto_20210425_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumne',
            name='last_group',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
