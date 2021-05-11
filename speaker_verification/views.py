from django.shortcuts import render
from django.contrib import messages
from .forms import UserForm
import requests


# Create your views here.
def index(request):
    if request.method == 'POST':
        f = UserForm(request.POST, request.FILES)
        if f.is_valid():
            data = requests.post('http://127.0.0.1:8000/speaker_verification/speaker-verify', files=request.FILES)
            messages.success(request, f'{data}')
        else:
            messages.error(request, "Failed. Please check again the information")
            return render(request, "speaker_verification/index.html", {
        'form': f
    })

    return render(request, "speaker_verification/index.html", {
        'form': UserForm()
    })