from django.contrib import admin

from.models import TestTransactions, GiftTransaction, Users

# Register your models here.

# Registering multiple models
myModels = [Users, TestTransactions, GiftTransaction]
admin.site.register(myModels)

