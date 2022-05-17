from django.views.generic import CreateView
from .models import Contact
from .forms import ContactForm
# Create your views here.


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = "/"