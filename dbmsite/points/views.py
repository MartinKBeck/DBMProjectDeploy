from django.views.generic import TemplateView
from django.shortcuts import render
from points.models import Users, PointTransactions, RedeemTransactions
import hashlib

# Create your views here.
class Index(TemplateView):
	template_name = 'points/index.html'
	
class Register(TemplateView):
	template_name = 'registration/register.html'

class Success(TemplateView):
	template_name = 'points/success.html'

def  user_login(request):
	if request.method == 'POST':
		# Retreiving user inputs
		username = request.POST.get('username')
		password = request.POST.get('password')

		# Hashing function to test against DB
		password_hash = hashlib.md5(password.encode()).hexdigest()

		# Checking against database
		if (Users.objects.filter(username=username, password=password_hash).exists()):
			return render(request, 'points/hub.html')
		else:
			print('Incorrect Credentials')
			return render(request, 'registration/login.html')
	else:
		return render(request, 'registration/login.html')

class UserHub(TemplateView):
	template_name = 'points/hub.html'

# Send points page
def send_points(request):
	if request.method == 'POST':

		# Creation of variables to be used in later sections
		sender = request.POST.get('sender')
		receiver = request.POST.get('receiver')
		amount = int(request.POST.get('amount'))
		message = request.POST.get('message')

		# User checking for sender existence
		if (Users.objects.filter(username=sender).exists()):
			# User checking for receiver existence
			if (Users.objects.filter(username=receiver).exists()):
				# Check that user has enough points
				senderIdentity = Users.objects.get(user_id=senderId)

				if(senderIdentity.points_left<amount):
					print('Insufficient Funds')
					return render(request, 'points/sendpoints.html')
				else:
					# Finding user_id of each person
					senderId = Users.objects.filter(username=sender).values_list('user_id')[0][0]
					receiverId = Users.objects.filter(username=receiver).values_list('user_id')[0][0]		

					# Pulling the Users object of each party
					receiverIdentity = Users.objects.get(user_id=receiverId)

					# Creation of new row in point transactions table
					newTransaction = PointTransactions.objects.create(sender_id = senderIdentity, recipient_id = receiverIdentity, sent_amount = amount, message = message)

					# Generating point amounts and updating DB
					senderIdentity.points_left = senderIdentity.points_left - amount
					senderIdentity.save()

					# Generating point amounts and updating DB
					receiverIdentity.points_received = receiverIdentity.points_received + amount
					receiverIdentity.save()

					# Return user back to their hub after sending points
					return render(request, 'points/hub.html')
	else:
		return render(request, 'points/sendpoints.html')

# Page for redeeming points gained
def redeem_points(request):
	if request.method == 'POST':

		# Setting variables to prep for usage
		redeemer = request.POST.get('redeemer')
		giftcardnum = int(request.POST.get('giftcardnum'))
		pointsredeemed = giftcardnum * 10000

		# Check that person exists in database currently
		if (Users.objects.filter(username=sender).exists()):

			# Getting userid and setting userclass to a variable
			redeemerId = Users.objects.filter(username=redeemer).values_list('user_id')[0][0]
			redeemerAccount = Users.objects.get(user_id=redeemerId)

			# Validating that redeemer has amount of points
			if redeemerAccount.points_left < pointsredeemed:
				print('Insufficient Funds')
				return render(request, 'points/redeempoints.html')
			else:
				# Points removal and creation of redeemtransactions 
				newRedeemTransaction = RedeemTransactions.objects.create(user_id=redeemerAccount, points_redeemed = pointsredeemed)

				redeemerAccount.points_left = redeemerAccount.points_left - pointsredeemed
				redeemerAccount.save()

			return render(request, 'points/hub.html')
	else:
		return render(request, 'points/redeempoints.html')
