from django.shortcuts import render

def activity(request):
    return render(request, 'fitness/activity.html')

def body(request):
    return render(request, 'fitness/body.html')

def performance(request):
    return render(request, 'fitness/performance.html')

