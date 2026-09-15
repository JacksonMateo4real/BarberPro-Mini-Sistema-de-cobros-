from django import forms
from .models import Sale


class RegisterNewSale(forms.ModelForm):

    client = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    service_type = forms.ChoiceField(
        choices=(
            ('haircut', 'Corte'),
            ('beard', 'Barba'),
            ('haircut_beard', 'Corte + Barba'),
            ('eyebrows', 'Cejas'),
        ),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    payment_method = forms.ChoiceField(
        choices=(
            ('cash', 'Efectivo'),
            ('card', 'Tarjeta de crédito/débito'),
        ),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Sale
        fields = ['service_type', 'payment_method'] 