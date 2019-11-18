from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from points.models import Users, PointTransactions, RedeemTransactions, Admin
import hashlib
import pandas as pd
from itertools import chain
from django.db import connection
from django.db.models import Sum, Q
from datetime import date
from django.db.models.functions import Extract, ExtractMonth

# Create your views here.
def Index(request):
	return HttpResponseRedirect('/login')

def  user_login(request):
	if request.method == 'POST':
		# Retreiving user inputs
		username = request.POST.get('username')
		password = request.POST.get('password')

		# Creation of sessions
		request.session['username'] = username

		# Hashing function to test against DB
		password_hash = hashlib.md5(password.encode()).hexdigest()

		# Checking against database
		if (Users.objects.filter(username=username, password=password_hash).exists()):
			request.session['admin'] = 0
			# return render(request, 'points/hub.html', {'username':request.session['username'], 'admin': request.session['admin']})
			return HttpResponseRedirect('/hub')

		if (Admin.objects.filter(username=username, password=password_hash).exists()):
			request.session['admin'] = 1
			return render(request, 'points/hub.html', {'username':request.session['username'], 'admin': request.session['admin']})
		else:
			return render(request, 'registration/login.html', {'message':'Incorrect Login Information'})
	else:
		return render(request, 'registration/login.html')

# Logs user out and resets session
def user_logout(request):
	request.session.flush()
	return HttpResponseRedirect('/login')

def UserHub(request):
	username = request.session['username']

	if (Users.objects.filter(username=username).exists()):
		current_user = Users.objects.filter(username=username).values_list('points_left','points_received')

		points_left = current_user[0][0]
		points_accumulated = current_user[0][1]
		return render(request, 'points/hub.html', {'username': request.session['username'], 'admin': request.session['admin'], 'points_left':points_left, 'points_accumulated':points_accumulated})
	else:
		return render(request, 'points/hub.html', {'username': request.session['username'], 'admin': request.session['admin']})
# Send points page
def send_points(request):

	if request.method == 'POST':

		# If they did not fill in all the fields
		if (request.POST.get('receiver') == "" or request.POST.get('amount')== ""):
			error = "Please fill in all the fields!"
			return render(request, 'points/sendpoints.html', {'message':error})
		
		# They fill in all the fields
		else:
			# If amount entered is valid
			if (request.POST.get('amount').isdigit()):
				# Creation of variables to be used in later sections
				sender = request.session['username']
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

						if(senderIdentity.points_left - amount <0):
							return render(request, 'points/sendpoints.html', {'admin':request.session['admin'], 'message':'Insufficient Funds'})
						else:
							if (request.POST.get('message') == ""):
								message = ""
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
							return render(request, 'points/sendpoints.html', {'message':confirmation, 'admin':request.session['admin']})
				
					# If user does not exist
					else:
						error = "The user you have specified does not exist"
						return render(request, 'points/sendpoints.html', {'message':error, 'admin': request.session['admin']})
			else:
				error = "Please enter a valid amount!"
				return render(request, 'points/sendpoints.html', {'message':error, 'admin': request.session['admin']})
	else:
		return render(request, 'points/sendpoints.html', {'admin':request.session['admin']})

# Page for redeeming points gained
def redeem_points(request):
	if request.method == 'POST':
		if (request.POST.get('giftcardnum')==""):
			error = "Please fill in the amount of gift cards!"
			return render(request, 'points/redeempoints.html', {'message':error, 'admin':request.session['admin']})
		else:
			if request.POST.get('giftcardnum').isdigit():
				# Setting variables to prep for usage
				redeemer = request.session['username']
				giftcardnum = int(request.POST.get('giftcardnum'))
				pointsredeemed = giftcardnum * 1000


				# Check that person exists in database currently
				if (Users.objects.filter(username=redeemer).exists()):

					# Getting userid and setting userclass to a variable
					redeemerId = Users.objects.filter(username=redeemer).values_list('user_id')[0][0]
					redeemerAccount = Users.objects.get(user_id=redeemerId)

					# Validating that redeemer has amount of points
					if (redeemerAccount.points_received < pointsredeemed):
						denial = 'Insufficient points to redeem {} giftcard(s)'.format(giftcardnum)
						return render(request, 'points/redeempoints.html', {'message':denial, 'admin':request.session['admin']})
					else:
						# Points removal and creation of redeemtransactions 
						newRedeemTransaction = RedeemTransactions.objects.create(user_id=redeemerId, points_redeemed = pointsredeemed)

						redeemerAccount.points_received = redeemerAccount.points_received - pointsredeemed
						redeemerAccount.save()

						confirmation = 'You redeemed {} points for {} giftcard(s)'.format(pointsredeemed, giftcardnum)

					return render(request, 'points/redeempoints.html', {'message':confirmation, 'admin':request.session['admin']})
			else:
				error = "Please enter a valid number!"
				return render(request, 'points/redeempoints.html', {'message':error, 'admin':request.session['admin']})
	else:
		return render(request, 'points/redeempoints.html', {'admin':request.session['admin']})

