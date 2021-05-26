from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

from resume.forms import NewResumeForm
from vacancy.forms import NewVacancyForm


# Create your views here.
class MainView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'is_authenticated': request.user.is_authenticated,
            'username': request.user.username,
        }
        return render(request, 'main.html', context=context)


class UserSignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signup.html'


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = NewVacancyForm() if request.user.is_staff else NewResumeForm()
        context = {
            'form': form,
            'is_authenticated': request.user.is_authenticated,
            'is_staff': request.user.is_staff,
            'username': request.user.username,
        }
        return render(request, 'home.html', context=context)
