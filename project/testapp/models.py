from distutils.command.upload import upload
from django.utils import timezone
from django.db import models
from datetime import datetime 

# Create your models here.
class Company(models.Model):
    cname=models.CharField(max_length=100)
    c_logo=models.ImageField(upload_to='uploads')
    hr_sign=models.ImageField(upload_to='uploads')
    def __str__(self):
        return self.cname



class Position(models.Model):
    pname = models.CharField(max_length=100) 
    description = models.CharField(max_length=1000) 
    def __str__(self):
        return str(self.pname)



class Department(models.Model):
    name = models.CharField(max_length=100) 
    description = models.CharField(max_length=300)  

    def __str__(self):
        return self.name


class Salary(models.Model):
    stream_name=models.CharField(max_length=100)

    def __str__(self):
        return self.stream_name

class SalaryHead(models.Model):
    head_name=models.CharField(max_length=100)
    CHOICES=[('0','Credited'),
            ('1','Debited')]
    sm_type= models.CharField(max_length=60,blank=True, default='',choices=CHOICES,verbose_name="salary type")
    def __str__(self):
        return self.head_name

class SalaryStructure(models.Model):
    salary_structure=models.ForeignKey(Position, on_delete=models.CASCADE)
    salary_head=models.ForeignKey(SalaryHead, on_delete=models.CASCADE)
    amount=models.FloatField(default=0)
    def __str__(self):
        return str(self.salary_structure)





class Employee(models.Model):
    employee_id=models.IntegerField()
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)

    gender = (
    ('x', 'Male'),
    ('y', 'Female'),
    )
    pan_no=models.CharField(max_length=10)
    gender = models.CharField(max_length=60, blank=True, default='',choices=gender,verbose_name="gender")
    dob = models.DateField(blank=True,null= True) 
    contact = models.IntegerField() 
    address = models.CharField(max_length=1000) 
    email = models.EmailField(max_length = 100)
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE) 
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE) 
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    offer_date=models.DateField(blank=True,null=True)
    joining_date = models.DateField(blank=True,null=True) 
    package = models.FloatField(default=0)   

    def __str__(self):
        return self.firstname + ' ' +self.middlename + ' '+self.lastname + ' '


class EmpResignation(models.Model):    
    employee_name = models.ForeignKey(Employee, on_delete=models.CASCADE)
    acceptence_date=models.DateField(blank=True,null= True)
    resignation_recieved=models.DateField(blank=True,null= True)
    last_working_date=models.DateField(blank=True,null= True)

    def __str__(self):
        return str(self.employee_name)

class EmpAppraisal(models.Model):    
    employee_name = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE)
    appraisal_date=models.DateField(blank=True,null= True)
    efective_from=models.DateField(blank=True,null= True)

    def __str__(self):
        return str(self.position_id)






class Country(models.Model):
    country=models.CharField(max_length=50)

    def __str__(self):
        return self.country

class Region(models.Model):
    country_name = models.ForeignKey(Country, on_delete=models.CASCADE)
    region=models.CharField(max_length=50)

    def __str__(self):
        return self.region

class State(models.Model):
    country_name = models.ForeignKey(Country, on_delete=models.CASCADE)
    region_name = models.ForeignKey(Region, on_delete=models.CASCADE)
    state_name=models.CharField(max_length=50)

    def __str__(self):
        return self.state_name

class City(models.Model):
    country_name = models.ForeignKey(Country, on_delete=models.CASCADE)
    region_name = models.ForeignKey(Region, on_delete=models.CASCADE)
    state_name=models.ForeignKey(State, on_delete=models.CASCADE)
    city_name=models.CharField(max_length=50)

    def __str__(self):
        return self.city_name








class LeaveMaster(models.Model):
    leave_name=models.CharField(max_length=200)
    no_of_days=models.IntegerField()
    CHOICES=[('0','Paid'),
            ('1','Unpaid')]
    leave_type= models.CharField(max_length=60,blank=True, default='',choices=CHOICES,verbose_name="Leave type")
    def __str__(self):
        return self.leave_name

class LeaveStructure(models.Model):
    name=models.CharField(max_length=200)
    leave_name=models.ForeignKey(LeaveMaster, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Leaves(models.Model):
    employee_name = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_name=models.ForeignKey(LeaveMaster, on_delete=models.CASCADE)
    from_date=models.DateField(blank=True,null= True)
    to_date=models.DateField(blank=True,null= True)
    def __str__(self):
        return str(self.employee_name)

    @property
    def date_diff(self):
        return (self.to_date - self.from_date).days