def user_history(request):
	if request.method == 'POST':

		requester = request.session['username']

		# Validate something was passed to form
		if (Users.objects.filter(username=requester).exists()):
		# Getting requesters information
			
			requesterId = Users.objects.filter(username=requester).values_list('user_id')[0][0]
			requesterAccount = Users.objects.get(user_id=requesterId)

			# Receive users choice
			choice = request.POST.get('history_choice')

			# Check users response
			# Pushing specific queries based on the history type they wanted
			if choice == 'points_received':

				# Check that the user has history for receiving points
				if PointTransactions.objects.filter(recipient = requesterId).exists():
					transactionDetail = PointTransactions.objects.filter(recipient = requesterId).order_by('-transaction_date').values_list('sender','sent_amount','transaction_date','message')
					
					return render(request, 'points/user_history.html', {'points_received':transactionDetail, 'admin':request.session['admin']})
				
				else:
					return render(request, 'points/user_history.html', {'message': 'No history for receiving points', 'admin':request.session['admin']})

			elif choice == 'points_given':

				# Check that user has history for giving points
				if PointTransactions.objects.filter(sender = requesterId).exists():

					transactionDetail = PointTransactions.objects.filter(sender = requesterId).order_by('-transaction_date').values_list('recipient','sent_amount','transaction_date','message')

					return render(request, 'points/user_history.html', {'points_given':transactionDetail, 'admin':request.session['admin']})
				else:
					return render(request, 'points/user_history.html', {'message': 'No history for giving points', 'admin':request.session['admin']})
	else:
		return render(request, 'points/user_history.html', {'admin':request.session['admin']})

# Creation of button that will reset user history.
def reset_points(request):
	if request.session['admin']==1:
		if request.method == 'POST':

			Users.objects.all().update(points_left=1000)

			confirmation = 'Month reset!'

			return render(request, 'points/reset.html', {'message':confirmation, 'admin':request.session['admin']})
		else:
			return render(request, 'points/reset.html', {'admin':request.session['admin']})
	else:
		return render(request,'points/login.html')


def redemption_report(request):
		today = date.today()
		
		# Query to show the aggregate usage of points on a monthly basis

		# Query set for aggregate sent points on monthly basis by user
		points_given_agg = pd.DataFrame(PointTransactions.objects.all().values('sender',month=ExtractMonth('transaction_date')).annotate(Sum('sent_amount')), columns=['month','sender','sent_amount__sum'])
		points_given_agg.columns = ['month','user','Points Given']

		# Query set for aggregate received points on monthly basis by user
		points_received_agg = pd.DataFrame(PointTransactions.objects.all().values('recipient',month=ExtractMonth('transaction_date')).annotate(Sum('sent_amount')), columns=['month','recipient','sent_amount__sum'])
		points_received_agg.columns = ['month','user','Points Received']

		# Merging first two queries
		second_df = pd.merge(points_given_agg, points_received_agg, how='outer', left_on=['month','user'], right_on=['month','user'])

		# Query set for aggregate redeemed points on motnhly basis by user
		points_redeemed_agg = pd.DataFrame(RedeemTransactions.objects.all().values('user', month=ExtractMonth('transaction_date')).annotate(Sum('points_redeemed')),columns=['month','user','points_redeemed__sum'])
		points_received_agg.columns = ['month','user','Points Redeemed']

		# Merging last two queries
		final_df = pd.merge(second_df, points_redeemed_agg, how='outer', left_on=['month','user'], right_on=['month','user']).sort_values(by=['month','Points Received'],ascending=False)
		aggregate_data = [tuple(x) for x in final_df.values.tolist()]

		# Query to show who isn’t giving out all of their points for the current recent month only 
		leftover_users = Users.objects.filter(~Q(points_left = 0)).values_list('user_id', 'username', 'points_left')

		# Query to show all redemptions, by month by user, for the previous two months
		redemptions = RedeemTransactions.objects.filter(transaction_date__month__gte = (today.month - 2)).values('user_id', month=Extract('transaction_date','month')).annotate(Sum('points_redeemed')).order_by('-month')

		return render(request, 'points/redemption_report.html', {'aggregate_data': aggregate_data, 'leftover_users': leftover_users,'data': redemptions, 'admin': request.session['admin']})
