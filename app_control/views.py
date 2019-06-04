from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView


# Create your views here.
class RegistrationWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        return redirect('')

    def get_context_data(self, form, **kwargs):
        context = super(RegistrationWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current == 'my_step_name':
            context.update({'another_var': True})
        return context
