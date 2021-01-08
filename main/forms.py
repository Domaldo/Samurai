from django import forms
from main.models import Cerrajero#, Ciudad

serviceType = (('Change', 'Change'), ('Copy', 'Copy'), ('Chip', 'Chip'))
serviceObject = (('Home', 'Home'), ('Vehicle', 'Vehicle'), ('Trunk', 'Trunk'))
serviceUrgency = (('Now', 'Now'), ('Day', 'Day'), ('Month', 'Month'), ('Latest', 'Latest'))
serviceIntent = (('Compare', 'Compare'), ('Negociate', 'Negociate'), ('Decide', 'Decide'))


class CreateNewLocksmith(forms.ModelForm):
    serviceType = forms.MultipleChoiceField(choices=serviceType, widget=forms.CheckboxSelectMultiple)
    serviceObject = forms.MultipleChoiceField(choices=serviceObject, widget=forms.CheckboxSelectMultiple)
    serviceUrgency = forms.MultipleChoiceField(choices=serviceUrgency, widget=forms.CheckboxSelectMultiple)
    serviceIntent = forms.MultipleChoiceField(choices=serviceIntent, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Cerrajero
        exclude = ('user',)


class LookForLocksmith(forms.Form):
    serviceType = forms.ChoiceField(choices=serviceType)
    serviceObject = forms.ChoiceField(choices=serviceObject, )
    serviceUrgency = forms.ChoiceField(choices=serviceUrgency, )
    serviceIntent = forms.ChoiceField(choices=serviceIntent, )
    #cities = forms.ModelChoiceField(queryset=Ciudad.objects.all(), to_field_name='id', required=False)
