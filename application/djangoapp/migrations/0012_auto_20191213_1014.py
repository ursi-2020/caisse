# Generated by Django 2.2.7 on 2019-12-13 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0011_auto_20191129_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleslist',
            name='promo',
        ),
        migrations.AddField(
            model_name='articleslist',
            name='promoPanier',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articleslist',
            name='promoProduit',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articleslist',
            name='promoProduitClient',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
