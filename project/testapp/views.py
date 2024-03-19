
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from matplotlib.style import context 	
from .forms import *
from.models import *
from datetime import datetime

# Create your views here.

def demo(request):
	# if request.user.is_authenticated:
	return render(request,'testapp/demo.html')


def home(request):
	context = {
        'page_title':'Home',
        'employee':employee,
        'Department':Department,
        'total_department':len(Department.objects.all()),
        'total_company':len(Company.objects.all()),
        'total_employee':len(Employee.objects.all()),
    }
	return render(request, 'testapp/index.html',context)
# def home(request):
# 	# if request.user.is_authenticated:
# 	return render(request,'testapp/index.html',{'name':request.user})
# 	# else:
# 	# 	return redirect('login')

# login page
def login_user (request):
	# if not request.user.is_authenticated:
	if request.method == 'POST': #if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:# if user exist
			login(request, user)
			messages.success(request,(f'succesfully Login !!!!..'))
			return redirect('home') #routes to 'home' on successful login  
		else:
			messages.success(request,('Please enter a correct username and password.'))
			return redirect('login') #re routes to login page upon unsucessful login
	else:
		return render(request, 'testapp/login.html', {})
	# else:
	# 	return redirect('home')

#logout page
def logout_user(request):
	
	messages.success(request,('Youre now logged out'))
	return redirect('login')

# register page
def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# username = form.cleaned_data['username']
			# password = form.cleaned_data['password1']
			# user = authenticate(username=username, password=password)
			# login(request,user)
			messages.success(request, ('Youre now registered'))
			return redirect('login')
	else: 
		form = SignUpForm() 

	context = {'form': form}
	return render(request, 'testapp/register.html', context)


def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You have edited your profile'))
			return redirect('home')
	else: 		#passes in user information 
		form = EditProfileForm(instance= request.user) 

	context = {'form': form}
	return render(request, 'testapp/edit_profile.html', context)
	

def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You have edited your password'))
			return redirect('home')
	else: 		#passes in user information 
		form = PasswordChangeForm(user= request.user) 

	context = {'form': form}
	return render(request, 'testapp/change_password.html', context)

#================ company section =============================
def company(request):
	comp=Company.objects.all()
	context={
		'comp':comp
	}
	
	return render(request,'company/company.html',context)

#add
def addcompany(request):
	form = CompanyForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		messages.success(request,("company Added successful  !!!"))
		
		return redirect('company')
	else:
		return render(request,'company/addcompany.html',{'form':form})





# ajax call unique company

def validate_company(request):
	cname = request.GET.get('cname',None)
    
	data = {
		'is_taken': Company.objects.filter(cname=cname).exists()
	}
	if data['is_taken']:
		data['error_messages']='company is already exists..'
	return JsonResponse(data)




# #django user already exist
# def addcompany(request):
	
# 	if request.POST:
# 		cname=request.POST['cname']
# 		c_logo=request.POST['c_logo']
# 		hr_sign=request.POST['hr_sign']

# 		form=CompanyForm(request.POST)
# 		if form.is_valid():
# 			check_existing=Company.objects.filter(cname=cname).exists()
# 			if check_existing:
# 				messages.success(request,("company name already exist  !!!"))
# 				return redirect('addcompany')
# 			else:
# 				form=Company(cname=cname,c_logo=c_logo,hr_sign=hr_sign)
# 				form.save()
# 				messages.success(request,("company Added successful  !!!"))
# 				return redirect('company')
# 	else:
# 		form=CompanyForm()
# 	return render(request,'company/addcompany.html',{'form':form})



#delete
def deletecomp(request,id=None):
	comp=Company.objects.get(id=id)	
	comp.delete()
	messages.add_message(request,messages.INFO,f"{comp.cname} company deleted")
	return redirect('company')
	
	

#edit
def editcomp(request,id):
	if request.method=='POST':
		comp=Company.objects.get(pk=id)
		fm=CompanyForm(request.POST,instance=comp)
		if fm.is_valid():
			fm.save()
			messages.add_message(request,messages.INFO,f"{comp.cname} company updated")
			return redirect('company')				
		else:
			comp=Company.objects.get(pk=id)
			fm=CompanyForm(instance=comp)			
	return render(request,'company/editcompany.html',{'form':fm})




