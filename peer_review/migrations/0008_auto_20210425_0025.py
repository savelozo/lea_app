# Generated by Django 3.1.7 on 2021-04-25 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0007_auto_20210420_0234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumne',
            name='corrector',
        ),
        migrations.CreateModel(
            name='EnsayoAlumneRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corregido_1', models.IntegerField(blank=True)),
                ('corregido_2', models.IntegerField(blank=True)),
                ('arte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peer_review.arte')),
                ('corrector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peer_review.alumne')),
            ],
        ),
    ]
