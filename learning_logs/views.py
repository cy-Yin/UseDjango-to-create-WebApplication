from django.shortcuts import render

# Create your views here.
def index(request):
    '''main page of the learning log project'''
    return render(request, 'learning_logs/index.html')