#================ position section =============================
def position(request):
    positions = Position.objects.all()
    context = {
        
        'positions':positions,
    }
    return render(request,'position/positions.html',context)


def addposition(request):
	if request.method=="POST":
		pname=request.POST['pname']
		description=request.POST['description']

		comp=Position(pname=pname,description=description)
		comp.save()
		messages.success(request,("Position Added successful  !!!"))
		return redirect('position')
	else:
		return render(request,'position/addposition.html')


#ajax POSITION unique
def validate_position(request):
	pname = request.GET.get('pname',None)
    
	data = {
		'is_taken': Position.objects.filter(pname=pname).exists()
	}
	if data['is_taken']:
		data['error_messages']='is already exists..'
	return JsonResponse(data)



def deletepos(request,id=None):
	pos=Position.objects.get(id=id)	
	pos.delete()
	messages.add_message(request,messages.INFO,f"{pos.pname} position deleted")
	return redirect('position')
	

def editposition(request,id):
	if request.method=='POST':
		pos=Position.objects.get(pk=id)
		fm=PositionForm(request.POST,instance=pos)
		if fm.is_valid():
			fm.save()
			messages.success(request,("position Edit successful  !!!"))
			return redirect('position')				
		else:
			pos=Position.objects.get(pk=id)
			fm=PositionForm(instance=pos)
					
	return render(request,'position/editposition.html',{'form':fm})


#================department section=============================


def department(request):
	depart=Department.objects.all()
	context={
		'depart':depart
	}
	
	return render(request,'department/department.html',context)

#add 
def adddepart(request):
	if request.method=="POST":
		name=request.POST['name']
		description=request.POST['description']

		depart=Department(name=name,description=description)
		depart.save()
		messages.success(request,("Department Added successful  !!!"))
		return redirect('department')
	else:
		return render(request,'department/adddepartment.html')

#delete

def deletedepart(request,id=None):
	depart=Department.objects.get(id=id)	
	depart.delete()
	messages.add_message(request,messages,f"{depart.name} Department deleted")
	return redirect('department')


#edit
def editdepart(request,id):
	if request.method=='POST':
		dep=Department.objects.get(pk=id)
		fn=DepartmentForm(request.POST,instance=dep)
		if fn.is_valid():
			fn.save()
			messages.success(request,("department Edit successful  !!!"))
			return redirect('department')				
		else:
			dep=Department.objects.get(pk=id)
			fn=DepartmentForm(instance=dep)
	context={
		'form':fn
	}
				
	return render(request,'department/editdepartment.html',context)



#================  employee section=============================

def employee(request):
	emp=Employee.objects.all()
	context={
		'emp':emp
	}
	
	return render(request,'employee/employee.html',context)



def addemp(request):
	employee = EmployeeForm()
	departments=Department.objects.all()
	positions = Position.objects.all()
	company=Company.objects.all()

	if request.method == 'POST':
		form = EmployeeForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,("Employee Added successful  !!!"))
			return redirect('employee')
	else:
		form=EmployeeForm()		

	context = {
		'form':form,
		'employee' : employee,
		'departments' : departments,
		'positions' : positions,
		'company':company
	}
	return render(request, 'employee/addemp.html', context)

#salary slip
import datetime
def salary_slip(request,id):
	emp=Employee.objects.get(id=id)
	context={
		'emp':emp
	}
	return render(request,'employee/salary_slip.html',context)

#increment letter

def increment_letter(request,id):
	currentdate = datetime.date.today()
	formatDate = currentdate.strftime("%d-%b-%y")
	emp=Employee.objects.get(id=id)
	context={
		'emp':emp,
		'currentdate':currentdate,
		'format_date':formatDate
	}
	return render(request,'employee/increment_letter.html',context)


#offer letter

def offer_letter(request,id):
	currentdate = datetime.date.today()
	formatDate = currentdate.strftime("%d-%b-%y")
	emp=Employee.objects.get(id=id)
	context={
		'emp':emp,
		'currentdate':currentdate,
		'format_date':formatDate
	}
	return render(request,'employee/offer_letter.html',context)

