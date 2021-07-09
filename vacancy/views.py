from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View

from .forms import NewVacancyForm
from .models import Vacancy


class VacancyListView(View):
    def get(self, request, *args, **kwargs):
        context = {'vacancies': Vacancy.objects.all()}
        return render(request, 'vacancy/list.html', context=context)


class NewVacancyView(View):
    def post(self, request, *args, **kwargs):
        can_submit = request.user.is_authenticated and request.user.is_staff
        if not can_submit:
            raise PermissionDenied

        form = NewVacancyForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('<h1>400 Bad Request</h1>')

        author = request.user
        description = form.cleaned_data['description']
        Vacancy.objects.create(author=author, description=description)
        return redirect('/home')
