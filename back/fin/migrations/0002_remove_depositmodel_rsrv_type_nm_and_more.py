# Generated by Django 4.2.16 on 2024-11-21 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depositmodel',
            name='rsrv_type_nm',
        ),
        migrations.AlterField(
            model_name='savingmodel',
            name='join_way',
            field=models.TextField(null=True),
        ),
    ]