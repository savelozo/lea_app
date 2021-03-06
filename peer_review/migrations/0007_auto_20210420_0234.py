# Generated by Django 3.1.7 on 2021-04-20 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0006_auto_20210419_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='artes',
            field=models.ManyToManyField(to='peer_review.Arte'),
        ),
        migrations.CreateModel(
            name='PeerReviewRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corregide_id', models.IntegerField()),
                ('corrector_id', models.IntegerField()),
                ('arte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peer_review.arte')),
            ],
        ),
    ]
