from django import forms
from django.core.exceptions import ValidationError

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
        label="DNI (8 dígitos)",
        help_text="Ingresa solo números.",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ej. 12345678',
            'pattern': '[0-9]*', 
            'inputmode': 'numeric'
        })
    )

    def clean_documento(self):
        """
        MEJORA: Validación específica para DNI.
        Verifica que el campo contenga solo dígitos y tenga una longitud exacta de 8.
        """
        data = self.cleaned_data['documento']
        
        # Verificar que sean solo números
        if not data.isdigit():
            raise ValidationError("El documento debe contener solo números.")
        
        # Verificar longitud (ejemplo para DNI peruano: 8 dígitos)
        if len(data) != 8:
            raise ValidationError("El DNI debe tener exactamente 8 dígitos.")
            
        return data