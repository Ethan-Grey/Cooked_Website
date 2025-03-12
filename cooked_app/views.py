from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def diet(request):
    return render(request, 'diet.html')

def holidays(request):
    return render(request, 'holidays.html')

def about_us(request):
    return render(request, 'aboutus.html')