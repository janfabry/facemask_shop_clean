# Generated by Django 2.1.1 on 2018-09-12 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_update_email_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatusChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.CharField(blank=True, max_length=100, verbose_name='Old Status')),
                ('new_status', models.CharField(blank=True, max_length=100, verbose_name='New Status')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_changes', to='order.Order', verbose_name='Order Status Changes')),
            ],
            options={
                'verbose_name': 'Order Status Change',
                'verbose_name_plural': 'Order Status Changes',
                'ordering': ['-date_created'],
                'abstract': False,
            },
        ),
    ]
