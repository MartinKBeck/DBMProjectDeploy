from django.views.generic import TemplateView
from django.shortcuts import render
from points.models import Users, PointTransactions

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
				senderId = Users.objects.filter(username=sender).values_list('user_id')[0][0]
				receiverId = Users.objects.filter(username=receiver).values_list('user_id')[0][0]

				amount = int(request.POST.get('amount'))
				message = request.POST.get('message')

				senderIdentity = Users.objects.get(userId=senderId)
				receiverIdentity = Users.objects.get(userId=receiverId)

				# buckettest = senderIdentity.givenBucket
				# receivertest = receiverIdentity.received

				senderIdentity.points_left = senderIdentity.points_left - amount
				senderIdentity.save()

				receiverIdentity.points_received = receiverIdentity.points_received + amount
				receiverIdentity.save()

				newTransaction = PointTransactions.objects.create(sender_id = senderIdentity, recipient_id = receiverIdentity, sent_amount = amount, message = message)

		return render(request,'points/hub.html')
	else:
		return render(request, 'points/sendpoints.html')