#experiance  letter

def experiance_letter(request,id):
	currentdate = datetime.date.today()
	formatDate = currentdate.strftime("%d-%b-%y")
	emp=Employee.objects.get(id=id)
	context={
		'emp':emp,
		'currentdate':currentdate,
		'format_date':formatDate
	}
	return render(request,'employee/experiance_letter.html',context)


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

# def render_to_pdf(template_src, context_dict={}):
# 	template = get_template(template_src)
# 	html  = template.render(context_dict)
# 	result = BytesIO()
# 	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
# 	if not pdf.err:
# 		return HttpResponse(result.getvalue(), content_type='application/pdf')
# 	return None

#Opens up page as PDF
def offer_letter_pdf(request,id):
	emp=Employee.objects.get(pk=id)
	currentdate = datetime.date.today()
	formatDate = currentdate.strftime("%d-%b-%y")
	template_path = 'employee/offer_letter.html'
	context={
		'emp':emp,
		'currentdate':currentdate,
		'format_date':formatDate
	}
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="offer.pdf"'
	template = get_template(template_path)
	html = template.render(context)
	pisa_status = pisa.CreatePDF(html, dest=response)
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response

def increment_letter_pdf(request,id):
	emp=Employee.objects.get(pk=id)
	currentdate = datetime.date.today()
	formatDate = currentdate.strftime("%d-%b-%y")
	
	template_path = 'employee/increment_letter.html'
	context={
		'emp':emp,
		'currentdate':currentdate,
		'format_date':formatDate
	}
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="increment_letter.pdf"'
	template = get_template(template_path)
	html = template.render(context)
	pisa_status = pisa.CreatePDF(html, dest=response)
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response

def salary_slip_pdf(request,id):
	emp=Employee.objects.get(pk=id)
	
	template_path = 'employee/salary_slip.html'
	context={'emp':emp}
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="salary_slip.pdf"'
	template = get_template(template_path)
	html = template.render(context)
	pisa_status = pisa.CreatePDF(html, dest=response)
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response

def experiance_letter_pdf(request,id):
	currentdate = datetime.date.today()
	formatDate = currentdate.strftime("%d-%b-%y")
	emp=Employee.objects.get(id=id)
	context={
		'emp':emp,
		'currentdate':currentdate,
		'format_date':formatDate
	}
	template_path = 'employee/experiance_letter.html'
	
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="experiance_letter.pdf"'
	template = get_template(template_path)
	html = template.render(context)
	options = {
        'page-size': 'A4',
        'margin-top': '0in',
        'margin-right': '0in',
        'margin-bottom': '0in',
        'margin-left': '0in',
        'encoding': "UTF-8",
        'no-outline': None
    }
	pisa_status = pisa.CreatePDF(html, dest=response)
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response




#ajax emp email unique
def validate_email(request):
	email = request.GET.get('email',None)
    
	data = {
		'is_taken': Employee.objects.filter(email=email).exists()
	}
	if data['is_taken']:
		data['error_messages']='is already exists..'
	return JsonResponse(data)




def deleteemp(request,id=None):
	emp=Employee.objects.get(id=id)
	
	emp.delete()
	messages.add_message(request,messages.INFO,f"{emp.firstname} Employee deleted")
	return redirect('employee')
	

def editemp(request,id):
	if request.method=='POST':
		emp=Employee.objects.get(pk=id)
		fn=EmployeeForm(request.POST,instance=emp)
		if fn.is_valid():	
			fn.save()
			messages.success(request,("Employee Edit successful  !!!"))
			return redirect('employee')				
		else:
			dep=Employee.objects.get(pk=id)
			fn=EmployeeForm(instance=dep)
	context = {
        'form': fn,
    }				
	return render(request,'employee/editemp.html',context)




#================  employee Resignation  =============================

def emp_resignation(request):
	form=EmpResignation.objects.all()
	context={
		'form':form
	}
	return render(request,'emp_resignation/emp_resignation.html',context)


