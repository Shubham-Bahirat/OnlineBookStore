# Generated by Django 4.1.6 on 2023-03-17 04:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User_App', '0003_mycart'),
    ]

    operations = [
        migrations.CreateModel(
            name='orderInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(default=datetime.datetime.now)),
                ('amount', models.FloatField(default=1200)),
                ('details', models.CharField(max_length=600)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User_App.userinfo')),
            ],
            options={
                'db_table': 'orderInfo',
            },
        ),
    ]
