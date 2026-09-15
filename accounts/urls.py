from django.urls import path
from .views import login_user, logout_user
from .views import owner_dashboard, owner_employee_details
from. views import barber_dashboard
from .views import barber_profile, owner_profile
from .views import owner_update_employee_view, owner_delete_employee_view
from .views import owner_create_employee, owner_delete_employee, owner_update_employee

urlpatterns = [
    path('', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    #Path del owner
    path('propietario/perfil', owner_profile, name='owner_profile'),
    path('propietario/dashboard', owner_dashboard, name='owner_dashboard'),
    path('propietario/empleado', owner_employee_details, name='owner_employee_details'),
    path('propietario/crear_empleado', owner_create_employee, name='owner_create_employee'),
    path('propietario/actualizar_empleado/', owner_update_employee_view, name='owner_update_employee_view'),
    path('propietario/eliminar_empleado/', owner_delete_employee_view, name='owner_delete_employee_view'),
    path('propietario/actualizar_empleado/seleccionar', owner_update_employee, name='owner_update_employee'),
    path('propietario/eliminar_empleado/seleccionar', owner_delete_employee, name='owner_delete_employee'),

    
    
    #Paht del barber
    path('barbero/dashboard', barber_dashboard, name='barber_dashboard' ),
    path('barbero/perfil', barber_profile, name='barber_profile'),
]