from django.views.generic import TemplateView
from django.shortcuts import render
from points.models import Users, PointTransactions, RedeemTransactions, Admin,
import hashlib

# Create your views here.
class Index(TemplateView):
	template_name = 'points/index.html'

def  user_login(request):
	if request.method == 'POST':
		# Retreiving user inputs
		username = request.POST.get('username')
		password = request.POST.get('password')

		# Hashing function to test against DB
		password_hash = hashlib.md5(password.encode()).hexdigest()

		# Checking against database
		if (Users.objects.filter(username=username, password=password_hash).exists()):
			return render(request, 'points/hub.html', {'admin':0})
		if (Admin.objects.filter(username=username, password=password_hash).exists()):
			return render(request, 'points/hub.html', {'admin':1})
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
				senderId = Users.objects.filter(username=sender).values_list('user_id')[0][0]
				senderIdentity = Users.objects.get(user_id=senderId)

				if(senderIdentity.points_left<amount and senderIdentity.points_left>0):
					print('Insufficient Funds')
					return render(request, 'points/sendpoints.html')
				else:
					# Finding user_id of each person
					receiverId = Users.objects.filter(username=receiver).values_list('user_id')[0][0]		

					# Pulling the Users object of each party
					receiverIdentity = Users.objects.get(user_id=receiverId)

					# Creation of new row in point transactions table
					newTransaction = PointTransactions.objects.create(sender_id = senderId, recipient_id = receiverId, sent_amount = amount, message = message)

					# Generating point amounts and updating DB
					senderIdentity.points_left = senderIdentity.points_left - amount
					senderIdentity.save()

					# Generating point amounts and updating DB
					receiverIdentity.points_received = receiverIdentity.points_received + amount
					receiverIdentity.save()

					confirmation = 'You sent {} points to {}'.format(str(amount),receiver)

					# Return user back to their hub after sending points
					return render(request, 'points/sendpoints.html', {'message':confirmation})
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
		if (Users.objects.filter(username=redeemer).exists()):

			# Getting userid and setting userclass to a variable
			redeemerId = Users.objects.filter(username=redeemer).values_list('user_id')[0][0]
			redeemerAccount = Users.objects.get(user_id=redeemerId)

			# Validating that redeemer has amount of points
			if redeemerAccount.points_left < pointsredeemed:
				denial = 'Insufficient points to redeem {} giftcards'.format(giftcardnum)
				return render(request, 'points/redeempoints.html', {'message':denial})
			else:
				# Points removal and creation of redeemtransactions 
				newRedeemTransaction = RedeemTransactions.objects.create(user_id=redeemerId, points_redeemed = pointsredeemed)

				redeemerAccount.points_left = redeemerAccount.points_left - pointsredeemed
				redeemerAccount.save()

				confirmation = 'You redeemed {} points for ${}'.format(pointsredeemed, pointsredeemed/100)

			return render(request, 'points/redeempoints.html', {'message':confirmation})
	else:
		return render(request, 'points/redeempoints.html')

def user_history(request):
	if request.method == 'POST':

		points_received_press = True
		points_given_press = False

		if points_received_press:
			return render(request, 'points/user_history.html')
		elif points_given_press:
			return render(request, 'points/user_history.html')

		return render(request, 'points/user_history.html')
	else:
		return render(request, 'points/user_history.html')

def reset_points(request):
	if request.method == 'POST':

		Users.objects.all().update(points_left=1000)

		confirmation = 'Month reset!'

		return render(request, 'points/reset.html', {'message':confirmation})
	else:
		return render(request, 'points/reset.html')
