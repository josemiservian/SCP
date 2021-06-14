#import re
from django.http import HttpResponse

from django.views.generic import ListView, DetailView
from .models import Help


class HelpListView(ListView):
    model = Help
    template_name = 'help_list.html'

class HelpDetailView(DetailView):
    model = Help
    template_name = 'help_detail.html'