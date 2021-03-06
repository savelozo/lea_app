# Generated by Django 3.1.7 on 2021-03-27 01:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fecha_entrega', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_canvas', models.IntegerField()),
                ('semestre', models.IntegerField()),
                ('año', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ensayo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrega', models.DateTimeField()),
                ('arte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peer_review.arte')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peer_review.curso')),
            ],
        ),
    ]
