from django.shortcuts import render
from django.contrib.auth import login,logout, authenticate
from find_a_volunteer_dir.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def register(request):
#There are two types of requests: GET and POST requests.
#In a GET request, data is requested from the web host machine by the client.
#In a POST request, data is submitted by the client to the web host to be processed.

    if request.method != 'POST':
        form = UserCreationForm() 
    #^this means if the request to the web hosting machine is not giving data then we create...
    #...an instance of the form with no data.
    else: 
        #this means we are being given data so we create an instance of the form with our data.
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
            login(request,authenticated_user) #The login function is defined by Django, not me.
            return HttpResponseRedirect(reverse('find_a_volunteer_dir:homepage'))
            #^After being logged in, the user is redirected to the (base) homepage.
    args={'form':form} #The form is passed as an argument to the template.
    return render(request, 'users/register.html',args)

