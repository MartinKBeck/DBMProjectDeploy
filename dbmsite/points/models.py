from django.db import models

class Users(models.Model):
	userId = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=30) 
	# Deal with hashing later
	received = models.IntegerField()
	givenBucket = models.IntegerField()

class PointTransactions(models.Model):
	transactionId = models.AutoField(primary_key=True)
	transactionDate = models.DateTimeField(auto_now_add=True)
	userGiver = models.ForeignKey(Users, related_name='givingUser', on_delete=models.CASCADE)
	userReceiver = models.ForeignKey(Users, related_name='receivingUser', on_delete=models.CASCADE)
	pointAmount = models.IntegerField()
	message = models.CharField(max_length = 40)

class Admin(models.Model):
	adminId = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=30)
	# Deal with hashing later
	def __str__(self):
		return self.admin_text

class GiftTransaction(models.Model):
	giftTransactionId = models.AutoField(primary_key=True)
	transactionDate = models.DateTimeField(auto_now_add=True, null=True)
	userId = models.ForeignKey(Users, on_delete=models.CASCADE)
	amountDeducting = models.IntegerField()
	def __str__(self):
		return self.gifttransactions_text