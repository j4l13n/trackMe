# Generated by Django 3.1 on 2020-08-26 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_auto_20200818_0701'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracking',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
