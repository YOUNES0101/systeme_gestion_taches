from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
# Create your views here.

def home(request):
   return render (request, 'home.html')



from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth import logout # For the logout view
from django.shortcuts import redirect
from django.views.generic.edit import CreateView  # For the logout view

# --- Import your custom form --
from .forms import UserLoginForm
from .forms import UserSignUpForm



class CustomLoginView(auth_views.LoginView):
    template_name = 'login.html'

    # --- Use your custom form ---
    form_class = UserLoginForm

    redirect_authenticated_user = True

    def get_success_url(self):
        # Redirect to the 'home' page after successful login.
        # Ensure you have a URL pattern named 'home'.
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['page_title'] = 'Log In to OrgaPro' # Example of adding extra context
        return context

# Logout View (remains the same)

def custom_logout_view(request):
    logout(request)
    return redirect('home')


class SignUpView(CreateView):
    form_class = UserSignUpForm
    template_name = 'signup.html' # We will create this template next
    success_url = reverse_lazy('home') # Redirect to home page after successful signup

    help_text = None # Disable help text for the email field



    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.save() creates the user.
        user = form.save()
        login(self.request, user) # Log the user in directly after signing up
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['page_title'] = 'Create Your OrgaPro Account'
        return context

# --- LOGOUT VIEW (from previous response, for context) ---
from django.contrib.auth import logout # Already imported above

def custom_logout_view(request):
    logout(request)
    return redirect('home')