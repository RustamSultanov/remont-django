from django import forms
from django_registration.forms import RegistrationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .models import Comment,Competence,UserAccept,Disputs,MessegesAppeal,Adress,Guaranty,Stage,Estimate
from django.db import models
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

User = get_user_model()

class RegistrationCustomForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        fields = [
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            'password1',
            'password2'
        ]
        widgets = {
            User.USERNAME_FIELD : forms.EmailInput(attrs={'id':"email", 'class':"validate"}),
        }
    def __init__(self, *args, **kwargs):
        super(RegistrationCustomForm, self).__init__(*args, **kwargs)
        email_field = User.get_email_field_name()
        self.fields[email_field].required = False

    def save(self,commit=False):
        user = super(RegistrationCustomForm, self).save(commit=False) 
        user.email = user.username 
        user.save() 
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(attrs={'id':"email", 'class':"validate"}))

class LoginImpForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(attrs={'class':"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control"}))
        
class FeedbackForm(forms.Form):
    size = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':"Количество метров", 'class':"form-control"}))

class CommentEditForm(forms.ModelForm):

    class Meta:
        model = UserAccept
        exclude = [
                'rating'
                 ]
        # fields = [
        #         'username', 'first_name','last_name','customer_flag','implementer_flag',
        #         'init_user','implementer','files','rating','employee','another_employee','rating_competence','rating_employee'
        #          ]
        # widgets = {
        #         'comment_text': forms.Textarea(attrs={'rows' : '2'}),
        #         'customer_flag': forms.CheckboxInput(attrs={"class":"filled-in",}),
        #         'implementer_flag': forms.CheckboxInput(attrs={"class":"filled-in", }),
        #         # 'init_user': forms.Select(attrs={'disabled':"disabled", 'selected':"selected"})
        #         }

class AcceptForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [ 'accept','failure','failure_text']
        widgets = {
                'accept': forms.CheckboxInput(attrs={"class":"filled-in",}),
                'failure': forms.CheckboxInput(attrs={"class":"filled-in",}),
                'failure_text': forms.Textarea(attrs={'rows' : '2'})
                }


class CompetenceForm(forms.ModelForm):

    class Meta:
        model = Competence
        fields = [ 'competence_name']


class DisputForm(forms.ModelForm):

    class Meta:
        model = Disputs
        fields = ['text']
        widgets = {
                'text': forms.Textarea(attrs={'id' : 'textarea1','class' : 'materialize-textarea',})
                }
class MessegesAppealForm(forms.ModelForm):

    class Meta:
        model = MessegesAppeal
        fields = ['text']
        widgets = {
                'text': forms.Textarea(attrs={'placeholder' : 'Напишите сообщение','class' : 'form-control','rows' : '2'})
                }


class RegistrationEmployeeMainForm(forms.ModelForm):
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={ 'class' : 'form-control'}))
    class Meta:
        model = User
        fields =  [
                'username','first_name','last_name','email','password'
                 ]
                 
        widgets = {
                'username': forms.EmailInput(attrs={'class' : 'form-control',}),
                'first_name': forms.TextInput(attrs={'class' : 'form-control',}),
                'password' : forms.PasswordInput(attrs={'class' : 'form-control'}),
                'last_name': forms.TextInput(attrs={'class' : 'form-control',})
                }
    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже зарегистрирован')
        password_check = self.cleaned_data['password_check']
        password = self.cleaned_data['password']
        if password_check!=password:
            raise forms.ValidationError('Пароль не совпадает!')


class RegistrationEmployeeAdditionForm(forms.ModelForm):
    class Meta:
        model = UserAccept
        exclude = [
                'rating','imp','user'
                 ]
        widgets = {
                'phone_number': PhoneNumberInternationalFallbackWidget(attrs={'class' : 'form-control',}),
                'social_net': forms.URLInput(attrs={'class' : 'form-control',}),
                'date_birth': forms.DateInput(attrs={'class' : 'form-control',}),
                'gov': forms.Select(attrs={'class' : 'custom-select',}),
                'position': forms.TextInput(attrs={'class' : 'form-control',}),
                'avatar': forms.FileInput(attrs={'class' : 'user-edit-fileinput',}),

                }

