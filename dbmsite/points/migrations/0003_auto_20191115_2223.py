# Generated by Django 2.1.13 on 2019-11-16 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0002_auto_20191115_1845'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pointtransactions',
            old_name='recipient_id',
            new_name='recipient',
        ),
        migrations.RenameField(
            model_name='pointtransactions',
            old_name='sender_id',
            new_name='sender',
        ),
        migrations.RenameField(
            model_name='redeemtransactions',
            old_name='user_id',
            new_name='user',
        ),
    ]