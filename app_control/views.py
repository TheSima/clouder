from django.contrib.auth import get_user, authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from django.db.models import Count


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
        return redirect('dashboard')

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
    context = {
        "count_not_unique_last_names" : get_count_not_unique_last_name(),
        "list_not_unique_last_names" : get_list_not_unique_last_names()
    }
    return render(request, 'dashboard.html', context)


def get_list_not_unique_last_names():
    field_last_name = 'last_name'
    qs = User.objects.values(field_last_name).order_by(field_last_name).annotate(count=Count(field_last_name))\
        .filter(count__gt=1).values('first_name', field_last_name, 'email', 'is_active')
    qs_not_unique_last_names = User.objects.values(field_last_name).order_by(field_last_name).annotate(count=Count(field_last_name)) \
        .filter(count__gt=1).values(field_last_name)
    res = []
    for last_name in (v[field_last_name] for v in qs_not_unique_last_names):
        res.extend(
            ("{} {} - {} is active : {}".format(v.first_name, v.last_name,v.email, v.is_active)
             for v in User.objects.filter(last_name=last_name))
        )
    return res


def get_count_not_unique_last_name():
    field_last_name = 'last_name'
    return User.objects.values(field_last_name).order_by(field_last_name).annotate(count=Count(field_last_name))\
        .filter(count__gt=1).count()