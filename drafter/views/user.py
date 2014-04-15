from django.shortcuts import render, redirect
from drafter.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from drafter.models import User
from django.core.urlresolvers import reverse

"""
User-related views
"""
"""
View all users
"""
def users(request):
    users = list(User.objects.all())
    return render(request, 'drafter/users/users.html', { 'users': users })

"""
Create a new user
"""
def new_user(request):
    if request.method == 'POST': # If the form was submitted...
        form = UserCreationForm(request.POST) # Make a form bound to the POST data
        if form.is_valid():
            new_user = form.save()
            username = request.POST['username']
            password = request.POST['password1']
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return redirect(reverse('drafter.views.user', kwargs={ 'user_id': new_user.id })) 
    else:
        form = UserCreationForm() # Unbound form
    
    return render(request, 'drafter/users/new.html', { 'form': form })    

"""
View a specific user
"""
def user(request, user_id=None, username=None): # id=None, nick=None, for nick in url?
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = User.objects.get(username=username)
    return render(request, 'drafter/users/user.html', { 'viewed_user': user })
