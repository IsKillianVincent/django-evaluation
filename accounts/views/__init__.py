from .auth import *
from .dashboard import *
from .profile import *

from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to the accounts section.")