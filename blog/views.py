from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def others(request):
    return render(request, 'nav.html')
