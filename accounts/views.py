from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.http import JsonResponse
from django.forms.models import model_to_dict
import sys

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
#@admin_only
def home(request):
	orders = LeadOrder.objects.all().order_by('-pk')
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
#@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	print('ORDERS:', orders)

	context = {'orders':orders, 'total_orders':total_orders,
	'delivered':delivered,'pending':pending}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
#@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)




@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin_only'])
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def customers(request):
	customers = Customer.objects.all()

	return render(request, 'accounts/customers.html', {'customers':customers})

@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def orders(request):
	orders = LeadOrder.objects.all()

	return render(request, 'accounts/orders.html', {'orders':orders})



@login_required(login_url='login')
@admin_only
def create_customer(request):	
	form = CustomerForm()
	if request.method == 'POST':
		form = CustomerForm(request.POST)
		param = request.POST
		contactPersonNames = param.getlist("contact_person_name[]")
		contactPersonMobiles = param.getlist("contact_person_mobile[]")
		param = param.dict()	
		
		try:
			if form.is_valid():
				print("contactPersonNames", contactPersonNames)
				print("contactPersonMobiles", contactPersonMobiles)
				user = form.save()

				rows = min([len(contactPersonNames), len(contactPersonMobiles)])
				print("rows", rows)
				for i in range(0, rows):
					contactPerson = CustomerContactPerson(
						# id=None, 
						name=contactPersonNames[i], 
						mobile=contactPersonMobiles[i],

						customer=user
					)
					print("contactPerson", contactPerson)
					contactPerson.save()

				company_name = form.cleaned_data.get('company_name')
				messages.success(request, 'Account was created for ' + company_name)

				return redirect('/')
			else:
				print("Errors", form.errors)
				
		except Exception as error:
			print("An exception was thrown!")
			print(error)
		
	context = {'form':form}
	return render(request, 'accounts/create_customer.html', context)

@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = LeadOrder.objects.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def create_order(request):
	'''
	form = OrderForm(request.POST)
	param = request.POST
	param = param.dict()
	print(param)
			#param['company_name'] = int(param['company_name'])
	obj = LeadOrder(**param)
	obj.save()
	
	#return JsonResponse('success')
	#return HttpResponse('success')

	customers = list(Customer.objects.all().values())
	products = list(Product.objects.all().values())
	context = {'form': form, 'status': LeadOrder.STATUS_L, 'customers': customers, 'products': products,
			   'units': LeadOrder.UNITS}
	return render(request, 'accounts/order_form.html', context)
    '''
	form = OrderForm()	
	if request.method == 'POST':
		form = OrderForm(request.POST)
		param = request.POST
		param = param.dict()
		print(param)

	
		try:
			if form.is_valid():
				obj = LeadOrder(**param)
				
				query=LeadOrder.objects.order_by("-pk")
				
				if len(query)>0:
					last_id= query[0].pk+1
					lead_no= 'LO_'+str(last_id)
				else:
					order_no= 'LO_1'
				obj.lead_no = lead_no
				obj.save()
				context = {
					'error': False
				}
				return JsonResponse(context)
			else:
				context = {
					'error': True,
					'message': form.errors
				}
				return JsonResponse(context)
				
		except Exception as error:
			context = {
				'error': True,
				'message': 'An exception was thrown!'
			}
			return JsonResponse(context)
	users = list(User.objects.all().values())
	customers = list(Customer.objects.all().values())
	products = list(Product.objects.all().values())	
	context = {'form': form, 'status': LeadOrder.STATUS_L, 'users': users, 'customers': customers, 'products': products,
			   'units': LeadOrder.UNITS}
	return render(request, 'accounts/order_form.html', context)


def get_customer_data(request):
	
	if request.method == 'POST':
		try:
			param = request.POST
			param = param.dict()
			param['customer_id'] = int(param['customer_id'])
			print(param)
			customer = Customer.objects.get(pk=param['customer_id'])
			context = {
				'error': False,
				'customer': model_to_dict(customer)
			}
		except:
			context = {
				'error': True,
				'customer': None
			}

		return JsonResponse(context)



'''
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)
'''
@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
	order = LeadOrder.objects.get(id=pk)
	form = OrderForm(instance=order)

	# print('tst', order.order_no)

	#print(form)
	#print('ORDER form:', form)
	if request.method == 'POST':

		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			#obj = Deal()
			query=Deal.objects.order_by("-pk")
			print(query)

			param = request.POST
			param = param.dict()

			obj = Deal(**param)					
			
			if len(query)>0:
				last_id= query[0].pk+1
				deal_no= 'DN_'+str(last_id)
			else:
				deal_no= 'DN_1'

			# copy code from lead

			obj.deal_no = deal_no
			obj.save()
			form.save()
			return redirect('/')
	users = list(User.objects.all().values())
	customers = list(Customer.objects.all().values())
	products = list(Product.objects.all().values())	
	context = {
		'form': form, 
		'status': LeadOrder.STATUS_L, 
		'users': users, 
		'customers': customers, 
		'products': products,
		'units': LeadOrder.UNITS,
		'order': order
	}

	return render(request, 'accounts/order_form_update.html', context)

@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = LeadOrder.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete_item.html', context)