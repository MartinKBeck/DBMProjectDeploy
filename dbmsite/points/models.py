from django.db import models

class Users(models.Model):
	user_id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=40) 
	points_left = models.IntegerField()
	points_received = models.IntegerField()

class PointTransactions(models.Model):
	transaction_id = models.AutoField(primary_key=True)
	sender = models.ForeignKey(Users, related_name='sendingUser', on_delete=models.CASCADE)
	recipient = models.ForeignKey(Users, related_name='receivingUser', on_delete=models.CASCADE)
	sent_amount = models.IntegerField()
	transaction_date = models.DateTimeField(auto_now_add=True)
	message = models.CharField(max_length = 40)

class RedeemTransactions(models.Model):
	transaction_id = models.AutoField(primary_key=True)
	user = models.ForeignKey(Users, related_name='redeemUser',on_delete=models.CASCADE)
	points_redeemed = models.IntegerField()
	transaction_date = models.DateTimeField(auto_now_add=True, null=True)
	def __str__(self):
		return self.redeemtransactions_text

class Admin(models.Model):
	adminId = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=40)
	def __str__(self):
		return self.admin_text