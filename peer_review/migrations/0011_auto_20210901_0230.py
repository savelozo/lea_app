# Generated by Django 3.1.7 on 2021-09-01 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0010_alumne_last_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtAlumneRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.IntegerField(blank=True, null=True)),
                ('alumne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peer_review.alumne')),
                ('arte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peer_review.arte')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peer_review.curso')),
            ],
        ),
        migrations.RenameField(
            model_name='ensayoalumnerelation',
            old_name='corregido_1',
            new_name='corrector_id_1',
        ),
        migrations.RenameField(
            model_name='ensayoalumnerelation',
            old_name='corregido_2',
            new_name='corrector_id_2',
        ),
        migrations.RenameField(
            model_name='ensayoalumnerelation',
            old_name='corrector',
            new_name='corregido',
        ),
        migrations.AddField(
            model_name='ensayoalumnerelation',
            name='curso',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='peer_review.curso'),
        ),
        migrations.AddField(
            model_name='ensayoalumnerelation',
            name='url',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.DeleteModel(
            name='PeerReviewRelation',
        ),
    ]