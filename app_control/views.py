from django.contrib.auth import get_user, authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView


# Create your views here.
class RegistrationWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        forms = list(form_list)
        if forms.__len__() != 3 and forms[0].is_valid() and forms[1].is_valid() and forms[2].is_valid():
            raise Http404
        try:
            username = email = forms[0].cleaned_data['email']
            password = forms[1].cleaned_data['password']
            first_name = forms[2].cleaned_data['first_name']
            last_name = forms[2].cleaned_data['last_name']
        except KeyError:
            raise Http404
        # Create user
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        # Authenticate user
        login(self.request, user)
        return redirect('main')

    def get_context_data(self, form, **kwargs):
        context = super(RegistrationWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current == '0':
            # check email => context['form'].add_error()
            pass
        elif self.steps.current == '1':
            pass
        elif self.steps.current == '2':
            pass
        return context


def main_view(request):
    return render(request, 'main.html')


def logout_view(request):
    logout(request)
    return redirect('main')


def login_view(request):
    username = request.POST['login']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('dashboard')
    return redirect('main')


def dashboard_view(request):
    user = get_user(request)
    if not user.is_authenticated:
        return redirect('main')
    # Render dashboard.html
    # DISTINCT not work in sqlite.
    count_unique_last_name = 0
    list_not_unique_last_names = []

    context = {
        "count_not_unique_last_names" : count_unique_last_name,
        "list_not_unique_last_names" : list_not_unique_last_names
    }
    return render(request, 'dashboard.html', context)
