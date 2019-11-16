# Generated by Django 2.1.13 on 2019-11-16 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0003_auto_20191115_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('adminId', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='users',
            name='admin',
        ),
    ]