def add_resignation(request):
	employee = Employee.objects.all()
	if request.method == 'POST':
		form = EmployeeResignationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,("Employee REsignation Added successful  !!!"))
			return redirect('emp_resignation')
	else:
		form=EmployeeResignationForm()		
	context={
		'employee':employee,
		'form':form
	}
	return render(request, 'emp_resignation/add_resignation.html',context)

#ajax resignation already exist
def validate_resignation(request):
	employee_name = request.GET.get('employee_name',None)
    
	data = {
		'is_taken': EmpResignation.objects.filter(employee_name=employee_name).exists()
	}
	if data['is_taken']:
		data['error_messages']='employee is already resigned..'
	return JsonResponse(data)









def edit_resignation(request,id):
	if request.method=='POST':
		emp=EmpResignation.objects.get(pk=id)
		fn=EmployeeResignationForm(request.POST,instance=emp)
		if fn.is_valid():	
			fn.save()
			messages.success(request,("Employee Edit successful  !!!"))
			return redirect('emp_resignation')				
		else:
			emp=EmpResignation.objects.get(pk=id)
			fn=EmployeeResignationForm(instance=emp)
	context = {
        'form': fn,
    }				
	return render(request,'emp_resignation/edit_resignation.html',context)


def deleteemp_res(request,id=None):
	emp=EmpResignation.objects.get(id=id)
	
	emp.delete()
	messages.add_message(request,messages.INFO,f" Employee deleted")
	return redirect('emp_resignation')
	








#================  employee Apprisal =============================

def emp_apprisal(request):
	emp=EmpAppraisal.objects.all()
	context={
		'emp':emp
	}
	
	return render(request,'emp_apprisal/emp_apprisal.html',context)



def add_emp_apprisal(request):
	emp_apprisal = EmpAppraisal()
	positions = Position.objects.all()
	employee = Employee.objects.all()
	salary_structre=SalaryStructure.objects.all()

	if request.method == 'POST':
		form = EmpAppraisalForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,("Employee Added successful  !!!"))
			return redirect('emp_apprisal')
	else:
		form=EmpAppraisalForm()		

	context = {
		'form':form,
		'employee' : employee,
		'emp_apprisal' : emp_apprisal,
		'positions' : positions,
		'salary_structre':salary_structre
	}
	return render(request, 'emp_apprisal/add_emp_apprisal.html', context)


def delete_emp_apprisal(request,id=None):
	emp=EmpAppraisal.objects.get(id=id)
	
	emp.delete()
	messages.success(request,'successfully deleted')
	return redirect('emp_apprisal')
	

# def edit_emp_apprisal(request,id):
# 	if request.method=='POST':
# 		emp=EmpAppraisal.objects.get(pk=id)
# 		fn=EmpAppraisalForm(request.POST,instance=emp)
# 		if fn.is_valid():	
# 			fn.save()
# 			messages.success(request,("Employee Edit successful!!!"))
# 			return redirect('emp_apprisal')				
# 		else:
# 			emp=EmpAppraisal.objects.get(pk=id)
# 			fn=EmpAppraisalForm(instance=emp)
# 	context={'form': fn,
# 				'emp':emp}				
# 	return render(request,'emp_apprisal/edit_emp_apprisal.html',context)


def edit_emp_apprisal(request,id):
	if request.method=='POST':
		emp=EmpAppraisal.objects.get(pk=id)
		fn=EmpAppraisalForm(request.POST,instance=emp)
		if fn.is_valid():	
			fn.save()
			messages.success(request,(" Edit successful  !!!"))
			return redirect('emp_apprisal')				
		else:
			emp=EmpAppraisal.objects.get(pk=id)
			fn=EmpAppraisalForm(instance=emp)
				
	return render(request,'emp_apprisal/edit_emp_apprisal.html',{'form': fn})










#================  COUNTRY  =============================

def country(request):
	c=Country.objects.all()
	context={
		'c':c
	}	
	return render(request,'country/country.html',context)

def country_delete(request,id):
	c=Country.objects.get(id=id)
	c.delete()
	messages.success(request,("Deleted successful  !!!"))
	return redirect('country')
	

