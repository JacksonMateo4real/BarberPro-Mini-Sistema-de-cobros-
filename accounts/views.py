from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import LoginForm, CreateEmployeeForm, UpdateEmployeeForm
from sales.forms import RegisterNewSale
from django.contrib import messages
from clients.models import Client
from sales.models import Sale


from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
# Create your views here.



def login_user(request):

    form = LoginForm()

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            if user.role == 'owner':
                return redirect('owner_dashboard')

            elif user.role == 'barber':
                return redirect('barber_dashboard')

        else:
            messages.error(request, "Credenciales incorrectas, intentelo de nuevo.")

    return render(request, 'login_user_view.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    return redirect ('login')

@login_required
def owner_dashboard(request):
    
    today = timezone.now().date()
    last_week = timezone.now() - timedelta(days=7)

    today_cuts = Sale.objects.filter(
        creation_date__gte=today
    ).count()
    
    today_incomes = Sale.objects.filter(
        creation_date__gte=today
    ).aggregate(total=Sum('price'))['total'] or 0

    last_week_incomes = Sale.objects.filter(
        creation_date__gte=last_week
        ).aggregate(total=Sum('price'))['total'] or 0

    recents_sales = Sale.objects.filter(
        creation_date__date=today
    ).order_by('-creation_date')[:6]

    return render(request, 'accounts/owner/owner_dashboard_view.html', {
        'today_cuts': today_cuts,
        'today_incomes': today_incomes,
        'last_week_incomes': last_week_incomes,
        'recents_sales': recents_sales
    })

def owner_reports_view(request):
    pass
    
@login_required
def owner_employee_details(request):
    barbers = User.objects.filter(role='barber')

    today = timezone.now().date()
    
    #cantidad de servicios del dia de cada barbero.
    barbers_today_cuts = {}
    for barber in barbers:
        count = 0
        for sale in barber.sales.all():
            if sale.creation_date.date() == today:
                count += 1
        barbers_today_cuts[barber.get_full_name()] = count

    #ingresos del dia de cada barbero.
    barbers_today_incomes = {}
    for barber in barbers:
        count = 0

        for sale in barber.sales.all():
            if sale.creation_date.date() == today:
                count += sale.price
        
        barbers_today_incomes[barber.get_full_name()] = count
    #login time
    barbers_today_login_time = {}
    for barber in barbers:
        barbers_today_login_time[barber.get_full_name()] = barber.last_login

    #total de servicios historicos de cada barbero (para el rango)
    barbers_total_sales = {}
    for barber in barbers:
        barbers_total_sales[barber.get_full_name()] = barber.sales.count()

    return render(request, 'accounts/owner/owner_employee_details_view.html', {
        'barbers': barbers,
        'barbers_today_cuts': barbers_today_cuts,
        'barbers_today_incomes': barbers_today_incomes,
        'barbers_today_login_time': barbers_today_login_time,
        'barbers_total_sales': barbers_total_sales,
    })


@login_required
def owner_create_employee(request):
    form = CreateEmployeeForm()
    if request.method == 'POST':
        form = CreateEmployeeForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_superuser = False
            user.set_password(form.cleaned_data['password']) #Hashear password antes de guardar.
            user.save()
            messages.success(request, "Empleado registrado exitosamente")
            return redirect('owner_create_employee')

        else:
            print(form.errors) # ver tipo de error en terminal en caso de haber uno.
            messages.error(request, "Lo sentimos algo ha salido mal...")
            return redirect('owner_create_employee')
    else:
        return render(request, 'accounts/owner/owner_create_employee_view.html', {
            'form': form        
            })

@login_required
@login_required
def owner_update_employee_view(request):
    employees = User.objects.all()
    return render(request, 'accounts/owner/owner_update_employee_view.html', {
        'employees': employees
    })

@login_required
def owner_delete_employee_view(request):
    employees = User.objects.filter(role='barber')
    return render(request, 'accounts/owner/owner_delete_employee_view.html', {
        'employees': employees
    })

@login_required
def owner_update_employee(request):
    employees = User.objects.all()
    form = UpdateEmployeeForm()
    if request.method == 'POST':
        form = UpdateEmployeeForm(request.POST)
        
        if form.is_valid():
            selected_employee = form.cleaned_data['selected_employee_id']

            if form.cleaned_data['username']:
                selected_employee.username = form.cleaned_data['username']
            
            if form.cleaned_data['first_name']:
                selected_employee.first_name = form.cleaned_data['first_name']
            
            if form.cleaned_data['last_name']:
                selected_employee.last_name = form.cleaned_data['last_name']
            
            if form.cleaned_data['email']:
                selected_employee.email = form.cleaned_data['email']
            
            if form.cleaned_data['password']:
                selected_employee.set_password(form.cleaned_data['password'])
            
            if form.cleaned_data['phone_number']:
                selected_employee.phone_number = form.cleaned_data['phone_number']

            if form.cleaned_data['role']:
                selected_employee.role = form.cleaned_data['role']

            selected_employee.save()

            messages.success(request, 'Actualizacion realizada exitosamente!')
            return redirect('owner_update_employee_view')
        
        else:
            messages.error(request, 'Lo sentimos, algo ha salido mal...')
            return render(request, 'accounts/owner/owner_update_employee_view.html', {
                'form': form,
                'employees': employees,
            })
    
    else:
        return redirect('owner_update_employee_view')
        
@login_required
def owner_delete_employee(request):
    if request.user.role != 'owner':
        messages.error(request, "No tienes permiso para realizar esta acción.")
        return redirect('barber_dashboard')

    employees = User.objects.filter(role='barber')
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        
        if employee_id:
            employee = User.objects.get(id=employee_id)
            employee.delete()
            messages.success(request, 'Empleado eliminado correctamente')
        else:
            messages.error(request, 'No se ha recibido el ID del empleado')

        return redirect('owner_delete_employee_view')

    else:
        return render(request, 'accounts/owner/owner_delete_employee_view.html',{
        'employees': employees})
    
@login_required
def home_owner(request):
    return redirect('owner_dashboard')
    
@login_required
def owner_profile(request):
    owner_data = User.objects.get(id=request.user.id)
    if owner_data:
        return render(request, 'accounts/owner/owner_profile_view.html',{
            'owner_data': owner_data})
    else:
        messages.error(request, "Lo sentimos, algo ha salido mal,ponerser en contacto con su admin")
        return redirect('logout')

@login_required  
def barber_dashboard(request):

    today = timezone.now().date()
    last_week = timezone.now() - timedelta(days=7)

    today_cuts = Sale.objects.filter(
        creation_date__date=today,
        user=request.user
    ).count()

    today_incomes = Sale.objects.filter(
        creation_date__date=today,
        user=request.user
    ).aggregate(total=Sum('price'))['total'] or 0

    last_week_incomes = Sale.objects.filter(
        creation_date__gte=last_week,
        user=request.user
    ).aggregate(total=Sum('price'))['total'] or 0


    # ventas recientes, top 5
    recents_sales = Sale.objects.filter(
        creation_date__date=today,
    user=request.user,
    ).order_by('-creation_date')[:6]

    return render(request,'accounts/barber/barber_dashboard_view.html',{
        'today_cuts': today_cuts,
        'today_incomes': today_incomes,
        'last_week_incomes': last_week_incomes,
        'recents_sales': recents_sales
    })
    
@login_required
def barber_home(request):
    return redirect('barber_dashboard')

@login_required
def barber_profile(request):
    barber_data = User.objects.get(id=request.user.id)
    total_services_by_user = Sale.objects.filter(user=barber_data).count()
    if barber_data:
        return render(request, 'accounts/barber/barber_profile_view.html',{
            'barber_data': barber_data,
            'total_services_by_user': total_services_by_user
        })
    else:
        messages.error(
            request, 
            "Lo sentimos, algo ha salido mal,ponerser en contacto con su admin"
            )
        return redirect('logout')