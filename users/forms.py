# users/forms.py
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can customize form widgets here if needed, for example:
        self.fields['username'].widget.attrs.update(
            {'class': 'appearance-none block w-full px-3 py-2 border border-border-gray rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-brand-blue focus:border-brand-blue sm:text-sm',
             'placeholder': 'Email'} # Added placeholder directly
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'appearance-none block w-full px-3 py-2 border border-border-gray rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-brand-blue focus:border-brand-blue sm:text-sm',
             'placeholder': 'Password'} # Added placeholder directly
        )





# class UserSignUpForm(UserCreationForm):

# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User # Import the User model

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Enter a valid email address.'
    )
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta(UserCreationForm.Meta):
        model = User # Specify the model to use
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')
        # UserCreationForm.Meta.fields typically includes 'username'
        # Password fields are handled by UserCreationForm itself

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Common Tailwind classes for form inputs
        input_classes = 'appearance-none block w-full px-3 py-2 border border-border-gray rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-brand-blue focus:border-brand-blue sm:text-sm'

        # Apply classes and placeholders
        self.fields['username'].widget.attrs.update({
            'class': input_classes,
            'placeholder': 'Choose a username',
            'autofocus': True
        })
        self.fields['email'].widget.attrs.update({
            'class': input_classes,
            'placeholder': 'your@email.com'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': input_classes,
            'placeholder': 'Your first name (Optional)'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': input_classes,
            'placeholder': 'Your last name (Optional)'
        })

        help_text= {
            'username': None,  # Remove the default help text
            'email': None,
            'first_name': None,
            'last_name': None,
        }

        # Password fields are a bit different due to PasswordInput widget
        # and password confirmation handled by UserCreationForm
        self.fields['password1'].label = "Password"
        self.fields['password1'].widget.attrs.update({
            'class': input_classes,
            'placeholder': 'Create a password'
        })
        self.fields['password2'].label = "Confirm password"
        self.fields['password2'].widget.attrs.update({
            'class': input_classes,
            'placeholder': 'Confirm your password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "") # Use .get for optional fields
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
        return user