from django.contrib import admin

from.models import PointTransactions, GiftTransaction, Users

# Register your models here.

# Registering multiple models
myModels = [Users, PointTransactions, GiftTransaction]
admin.site.register(myModels)

