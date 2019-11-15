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
				senderId = Users.objects.filter(username=sender).values_list('userId')[0][0]
				receiverId = Users.objects.filter(username=receiver).values_list('userId')[0][0]

				amount = int(request.POST.get('amount'))
				message = request.POST.get('message')

				senderIdentity = Users.objects.get(userId=senderId)
				receiverIdentity = Users.objects.get(userId=receiverId)

				# buckettest = senderIdentity.givenBucket
				# receivertest = receiverIdentity.received

				senderIdentity.givenBucket = senderIdentity.givenBucket - amount
				senderIdentity.save()

				receiverIdentity.received = receiverIdentity.received + amount
				receiverIdentity.save()

				newTransaction = PointTransactions.objects.create(userGiver = senderIdentity, userReceiver = receiverIdentity, pointAmount = amount, message = message)

		return render(request,'points/hub.html')
	else:
		return render(request, 'points/sendpoints.html')