def add_country(request):
	c=Country.objects.all()
	if request.method=='POST':
		c=CountryForm(request.POST)
		if c.is_valid():
			c.save()
			messages.success(request,(" Added successful  !!!"))
			return redirect('country')
	else:
		c=CountryForm()		
	context={'country':c,}
	return render(request, 'country/add_country.html',context)


def edit_country(request,id):
	if request.method=='POST':
		c=Country.objects.get(pk=id)
		fn=CountryForm(request.POST,instance=c)
		if fn.is_valid():	
			fn.save()
			messages.success(request,(" Edit successful  !!!"))
			return redirect('country')				
		else:
			c=Country.objects.get(pk=id)
			fn=CountryForm(instance=c)
	context = {
        'form': fn,
    }				
	return render(request,'country/edit_country.html',context)


#================  REgion  =============================
def region(request):
	fm=Region.objects.all()

	return render(request,'region/region.html',{'form':fm})


def add_region(request):
	r=Region.objects.all()
	c=Country.objects.all()
	if request.method=='POST':
		r=RegionForm(request.POST)
		if r.is_valid():
			r.save()
			messages.success(request,("Added successful !!!"))
			return redirect('region')
	else:
		r=RegionForm()		
	context={'region':r,
			'country':c		}
	return render(request,'region/add_region.html',context)


def region_delete(request,id):
	r=Region.objects.get(id=id)
	r.delete()
	messages.success(request,("Deleted successful  !!!"))
	return redirect('region')


def edit_region(request,id):
	if request.method=='POST':
		c=Region.objects.get(pk=id)
		fn=RegionForm(request.POST,instance=c)
		if fn.is_valid():	
			fn.save()
			messages.success(request,(" Edit successful  !!!"))
			return redirect('region')				
		else:
			c=Region.objects.get(pk=id)
			fn=RegionForm(instance=c)
	context = {
        'form': fn,
    }				
	return render(request,'region/edit_region.html',context)


#================  StATE =============================

def state(request):
	fm=State.objects.all()

	return render(request,'state/state.html',{'form':fm})


def add_state(request):
	s=State.objects.all()
	c=Country.objects.all()
	r=Region.objects.all()
	if request.method=='POST':
		s=StateForm(request.POST)
		if s.is_valid():
			s.save()
			messages.success(request,("Added successful !!!"))
			return redirect('state')
	else:
		s=StateForm()		
	context={'region':r,
			'country':c,	
			'state':s,		}
	return render(request,'state/add_state.html',context)


def delete_state(request,id):
	s=State.objects.get(id=id)
	s.delete()
	messages.success(request,("Deleted successful  !!!"))
	return redirect('state')


def edit_state(request,id):
	if request.method=='POST':
		c=State.objects.get(pk=id)
		fn=StateForm(request.POST,instance=c)
		if fn.is_valid():	
			fn.save()
			messages.success(request,(" Edit successful  !!!"))
			return redirect('state')				
		else:
			c=State.objects.get(pk=id)
			fn=StateForm(instance=c)
	context = {
        'form': fn,
    }				
	return render(request,'state/edit_state.html',context)


#ajax region dependent dropdown
def load_cities(request):
    country_id = request.GET.get('country_name')
    cities = Region.objects.filter(country_id=country_id).order_by('region')
    return render(request, 'state/state_dropdown_list.html', {'cities': cities})



#================ City =============================

def city(request):
	fm=City.objects.all()

	return render(request,'city/city.html',{'form':fm})



def add_city(request):
	cy=City.objects.all()
	# s=State.objects.all()
	c=Country.objects.all()
	r=Region.objects.all()
	if request.method=='POST':
		cy=CityForm(request.POST)
		if cy.is_valid():
			cy.save()
			messages.success(request,("Added successful !!!"))
			return redirect('city')
	else:
		cy=CityForm()		
	context={'region':r,
			'country':c,		
			'city':cy	}
	return render(request,'city/add_city.html',context)


def delete_city(request,id):
	cy=City.objects.get(id=id)
	cy.delete()
	messages.success(request,("Deleted successful  !!!"))
	return redirect('city')



