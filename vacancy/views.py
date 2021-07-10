import logging

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View

from .forms import NewVacancyForm
from .models import Vacancy

logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


class VacancyListView(View):
    def get(self, request, *args, **kwargs):
        context = {'vacancies': Vacancy.objects.all()}
        return render(request, 'vacancy/list.html', context=context)


class NewVacancyView(View):
    def post(self, request, *args, **kwargs):
        can_submit = request.user.is_authenticated and request.user.is_staff
        if not can_submit:
            username = request.user.username
            ip = get_client_ip(request)
            logger.warning(
                'User "%s" with IP %s can not submit NewVacancy', username, ip)
            raise PermissionDenied

        form = NewVacancyForm(request.POST)
        if not form.is_valid():
            username = request.user.username
            ip = get_client_ip(request)
            logger.warning(
                'User "%s" with IP %s submitted non-valid NewVacancy', username, ip)
            return HttpResponseBadRequest('<h1>400 Bad Request</h1>')

        author = request.user
        description = form.cleaned_data['description']
        Vacancy.objects.create(author=author, description=description)
        return redirect('/home')
