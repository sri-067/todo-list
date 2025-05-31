from django import forms
from .models import Task,Category

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'important', 'due_date', 'category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color', 'icon']
        widgets = {
            'color': forms.TextInput(attrs={'placeholder': 'e.g., primary, success, danger'}),
            'icon': forms.TextInput(attrs={'placeholder': 'e.g., bi bi-star'}),
        }



from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Used for password recovery.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email




from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Safe for normal users

class AdminProfileForm(UserChangeForm):  # For superusers only
    class Meta:
        model = User
        fields = '__all__'
