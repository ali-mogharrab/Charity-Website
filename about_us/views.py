from django.shortcuts import render
from accounts.models import User

def about_us(request):
    query = User.objects.all()
    context = {'users': query}
    return render(request, 'about_us.html', context=context)

    