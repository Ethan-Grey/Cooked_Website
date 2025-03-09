from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def diet(request):
    return render(request, 'diet.html')

def holidays(request):
    return render(request, 'holidays.html')