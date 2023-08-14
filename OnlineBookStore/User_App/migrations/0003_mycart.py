# Generated by Django 4.1.6 on 2023-03-03 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_App', '0001_initial'),
        ('User_App', '0002_remove_userinfo_id_alter_userinfo_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_App.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User_App.userinfo')),
            ],
        ),
    ]
