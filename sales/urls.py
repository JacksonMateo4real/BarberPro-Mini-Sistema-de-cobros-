from django.urls import path
from .views import register_new_sale, edit_sale



urlpatterns = [
    path('ventas/registrar', register_new_sale, name='register_new_sale'),
    path('ventas/editar/<int:sale_id>', edit_sale, name='edit_sale'),
]