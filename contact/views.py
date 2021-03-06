from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import ContactForm
from django.contrib.messages import success, error

class ContactView(View):
    form_class = ContactForm
    template_name = "contact/contact_form.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {'form': self.form_class()}
        )

    def post(self, request):
        bound_form = ContactForm(request.POST)
        if bound_form.is_valid():
            mail_sent = True #bound_form.send_mail()
            if mail_sent:
                success(
                    request,
                    'Email successfully sent.')
                return redirect('blog_post_list')
            else:
                error(
                    request,
                    'Email not sent, Please try again.')
        return render(
            request,
            self.template_name,
            {'form': bound_form}
        )