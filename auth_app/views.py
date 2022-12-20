from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from shopify_auth.decorators import login_required


@login_required
def home(request, *args, **kwargs):
    return render(request, "my_app/home.html")