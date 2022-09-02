from django.shortcuts import render
from extraction.lib.status_utils import get_last_submissions

def status(request):
    return render(request, 
        'status.html', 
        {'submissions': get_last_submissions(10)}
    )
