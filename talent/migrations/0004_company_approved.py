# Generated by Django 4.2.3 on 2024-11-08 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0003_alter_companyjobs_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
