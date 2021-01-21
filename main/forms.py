from django import forms

from main.models import Cerrajero, Ciudad, Available, Job

serviceType = (('Cambio de Cerradura', 'Cambio de Cerradura'), ('Copia de Llave', 'Copia de Llave'), ('Llave con Chip', 'Llave con Chip'))
serviceObject = (('Casa', 'Casa'), ('Vehiculo', 'Vehiculo'), ('Cofre', 'Cofre'))

class CreateNewLocksmith(forms.ModelForm):
    serviceType = forms.MultipleChoiceField(choices=serviceType, widget=forms.CheckboxSelectMultiple)
    serviceObject = forms.MultipleChoiceField(choices=serviceObject, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Cerrajero
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(CreateNewLocksmith, self).__init__(*args, **kwargs)
        self.fields['available'].widget = forms.CheckboxSelectMultiple()
        self.fields['available'].queryset = Available.objects.all()


class LookForLocksmith(forms.Form):
    serviceType = forms.ChoiceField(choices=serviceType, label='Tipo servicio')
    serviceObject = forms.ChoiceField(choices=serviceObject, label='Objeto servicio')
    cities = forms.ModelChoiceField(queryset=Ciudad.objects.all(), to_field_name='id', required=False, label='Ciudad')


class ContractForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget, label='Fecha del Servicio')

    class Meta:
        model = Job
        exclude = ('user', 'cerrajero', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = kwargs.get('initial').get('request')
        serviceType = request.session.get('serviceType', False)
        serviceObject = request.session.get('serviceObject', False)
        self.fields['service_type'].initial = serviceType
        self.fields['service_type'].label = "Tipo de Servicio"
        self.fields['service_type'].disabled = True
        self.fields['service_object'].initial = serviceObject
        self.fields['service_object'].label = "Objeto que requiere el Servicio"
        self.fields['service_object'].disabled = True
        self.fields['take_piece'].label = "Tienes el repuesto?"
        self.fields['car_model'].label = "Modelo del Vehiculo"
        self.fields['car_year'].label = "Año del Vehiculo"
        self.fields['description'].label = "Datos adicionales"
        
        if serviceType != 'Cambio de Cerradura':
            self.fields.__delitem__('take_piece')
        if serviceObject != 'Vehiculo':
            self.fields.__delitem__('car_model')
            self.fields.__delitem__('car_year')