def edit_city(request,id):
	if request.method=='POST':
		cy=City.objects.get(pk=id)
		fn=CityForm(request.POST,instance=cy)
		if fn.is_valid():	
			fn.save()
			messages.success(request,(" Edit successful  !!!"))
			return redirect('city')				
		else:
			cy=City.objects.get(pk=id)
			fn=CityForm(instance=cy)
	context = {
        'form': fn,
    }				
	return render(request,'city/edit_city.html',context)


# ================ Salary MAster =============================
def salary_master(request):
	fm=Salary.objects.all()

	return render(request,'salary/salary_master/salary_master.html',{'form':fm})

def delete_sm(request,id):
	sm=Salary.objects.get(id=id)
	sm.delete()
	messages.success(request,("Deleted successful  !!!"))
	return redirect('salary_master')



def add_sm(request):
	sm=Salary.objects.all()
	
	if request.method=='POST':
		sm=SalaryForm(request.POST)
		if sm.is_valid():
			sm.save()
			messages.success(request,("Added successful !!!"))
			return redirect('salary_master')
	else:
		sm=SalaryForm()		
	context={'salary':sm,
				}
	return render(request,'salary/salary_master/add_sm.html',context)

def edit_sm(request,id):
	if request.method=='POST':
		sm=Salary.objects.get(pk=id)
		fn=SalaryForm(request.POST,instance=sm)
		if fn.is_valid():	
			fn.save()
			messages.success(request,(" Edit successful  !!!"))
			return redirect('salary_master')				
		else:
			sm=Salary.objects.get(pk=id)
			fn=SalaryForm(instance=sm)
	context = {
        'form': fn,
    }				
	return render(request,'salary/salary_master/edit_sm.html',context)


# ================ Salary Head =============================
def salary_head(request):
	fm=SalaryHead.objects.all()
	return render(request,'salary/salary_head/salary_head.html',{'form':fm})


def add_sh(request):
	sh=SalaryHead.objects.all()
	
	if request.method=='POST':
		sh=SalaryHeadForm(request.POST)
		if sh.is_valid():
			sh.save()
			messages.success(request,("Added successful !!!"))
			return redirect('salary_head')
	else:
		sh=SalaryHeadForm()		
	context={'salary':sh,
				}
	return render(request,'salary/salary_head/add_sh.html',context)

def delete_sh(request,id):
	sh=SalaryHead.objects.get(id=id)
	sh.delete()
	messages.success(request,("Deleted successful  !!!"))
	return redirect('salary_head')

def edit_sh(request,id):
	if request.method=='POST':
		sh=SalaryHead.objects.get(pk=id)
		fn=SalaryHeadForm(request.POST,instance=sh)
		if fn.is_valid():	
			fn.save()
			messages.success(request,(" Edit successful  !!!"))
			return redirect('salary_head')				
		else:
			sm=SalaryHead.objects.get(pk=id)
			fn=SalaryHeadForm(instance=sh)
	context = {
        'form': fn,
    }				
	return render(request,'salary/salary_head/edit_sh.html',context)



# ================ Salary Structure=============================
def salary_structure(request):
	fm=SalaryStructure.objects.all()
	return render(request,'salary/salary_structure/salary_structure.html',{'form':fm})

def delete_ss(request,id):
	ss=SalaryStructure.objects.get(id=id)
	ss.delete()
	
	return redirect('salary_structure')


def add_ss(request):
	ss=SalaryStructure.objects.all()
	
	if request.method=='POST':
		ss=SalaryStructureForm(request.POST)
		if ss.is_valid():
			ss.save()
			messages.success(request,("Added successful !!!"))
			return redirect('salary_structure')
	else:
		ss=SalaryStructureForm()		
	context={'salary':ss,
				}
	return render(request,'salary/salary_structure/add_ss.html',context)


def edit_ss(request,id):
	if request.method=='POST':
		ss=SalaryStructure.objects.get(pk=id)
		fn=SalaryStructureForm(request.POST,instance=ss)
		if fn.is_valid():	
			fn.save()
			messages.success(request,(" Edit successful  !!!"))
			return redirect('salary_structure')				
		else:
			ss=SalaryStructure.objects.get(pk=id)
			fn=SalaryStructureForm(instance=ss)
	context = {
        'form': fn,
    }				
	return render(request,'salary/salary_structure/edit_ss.html',context)




