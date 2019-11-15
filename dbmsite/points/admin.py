from django.contrib import admin

from.models import Users, PointTransactions, RedeemTransactions

# Register your models here.

# Registering multiple models
myModels = [Users, PointTransactions, RedeemTransactions]
admin.site.register(myModels)

