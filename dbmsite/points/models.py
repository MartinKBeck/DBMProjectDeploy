from django.db import models

class Users(models.Model):
	userId = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=30) 
	# Deal with hashing later
	received = models.IntegerField()
	givenBucket = models.IntegerField()
	def __str__(self):
		return self.users_text

# class PointTransactions(models.Model):
# 	transactionId = models.AutoField(primary_key=True)
# 	userGiver = models.ForeignKey(Users, on_delete=models.CASCADE)
# 	userReceiver = models.ForeignKey(Users, on_delete=models.CASCADE)
# 	pointAmount = models.IntegerField()

class Test(models.Model):
	testid = models.AutoField(primary_key=True)

class TestTransactions(models.Model):
	testerId = models.AutoField(primary_key=True)
	usertest = models.CharField(max_length=30, unique=True)
	def __str__(self):
		return self.testtransactions_text

class Admin(models.Model):
	adminId = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=30)
	# Deal with hashing later
	def __str__(self):
		return self.admin_text

class GiftTransaction(models.Model):
	giftTransactionId = models.AutoField(primary_key=True)
	userId = models.ForeignKey(Users, on_delete=models.CASCADE)
	amountDeducting = models.IntegerField()
	def __str__(self):
		return self.gifttransactions_text