# ================ Leave Master =============================
def leave_master(request):
	fm=LeaveMaster.objects.all()
	return render(request,'leave/leave_master/leave_master.html',{'form':fm})

def delete_lm(request,id):
	lm=LeaveMaster.objects.get(id=id)
	lm.delete()
	messages.success(request,("Deleted successful  !!!"))
	return redirect('leave_master')


def add_lm(request):
	lm=LeaveMaster.objects.all()
	
	if request.method=='POST':
		lm=LeaveMasterForm(request.POST)
		if lm.is_valid():
			lm.save()
			messages.success(request,("Added successful !!!"))
			return redirect('leave_master')
	else:
		lm=LeaveMasterForm()		
	context={'leave':lm,
				}
	return render(request,'leave/leave_master/add_lm.html',context)


def edit_lm(request,id):
	if request.method=='POST':
		lm=LeaveMaster.objects.get(pk=id)
		fn=LeaveMasterForm(request.POST,instance=lm)
		if fn.is_valid():	
			fn.save()
			messages.success(request,(" Edit successful  !!!"))
			return redirect('leave_master')				
		else:
			lm=LeaveMaster.objects.get(pk=id)
			fn=LeaveMasterForm(instance=lm)
	context = {
        'form': fn,
    }				
	return render(request,'leave/leave_master/edit_lm.html',context)




# ================ Leave Structure ============================
def leave_structure(request):
	fm=LeaveStructure.objects.all()
	return render(request,'leave/leave_structure/leave_structure.html',{'form':fm})

def delete_ls(request,id):
	ls=LeaveStructure.objects.get(id=id)
	ls.delete()
	messages.success(request,("Deleted successful  !!!"))
	return redirect('leave_structure')


def add_ls(request):
	ls=LeaveStructure.objects.all()
	
	if request.method=='POST':
		ls=LeaveStructureForm(request.POST)
		if ls.is_valid():
			ls.save()
			messages.success(request,("Added successful !!!"))
			return redirect('leave_structure')
	else:
		ls=LeaveStructureForm()		
	context={'leave':ls,
				}
	return render(request,'leave/leave_structure/add_ls.html',context)


def edit_ls(request,id):
	if request.method=='POST':
		ls=LeaveStructure.objects.get(pk=id)
		fn=LeaveStructureForm(request.POST,instance=ls)
		if fn.is_valid():	
			fn.save()
			messages.success(request,(" Edit successful  !!!"))
			return redirect('leave_structure')				
		else:
			ls=LeaveStructure.objects.get(pk=id)
			fn=LeaveStructureForm(instance=ls)
	context = {
        'form': fn,
    }				
	return render(request,'leave/leave_structure/edit_ls.html',context)




# ================ Leaves ============================
def leaves(request):
	fm=Leaves.objects.all()
	
	return render(request,'leave/leaves/leaves.html',{'form':fm})

def delete_leaves(request,id):
	l=Leaves.objects.get(id=id)
	l.delete()
	messages.success(request,("Deleted successful  !!!"))
	return redirect('leaves')


def add_leaves(request):
	l=Leaves.objects.all()
	employee = Employee.objects.all()
	if request.method=='POST':
		l=LeavesForm(request.POST)
		if l.is_valid():
			l.save()
			messages.success(request,("Added successful !!!"))
			return redirect('leaves')
	else:
		l=LeavesForm()		
	context={'leave':l,
				'emp':employee}
	return render(request,'leave/leaves/add_leaves.html',context)


def edit_leaves(request,id):
	if request.method=='POST':
		l=Leaves.objects.get(pk=id)
		fn=LeavesForm(request.POST,instance=l)
		if fn.is_valid():	
			fn.save()
			messages.success(request,(" Edit successful  !!!"))
			return redirect('leaves')				
		else:
			l=Leaves.objects.get(pk=id)
			fn=LeavesForm(instance=l)
	context = {
        'form': fn,
    }				
	return render(request,'leave/leaves/edit_leaves.html',context)




