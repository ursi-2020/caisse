# Generated by Django 2.2.5 on 2019-10-05 16:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0003_auto_20190923_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='name',
        ),
        migrations.RemoveField(
            model_name='article',
            name='price',
        ),
        migrations.AddField(
            model_name='article',
            name='codeProduit',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='prix',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('prix', models.IntegerField()),
                ('client', models.CharField(max_length=20)),
                ('pointsFidelite', models.IntegerField()),
                ('modePaiement', models.CharField(max_length=10)),
                ('articles', models.ManyToManyField(to='djangoapp.Article')),
            ],
        ),
    ]
