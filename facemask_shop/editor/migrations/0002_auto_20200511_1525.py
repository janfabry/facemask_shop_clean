# Generated by Django 2.2.12 on 2020-05-11 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facemask',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='facemask/thumbnail/'),
        ),
    ]
