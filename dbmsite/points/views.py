from django.views.generic import TemplateView
from django.shortcuts import render
from points.models import Users, PointTransactions, RedeemTransactions

# Create your views here.

class Index(TemplateView):
	template_name = 'points/index.html'
	
class Register(TemplateView):
	template_name = 'registration/register.html'

class Success(TemplateView):
	template_name = 'points/success.html'

def  user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		if (Users.objects.filter(username=username, password=password).exists()):
			return render(request, 'points/hub.html')
		else:
			return HttpResponse("Failed login")
	else:
		return render(request, 'registration/login.html')

class UserHub(TemplateView):
	template_name = 'points/hub.html'

def send_points(request):
	if request.method == 'POST':

		sender = request.POST.get('sender')
		receiver = request.POST.get('receiver')
		if (Users.objects.filter(username=sender).exists()):

			if (Users.objects.filter(username=receiver).exists()):
				# Finding user_id of each person
				senderId = Users.objects.filter(username=sender).values_list('user_id')[0][0]
				receiverId = Users.objects.filter(username=receiver).values_list('user_id')[0][0]

				# Generating variables to put into point transaction
				amount = int(request.POST.get('amount'))
				message = request.POST.get('message')

				# Pulling the Users object of each party
				senderIdentity = Users.objects.get(user_id=senderId)
				receiverIdentity = Users.objects.get(user_id=receiverId)

				# Generating point amounts and updating DB
				senderIdentity.points_left = senderIdentity.points_left - amount
				senderIdentity.save()

				# Generating point amounts and updating DB
				receiverIdentity.points_received = receiverIdentity.points_received + amount
				receiverIdentity.save()

				# Creation of new row in point transactions table
				newTransaction = PointTransactions.objects.create(sender_id = senderIdentity, recipient_id = receiverIdentity, sent_amount = amount, message = message)

				# Return user back to their hub after sending points
		return render(request,'points/hub.html')
	else:
		return render(request, 'points/sendpoints.html')

def redeem_points(request):
	if request.method == 'POST':

		redeemer = request.POST.get('redeemer')
		giftcardnum = int(request.POST.get('giftcardnum'))

		pointsredeemed = giftcardnum * 10000

		redeemerId = Users.objects.filter(username=redeemer).values_list('user_id')[0][0]
		redeemerAccount = Users.objects.get(user_id=redeemerId)

		if redeemerAccount.points_left < pointsredeemed:
			print('Insufficient Funds')
			return render(request, 'points/redeempoints.html')
		else:
			redeemerAccount.points_left = redeemerAccount.points_left - pointsredeemed
			redeemerAccount.save()

			newRedeemTransaction = RedeemTransactions.objects.create(user_id=redeemerAccount, points_redeemed = pointsredeemed)

		return render(request, 'points/hub.html')
	else:
		return render(request, 'points/redeempoints.html')
