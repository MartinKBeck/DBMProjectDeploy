from django.views.generic import TemplateView
from django.shortcuts import render
from points.models import Users

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
			return render(request, 'points/success.html')
		else:
			return HttpResponse("Failed login")
	else:
		return render(request, 'registration/login.html')

class UserHub(TemplateView):
	template_name = 'points/hub.html'