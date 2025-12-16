from django import forms

class RegistroPersonaForm(forms.Form):
    nombre = forms.CharField(
        max_length=100, 
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej. Juan'
        })
    )
    apellido = forms.CharField(
        max_length=100, 
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej. Pérez'
        })
    )
    documento = forms.CharField(
        max_length=20, 
        label="DNI / ID",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej. 12345678'
        })
    )