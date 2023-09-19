from django import forms
from .models import GroupChat, Orders, Product

class RegisterForm(forms.Form):
    fullname = forms.CharField(label='Full Name', max_length=100)
    phone = forms.CharField(label='Phone Number', max_length=20)
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class MemberForm(forms.ModelForm):
    # participants = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    
    class Meta:
        model = GroupChat
        fields = ['participants']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ('__all__')
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
