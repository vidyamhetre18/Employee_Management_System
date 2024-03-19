from django.conf.urls.static import static
from django.conf import settings


from django.conf import settings
from testapp import views
from django.urls import include, path
from django.views.generic.base import RedirectView
# from django.conf.urls import url
urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('home/',views.home,name="home"),
    path('demo/',views.demo,name="demo"),
    path('', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),


#   company
    path('company/', views.company, name='company'),
    path('addcompany/', views.addcompany, name='addcompany'),
    path('deletecomp/<int:id>', views.deletecomp, name='deletecomp'),
    path('editcomp<int:id>/', views.editcomp, name='editcomp'),

    path('validate_company/', views.validate_company, name='validate_company'),

#   positions    
    path('position/', views.position, name='position'),
    path('addposition/', views.addposition, name='addposition'),
    path('deletepos/<int:id>/', views.deletepos, name='deletepos'),
    path('editposition/<int:id>/', views.editposition, name='editposition'),
    #ajax 
    path('validate_position/', views.validate_position, name='validate_position'),

#   department
    path('department/', views.department, name='department'),
    path('adddepart/', views.adddepart, name='adddepart'),
    path('deletedepart/<int:id>/', views.deletedepart, name='deletedepart'),
    path('editdepart/<int:id>/', views.editdepart, name='editdepart'),

#   employee
    path('employee/', views.employee, name='employee'),
    path('addemp/', views.addemp, name='addemp'),
    path('deleteemp/<int:id>/', views.deleteemp, name='deleteemp'),
    path('editemp/<int:id>/', views.editemp, name='editemp'),
    #ajax unique username
    path('validate_email/', views.validate_email, name='validate_email'),
    #salary_slip
    path('salary_slip_pdf/<int:id>/', views.salary_slip_pdf, name='salary_slip_pdf'),
    path('increment_letter_pdf/<int:id>/', views.increment_letter_pdf, name='increment_letter_pdf'),
    
    path('experiance_letter_pdf/<int:id>/', views.experiance_letter_pdf, name='experiance_letter_pdf'),
    path('offer_letter_pdf/<int:id>/', views.offer_letter_pdf, name='offer_letter_pdf'),

#   employee RESIGNATION
    path('emp_resignation/', views.emp_resignation, name='emp_resignation'),
    path('add_resignation/', views.add_resignation, name='add_resignation'),
    path('edit_resignation/<int:id>/', views.edit_resignation, name='edit_resignation'),
    path('deleteemp_res/<int:id>/', views.deleteemp_res, name='deleteemp_res'),
    #ajax emp already resigned
    path('validate_resignation/', views.validate_resignation, name='validate_resignation'),

#   employee Apprisal
    path('emp_apprisal/', views.emp_apprisal, name='emp_apprisal'),
    path('add_emp_apprisal/', views.add_emp_apprisal, name='add_emp_apprisal'),
    path('edit_emp_apprisal/<int:id>/', views.edit_emp_apprisal, name='edit_emp_apprisal'),
    path('delete/<int:id>/', views.delete_emp_apprisal, name='delete_emp_apprisal'),



#   Country
    path('country/', views.country, name='country'),
    path('add_country/', views.add_country, name='add_country'),
    path('edit_country/<int:id>/', views.edit_country, name='edit_country'),
    path('country/<int:id>/', views.country_delete, name='country_delete'),


#   region
    path('region/', views.region, name='region'),
    path('add_region/', views.add_region, name='add_region'),
    path('edit_region/<int:id>/', views.edit_region, name='edit_region'),
    path('region/<int:id>/', views.region_delete, name='region_delete'),

#   State
    path('state/', views.state, name='state'),
    path('add_state/', views.add_state, name='add_state'),
    path('edit_state/<int:id>/', views.edit_state, name='edit_state'),
    path('state/<int:id>/', views.delete_state, name='delete_state'),

    path('load-cities/', views.load_cities, name='ajax_load_cities'),
      
#   city
    path('city/', views.city, name='city'),
    path('add_city/', views.add_city, name='add_city'),
    path('edit_city/<int:id>/', views.edit_city, name='edit_city'),
    path('city/<int:id>/', views.delete_city, name='delete_city'),
      
      
#   Salary Master
    path('salary_master/', views.salary_master, name='salary_master'),
    path('add_sm/', views.add_sm, name='add_sm'),
    path('edit_sm/<int:id>/', views.edit_sm, name='edit_sm'),
    path('sm/<int:id>/', views.delete_sm, name='delete_sm'),
      

#   Salary Head
    path('salary_head/', views.salary_head, name='salary_head'),
    path('add_sh/', views.add_sh, name='add_sh'),
    path('edit_sh/<int:id>/', views.edit_sh, name='edit_sh'),
    path('sh/<int:id>/', views.delete_sh, name='delete_sh'),
      
#   Salary Structure
    path('salary_structure/', views.salary_structure, name='salary_structure'),
    path('add_ss/', views.add_ss, name='add_ss'),
    path('edit_ss/<int:id>/', views.edit_ss, name='edit_ss'),
    path('ss/<int:id>/', views.delete_ss, name='delete_ss'),


#   Leave MAster
    path('leave_master/', views.leave_master, name='leave_master'),
    path('add_lm/', views.add_lm, name='add_lm'),
    path('edit_lm/<int:id>/', views.edit_lm, name='edit_lm'),
    path('lm/<int:id>/', views.delete_lm, name='delete_lm'),
      

#   Leave Structure
    path('leave_structure/', views.leave_structure, name='leave_structure'),
    path('add_ls/', views.add_ls, name='add_ls'),
    path('edit_ls/<int:id>/', views.edit_ls, name='edit_ls'),
    path('ls/<int:id>/', views.delete_ls, name='delete_ls'),
      
#   Leaves
    path('leaves/', views.leaves, name='leaves'),
    path('add_leaves/', views.add_leaves, name='add_leaves'),
    path('edit_leaves/<int:id>/', views.edit_leaves, name='edit_leaves'),
    path('leaves/<int:id>/', views.delete_leaves, name='delete_leaves'),
      


      
]
