import logging

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View

from .forms import NewResumeForm
from .models import Resume

logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


# Create your views here.
class ResumeListView(View):
    def get(self, request, *args, **kwargs):
        context = {'resumes': Resume.objects.all()}
        return render(request, 'resume/list.html', context=context)


class NewResumeView(View):
    def post(self, request, *args, **kwargs):
        can_submit = request.user.is_authenticated and not request.user.is_staff
        if not can_submit:
            username = request.user.username
            ip = get_client_ip(request)
            logger.warning(
                'User "%s" with IP %s can not submit NewResume', username, ip)
            raise PermissionDenied

        form = NewResumeForm(request.POST)
        if not form.is_valid():
            username = request.user.username
            ip = get_client_ip(request)
            logger.warning(
                'User "%s" with IP %s submitted non-valid NewResume', username, ip)
            return HttpResponseBadRequest('<h1>400 Bad Request</h1>')

        author = request.user
        description = form.cleaned_data['description']
        Resume.objects.create(author=author, description=description)
        return redirect('/home')
