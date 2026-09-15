from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterNewSale
from clients.models import Client
from .models import Sale


@login_required
def register_new_sale(request):

    form = RegisterNewSale()

    if request.method == 'POST':
        form = RegisterNewSale(request.POST)

        if form.is_valid():

            # verificar si el cliente existe
            client_name = form.cleaned_data['client']

            client = Client.objects.filter(full_name=client_name).first()

            if not client:
                client = Client.objects.create(full_name=client_name)

            sale = form.save(commit=False)

            sale.user = request.user
            sale.client = client

            sale.price = Sale.SERVICE_PRICE.get(sale.service_type, 0)

            sale.save()

            messages.success(request, "Venta registrada...")
            return redirect('barber_dashboard')

        else:
            messages.error(request, "Lo sentimos algo ha salido mal...")
            return redirect('register_new_sale')

    return render(request, 'sales/register_new_sale_view.html', {
        'form': form
    })


@login_required
def edit_sale(request, sale_id):
    # solo puede editar sus propias ventas
    sale = get_object_or_404(Sale, id=sale_id, user=request.user)

    if request.method == 'POST':
        form = RegisterNewSale(request.POST, instance=sale)

        if form.is_valid():
            client_name = form.cleaned_data['client']
            client = Client.objects.filter(full_name=client_name).first()

            if not client:
                client = Client.objects.create(full_name=client_name)

            updated_sale = form.save(commit=False)
            updated_sale.client = client
            updated_sale.price = Sale.SERVICE_PRICE.get(updated_sale.service_type, 0)
            updated_sale.save()

            messages.success(request, "Venta actualizada...")
            return redirect('barber_dashboard')

        else:
            messages.error(request, "Lo sentimos algo ha salido mal...")
            return redirect('edit_sale', sale_id=sale.id)

    else:
        form = RegisterNewSale(instance=sale, initial={
            'client': sale.client.full_name if sale.client else ''
        })

    return render(request, 'sales/edit_sale_view.html', {
        'form': form,
        'sale': sale,
    })