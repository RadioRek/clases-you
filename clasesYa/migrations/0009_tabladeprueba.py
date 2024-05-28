# Generated by Django 4.2.5 on 2023-11-27 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clasesYa', '0008_chatroom_chatmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='tablaDePrueba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, default='', max_length=255)),
                ('apellido', models.CharField(blank=True, default='', max_length=255)),
                ('rut', models.IntegerField(blank=True, default=12345678)),
                ('dv', models.CharField(blank=True, default='k', max_length=1)),
                ('telefono', models.IntegerField(blank=True, default=12345678)),
            ],
        ),
    ]