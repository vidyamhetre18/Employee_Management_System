from django.contrib import admin

from testapp.models import *

# Register your models here.
admin.site.register(Company)

admin.site.register(Position)

admin.site.register(Department)

admin.site.register(Employee)

admin.site.register(EmpResignation)

admin.site.register(Country)

admin.site.register(Region)

admin.site.register(State)

admin.site.register(City)
admin.site.register(Salary)
admin.site.register(SalaryHead)
admin.site.register(SalaryStructure)

admin.site.register(LeaveMaster)
admin.site.register(LeaveStructure)

admin.site.register(Leaves)
admin.site.register(EmpAppraisal)