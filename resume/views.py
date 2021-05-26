from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views import View

from .forms import NewResumeForm
from .models import Resume


# Create your views here.
class ResumeListView(View):
    def get(self, request, *args, **kwargs):
        context = {'resumes': Resume.objects.all()}
        return render(request, 'resume/list.html', context=context)


class NewResumeView(View):
    def post(self, request, *args, **kwargs):
        can_submit = request.user.is_authenticated and not request.user.is_staff
        if not can_submit:
            raise PermissionDenied

        form = NewResumeForm(request.POST)
        if not form.is_valid():
            return redirect('/home')

        author = request.user
        description = form.cleaned_data['description']
        Resume.objects.create(author=author, description=description)
        return redirect('/home')
