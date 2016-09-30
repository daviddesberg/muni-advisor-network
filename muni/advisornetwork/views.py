from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegistrationForm


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return HttpResponse("Thing")
            # do things

    else:
        form = RegistrationForm()

        return render(request, 'registration.html', {'form': form})