class EmployeeMainForm(forms.ModelForm):
    class Meta:
        model = User
        fields =  [
                'username','first_name','last_name','email'
                 ]
                 
        widgets = {
                'username': forms.EmailInput(attrs={'class' : 'form-control',}),
                'first_name': forms.TextInput(attrs={'class' : 'form-control',}),
                'last_name': forms.TextInput(attrs={'class' : 'form-control',})
                }

class AdressForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields =  [
                'city','street','build','flat','domofone','comment'
                 ]
                 
        widgets = {
                'city': forms.TextInput(attrs={'class' : 'form-control','placeholder':"Город"}),
                'street': forms.TextInput(attrs={'class' : 'form-control','placeholder':'Улица'}),
                'build': forms.TextInput(attrs={'class' : 'form-control','placeholder':'Дом'}),
                'flat': forms.TextInput(attrs={'class' : 'form-control','placeholder':'Квартира'}),
                'domofone': forms.TextInput(attrs={'class' : 'form-control','placeholder':'Домофон'}),
                'comment': forms.Textarea(attrs={'class' : 'form-control','placeholder':'Коментарий','rows' : '2'}),
                }

class GuarantyForm(forms.ModelForm):
    class Meta:
        model = Guaranty
        fields =  [
                'name','email','phone_number','files','comment'
                 ]
                 
        widgets = {
                'name': forms.TextInput(attrs={'class' : 'form-control','placeholder':"Имя"}),
                'email': forms.EmailInput(attrs={'class' : 'form-control','placeholder':'Email'}),
                'phone_number': forms.TextInput(attrs={'type':'tel','class' : 'form-control','placeholder':'Телефон'}),
                'files': forms.FileInput(attrs={'class' : 'form-control'}),
                'comment': forms.Textarea(attrs={'class' : 'form-control','placeholder':'Коментарий','rows' : '2'}),
                }

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields =  [
                'reason'
                 ]
                 
        widgets = {
                'reason': forms.TextInput(attrs={'class' : 'form-control','placeholder':"Введите причину"}),
               
                }

class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields =  [
                'files'
                 ]
                 
        widgets = {
                
                'files': forms.FileInput(attrs={'class' : 'form-control'}),
                
                }

class EstimateFailureForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields =  [
                'reason'
                 ]
                 
        widgets = {
                'reason': forms.TextInput(attrs={'class' : 'form-control','placeholder':"Введите причину"}),
               
                }

class EmployeeAdditionForm(forms.ModelForm):
    class Meta:
        model = UserAccept
        exclude = [
                'rating','user','imp','company'
                 ]
        widgets = {
                'phone_number': PhoneNumberInternationalFallbackWidget(attrs={'class' : 'form-control',}),
                'social_net': forms.URLInput(attrs={'class' : 'form-control',}),
                'date_birth': forms.DateInput(attrs={'class' : 'form-control',}),
                'gov': forms.Select(attrs={'class' : 'custom-select',}),
                'position': forms.TextInput(attrs={'class' : 'form-control',}),
                'avatar': forms.FileInput(attrs={'class' : 'user-edit-fileinput',}),

                }
    
    
    # class Meta:
    #     model = User
    #     fields = ['username', 'password', 'first_name', 'last_name']
    #     widgets = {
    #     'username' : forms.EmailInput(attrs={'placeholder' : 'Ваша почта'}),
    #     'first_name' : forms.TextInput(attrs={'placeholder' : 'Имя', 'name' : 'Name'}),
    #     'last_name' : forms.TextInput(attrs={'placeholder' : 'Фамилия', 'name' : 'Surname'}),
    #     'password' : forms.PasswordInput(attrs={'placeholder' : 'Пароль', 'name' : 'pass'}),
    #     }

    #     error_messages = {
    #         'username': {
    #             'max_length': ("Превышена длинна"),
    #         },
    #     }

    # def clean(self):
    #     username = self.cleaned_data['username']
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('Пользователь с такой почтой уже зарегистрирован')
    #     password_check = self.cleaned_data['password_check']
    #     password = self.cleaned_data['password']
    #     if password_check!=password:
    #         raise forms.ValidationError('Пароль не совпадает!')
    #     