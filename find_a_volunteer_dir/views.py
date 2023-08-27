from django.shortcuts import render
#render is defined by Django and is used to "render" templates 

from .models import image_upload, volunteer_profile,organisation_profile, matched_organisations, accepted_organisations, verification_details
#These models from the models.py file which is located in the same directory as this file are used in various views to ...
#... create/edit/delete/query objects of these models.

from django.shortcuts import redirect
#many views and decorators use Django's redirect function to redirect users to other pages based on certain events.

from functools import wraps
#Wraps is a crucial part of the decorators.

from django.http import HttpResponseRedirect
#HttpResponseRedirect is a more flexible version of redirect with more or less the same purpose.

from .forms import upload_image_form, volunteer_profile_form, organisation_profile_form, accept_reject_form, captcha_verification_form
#These forms from the forms.py file located in the same directory as this file are used in various views.

from users.models import CustomUser
#Various views query objects of my CustomUser model. This model cannot be imported together with the ones in line 4 as it is located in...
#... the models.py file in the users app whereas the other models are located in the models.py file in the find_a_volunteer_dir app...
#...which is the app that this file is also inside.

import requests
#Every view takes request a parameter. The request parameter is a HttpRequest object which contains data about the request.

from .my_extra_modules import (split_string, date_time_format_converter, latest_tweet, list_contains_element, merge, 
      dictionary_to_key_value_list, merge_sort_list_of_key_value_pairs_by_value, apply_filter, transpose, concatenate_4_image_arrays, 
      letter_modification_1, letter_modification_2, letter_modification_3)
#These functions from the my_extra_modules.py are used in various views.

import random #This is used in some views


 # this is so I can pass my user to the homepage template in the homepage view.
# Create your views here.

#The function the decorator "wraps" around is a parameter to the decorator function.
#Hence making decorators HIGHER ORDER FUNCTIONS. 
def must_be_logged_in(function): 
      @wraps(function)
      def wrap(request, *args, **kwargs):            
            if request.user.is_authenticated: 
            #^request.user.is_authenticated returns True if the user is authenticated (i.e logged in)                 
                  return function(request, *args, **kwargs)
            else:
                  return HttpResponseRedirect('/error/')
      return wrap

      
def volunteers_only(function):
      @wraps(function)
      def wrap(request, *args, **kwargs):
            if request.user.is_authenticated:
                  user_type = request.user.user_type
                  #The user type has to be checked after making sure...
                  #...the user is_authenticated (logged in) or else...
                  #...an error will be thrown if the user type...
                  #...of a non-logged in user is queried.
                  if user_type == 'volunteer':
                        return function(request, *args, **kwargs)
                  else:
                        #If either [if condition] is not satisifed...
                        #...the user is redirected to the error page.
                        return HttpResponseRedirect('/error/')
            else:
                  return HttpResponseRedirect('/error/')
      return wrap


def volunteer_with_one_volunteer_profile_only(function):
      @wraps(function)
      def wrap(request, *args, **kwargs):

            if request.user.is_authenticated:
                  
                  user_type = request.user.user_type
                  if user_type == 'volunteer':
                        num_volunteer_profiles=volunteer_profile.objects.filter(owner_id=request.user.id).count()
                        #^This line gets the number of volunteer_profile objects associated with the user ...
                        #...requesting to access the view this decorator "wraps" around.
                        if num_volunteer_profiles==1:
                              return function(request, *args, **kwargs)
                        else:
                              #If any of the 3 [if conditions] are not satisifed, the user is redirected to the error page.
                              return HttpResponseRedirect('/error/')
                  else:
                        return HttpResponseRedirect('/error/')
            else:
                  return HttpResponseRedirect('/error/')

      return wrap
      

def organisations_only(function):
      @wraps(function)
      def wrap(request, *args, **kwargs):

            if request.user.is_authenticated:
                  user_type = request.user.user_type
                  if user_type == 'organisation':
                        return function(request, *args, **kwargs)
                  else:
                        return HttpResponseRedirect('/error/')
            else:
                  return HttpResponseRedirect('/error/')
      return wrap


def organisation_with_one_organisation_profile_only(function):
      @wraps(function)
      def wrap(request, *args, **kwargs):

            if request.user.is_authenticated:
                  
                  user_type = request.user.user_type
                  if user_type == 'organisation':
                        num_organisation_profiles=organisation_profile.objects.filter(owner_id=request.user.id).count()
                        if num_organisation_profiles==1:
                              return function(request, *args, **kwargs)
                        else:
                              return HttpResponseRedirect('/error/')
                  else:
                        return HttpResponseRedirect('/error/')
            else:
                  return HttpResponseRedirect('/error/')

      return wrap

#^^^^The custom decorators



def homepage(request): 

      if request.user.is_authenticated: 
      #^before filtering the verification_details objects, we have to make sure the user is_authenticated.
            if verification_details.objects.filter(owner_id=request.user.id,verified="True").count()>0:
            #The condition ^ means the user has a verification_details object where the verified field...
            #... ==True which therefore means the user is verified.      
                  verified=True 
            else:
                  verified=False
      else:                   
            verified=False
            #^If the user is not even logged in then they are not verified. 

      #The below section uses various functions (which use the twitter API with my twitter account as the PARAMETER)...
      #...from my my_extra_modules.py file.
      tweet_and_date_created=latest_tweet(1475518586663878662)
      #^This gets the latest tweet from the twitter account with that (1475...) id. This account is my...
      #...volunteering promotion twitter account.
      twitter_user = "@arun_hussain" #this is the account the id above corresponds to.
      tweet=tweet_and_date_created[0]
      #^tweet_and_date_created[0] is the actual text contents of the latest tweet from my account.

      formatted_date_created=date_time_format_converter(tweet_and_date_created[1])
      #tweet_and_date_created[1] is the date_and_time of the latest tweet and is...
      #...formatted in the way that twitter formats the information their api returns.
      #This formatting is not easily readable so I use my own formatting converter function...
      #...designed for the particular way the date_time infomation returned by the api is formatted.

      args={'tweet':tweet , 'date_created':formatted_date_created , 'twitter_user':twitter_user,'verified':verified}
      #^these are the arguments my template will need and use.
      return render(request, 'find_a_volunteer_dir/homepage.html',args)


      
def error_page(request):
      return render(request,'find_a_volunteer_dir/error_page.html')


@volunteers_only
def volunteer_homepage(request):

      #The block below is needed to get the variable necessary for me to control...
      #...when the accept-reject page link appears! Only if num_matched_remai... ...
      #... is >0 will the accept-reject link appear.  
      num_matches_remaining_to_be_decided_on=0 
      for o in matched_organisations.objects.filter(volunteer_owner_id=request.user.id):
            num_matches_remaining_to_be_decided_on+=1 
            for org in accepted_organisations.objects.filter(volunteer_owner_id=request.user.id):
                if o.id_of_matched_organisation == org.id_of_accepted_organisation:
                    num_matches_remaining_to_be_decided_on -= 1
      #The way this above code works is: For each match the volunteer user has, ...
      #... +1 is added to the variable. THEN, if that match with its particular...
      #... volunteer and organisation id also appears as an accepted_organisation...
      #... object then -1 is taken from the variable as this implies that that match...
      #... has already been decided on.


      num_accepted=accepted_organisations.objects.filter(volunteer_owner_id=request.user.id,decision="Accept").count() 
      #The num_accepted variable is needed for me to control when the view_accepted_organisations page link...
      #...appears.
                                  
      num = volunteer_profile.objects.filter(owner_id=request.user.id).count()
      #^This is number of volunteer_profiles the user has.
      num_matches=matched_organisations.objects.filter(volunteer_owner_id=request.user.id).count()
      #This is the number of matches (regardless of if they have been decided on or not)...
      #...that the user has.

      args={'num_profiles':num,'num_matches':num_matches,
            'num_matches_remaining_to_be_decided_on':num_matches_remaining_to_be_decided_on,'num_accepted':num_accepted,
      }#^All these arguments have to be passed to the template to determine which links and which text...
      #... is displayed!
      return render(request, 'find_a_volunteer_dir/volunteer_homepage.html',args)

@volunteers_only
def new_volunteer_profile(request):
      if volunteer_profile.objects.filter(owner_id=request.user.id).count()==0:
      #the above checks the number of volunteer_profiles a user has.
      #If the user doesn't have 0 volunteer_profiles then they aren't...
      #... allowed to access this page and are redirected to the error page.
            
            if request.method != 'POST':
            #^If the request is a 'GET' one (i.e not 'POST')...
            #...then a blank instance of the form is created.
                  form=volunteer_profile_form()
            else:
            #If the request is a 'POST' one, this branch is run.
            #An instance of the form is created and filled with...
            #...the user's POST data in the line below.
                  form=volunteer_profile_form(data=request.POST)
                  if form.is_valid():
                        new_volunteer_profile=form.save(commit=False) 
                        #^commit=False allows me to populate some fields of the object...
                        #...myself without using the form's inputs before...
                        #...the new object is properly saved to the database.

                        new_volunteer_profile.owner_id=CustomUser.objects.get(id=request.user.id) 
                        #^Here I fill the owner_id field of the new volunteer_profile object...
                        #...as the form does not take an input for this field because...
                        #...the user doesn't get to decide the owner_id of their profile!
                        #The reason the field is filled with a CustomUser object and not an...
                        #...integer is because in the volunteer_profle model, the owner_id...
                        #...field is defined as a OneToOne field with the CustomUser model.
                                           
                        new_volunteer_profile.save()
                        #^This saves the object to the database.
                        return redirect('/volunteer/homepage/')
                        #^The user is redirected to the volunteer homepage after the object is saved.
            args={'form':form}
            return render(request, 'find_a_volunteer_dir/new_volunteer_profile.html',args)
      else:
            return redirect('/error/')



@volunteer_with_one_volunteer_profile_only
def view_volunteer_profile(request):
      user_volunteer_profile=volunteer_profile.objects.filter(owner_id=request.user.id).get()
      #the above line gets the volunteer_profile of the current user.
      args={'volunteer_profile':user_volunteer_profile}
      #^This volunteer profile is passed to the template so that the template can access and...
      #...dispaly all of its attributes.
      return render(request, 'find_a_volunteer_dir/view_volunteer_profile.html',args)
      
            

@volunteer_with_one_volunteer_profile_only
def edit_volunteer_profile(request):
      user_volunteer_profile=volunteer_profile.objects.filter(owner_id=request.user.id).get()
      #This gets the volunteer profile of the user which they are trying to edit.
      if request.method != 'POST':
      #This branch runs if it's they're initial GET request and they're NOT saving the updated form.
            form=volunteer_profile_form(instance=user_volunteer_profile)
            #An instance of the form is created and pre-filled with the...
            #...attributes of their current volunteer profile.

      else:
      #This branch runs if POST data is submitted so here I process the update to the form.
            form=volunteer_profile_form(instance=user_volunteer_profile, data=request.POST)
            if form.is_valid:
                  form.save()
                  #The updated form is saved so the user's volunteer_profile object is...
                  #...updated in the database based on the user's new inputs.
                  return redirect('/volunteer/homepage/')
      args={'form':form}
      return render(request, 'find_a_volunteer_dir/edit_volunteer_profile.html', args)



@volunteer_with_one_volunteer_profile_only
def match_volunteer_with_organisations(request):
      volunteer=volunteer_profile.objects.filter(owner_id=request.user.id).get()
      #^I first get the volunteer profile of the user making the request to the web host machine.

      #This list below will store the preffered_activities details from the user's volunteer profile.
      volunteer_desired_activities=[] 
      volunteer_desired_activities.append(volunteer.first_preferred_activity)
      if volunteer.second_preferred_activity is None: 
            pass
            #The second and third preferred activity are optional fields so before querying...
            #...them, I have to first make sure they exist (i.e are not None).
            #If I query the fields and they are None, an error will be thrown!
      else:
            volunteer_desired_activities.append(volunteer.second_preferred_activity)
      if volunteer.third_preferred_activity is None:
            pass
      else:
            volunteer_desired_activities.append(volunteer.third_preferred_activity)

      volunteer_day_availability=[volunteer.monday_availability,volunteer.tuesday_availability,
                                  volunteer.wednesday_availability,volunteer.thursday_availability,
                                  volunteer.friday_availability,volunteer.saturday_availability,
                                  volunteer.sunday_availability] 

      matches_dict={}
      matched_organisations.objects.filter(volunteer_owner_id=volunteer.owner_id_id).delete()
      #^When a user requests this page, they are generating their matches. If this is not the...
      #... first time they are generating their matches then they will already have matched_organisations...
      #... objects in the database. To prevent a user repeatedly generating matches and flooding the...
      #...database with matches, in the line above these comments, I delete all matches associated...
      #...with the volunteer accessing this page.

      #Now I go through every organisation profile to see if it is a match.
      for organisation in organisation_profile.objects.all():
            organisation_day_availability=[organisation.monday_availability,organisation.tuesday_availability,
                                           organisation.wednesday_availability,organisation.thursday_availability,
                                           organisation.friday_availability,organisation.saturday_availability,
                                           organisation.sunday_availability]            
            availability_intersections = 0

            #For an organsation to be considered a match, the 3 booleans below must be true.
            bool_availability_intersection=False 
            bool_activity_intersection=False
            bool_age_intersection=False

            #Below is where I determine both if there is an availability_intersection and how many there are.
            for index in range(0,6): #the index allows each day to be each of the 7 day_availabilities...
                                     # to be iterated through. 
                  if ((volunteer_day_availability[index]==organisation_day_availability[index] and 
                       volunteer_day_availability!="None")
                       or (volunteer_day_availability[index]=="All day" and organisation_day_availability != "None")
                       or (organisation_day_availability[index]=="All day" and volunteer_day_availability != "None")):
                  #^Given that each day_availability can = Morning, afternoon, evening, all day or none, these if...
                  #...statements will successfully identify if there is an availability_intersection for a certain day. 

                        availability_intersections=availability_intersections+1
                        #^The number of intersections is also counted as this will affect compatibility score.
                        bool_availability_intersection=True
                        
            
            if bool_availability_intersection:
                  #It is only worth checking for an age intersection if there is an availability intersection.
                  if organisation.desired_age_lower_bound<=volunteer.age<=organisation.desired_age_upper_bound:
                        bool_age_intersection=True #^This determines if there is an age intersection.

                        organisation_available_activities=[]
                        organisation_available_activities.append(organisation.available_activity_1)
                        if organisation.available_activity_2 is None:
                              #I have to make sure the optional fields are not empty before I...
                              #... try to add them to a list.
                              pass
                        else: 
                              organisation_available_activities.append(organisation.available_activity_2)
                        if organisation.available_activity_3 is None:
                              pass
                        else:
                              organisation_available_activities.append(organisation.available_activity_3)
                        
                        compatibility_score=0 

                        for index in range(0,len(volunteer_desired_activities)):
                              if list_contains_element(organisation_available_activities,volunteer_desired_activities[index]):
                                    compatibility_score=compatibility_score+(3-index) 
                                    #So if the first element of ...
                                    #volunteer_desired_activities (the volunteer's most preferred activity)...
                                    #is in the organisation's available activities then (3-0)= 3 points are given. 
                                    #If the volunteer's second most preferred activity is in the organisation's ...
                                    # ...available ones then (3-1) = 2 points are given.                        
                                    #If the volunteer's third most is then (3-2)=1 point is given.
                                    bool_activity_intersection=True
                        compatibility_score=compatibility_score+availability_intersections
                        #The number of time availability_intersections count towards the score.
                        
                  else:
                        pass
            else:
                  pass

            if bool_availability_intersection==True and bool_age_intersection==True and bool_activity_intersection==True:
                  matches_dict[organisation.owner_id_id]=compatibility_score
                  #^If the 3 bools are true then the match is added to the dictionary of matches for this volunteer.
                  #Each pair in the dictionary is the id of the organisation and its compatibility score.
                 
                 
                  save_match = matched_organisations.objects.create(volunteer_owner_id=volunteer.owner_id_id,
                                                                    id_of_matched_organisation=organisation.owner_id_id, 
                                                                    organisation_compatibility_score=compatibility_score)
                  save_match.save()#this creates a matched_organisations onject for each matched organisation.
                  
      #When the dictionary of matches is passed to the template, it must be sorted by compatibility score...
      #...in descending order with the pair with the highest compatibility score in the first index.

      #first I will convert the dictionary {'owner_id_id':compatibility_score , '___':___ , .... }  ...
      #...into a list of lists of form [('owner_id_id',compatibility_score) , ('...',...) , ].
      key_value_list_of_matches=dictionary_to_key_value_list(matches_dict)
      #^This uses one of the function I've defined in my_extra_modules.py

      sorted_matches_key_value_list = merge_sort_list_of_key_value_pairs_by_value(key_value_list_of_matches)
      #^Now that my dictionary is a list of lists where the sublists are key-value pairs, I can sort the list...
      #...and change the indexes of the sublists by the value (compatibility score) of each pair.

      #the list below will have the names and verified bool of the organisations which the organisation ids...
      #... in the sorted list from the code above correspond to. The indexes of the sorted list and the list below...
      # ...will match up so that elements of both lists with the same index contain info about the same organisation. 
      names_and_verifications_of_organisations_list=[]
      for i in range(0,len(sorted_matches_key_value_list)):
            name=organisation_profile.objects.filter(owner_id_id=sorted_matches_key_value_list[i][0]).get().name
            if verification_details.objects.filter(owner_id=sorted_matches_key_value_list[i][0], verified="True").count()==0:
                  verified="[Not verified]"
            else:
                  verified="[Verified]"
            to_be_appended=[name,verified]
            names_and_verifications_of_organisations_list.append(to_be_appended)
            #This list has a list appended to it so it is also a list of lists.
            
      args={'matches_list':sorted_matches_key_value_list , 
            'names_and_verifications_of_organisations':names_and_verifications_of_organisations_list}
      return render(request,'find_a_volunteer_dir/matches_with_organisations.html',args)



@volunteer_with_one_volunteer_profile_only 
def view_matched_organisation_profile(request,organisation_id):

      #When this page/view is requested, an organisation_id is passed...
      #... as a parameter. First, I need to check that there actually...
      #...exists an organisation with the organisation_id passed...
      #...and that that organisation, if it does exist, has an organisation...
      #...profile or else there is nothing to view!
      #If there is not an organisation with that organisation id...
      #... which also has an organisation profile, the client is...
      #...redirected to the error page.
      org_exists=False
      for o in organisation_profile.objects.all(): 
            if o.owner_id_id==organisation_id:
                  #Because of the one to one relationship between organisation...
                  #...users and the organisation_profile, if this condition...
                  #... is true, there exists an organisation with the ...
                  #...organisation_id parameter passed and that organisation...
                  #...has an organisation profile.  
                  org_exists=True

      if org_exists:
            

            volunteer_has_access=False
            for match in matched_organisations.objects.filter(volunteer_owner_id=request.user.id):
                  if match.id_of_matched_organisation == organisation_id:
                        volunteer_has_access=True
            #^Only volunteers who have the organisation they're trying to view as one of their...
            #...matches are allowed to see that organisation's profile, ...
            #...hence why the block above is needed.

            if volunteer_has_access:
                  if verification_details.objects.filter(owner_id=organisation_id, verified="True").count()==0:
                        verified="[Not verified]"
                  else:
                        verified="[Verified]"
                  #the below gets the organisation_profile details of the...
                  #...organisation with the organisation_id passed from the url.      
                  organisation_details=organisation_profile.objects.get(owner_id=organisation_id)
                  args={"organisation_profile":organisation_details,"verified":verified}
                  #^These are the arguments the template requires.
                  return render(request,'find_a_volunteer_dir/view_matched_organisation_profile.html' ,args)
            else:
                  return redirect('/error/')
      else:
            return redirect('/error/')

      
@volunteer_with_one_volunteer_profile_only 
def accept_or_reject_matches(request):
      
      #A user can only access this page if they have >0 matches which haven't been...
      #...decided on yet so the below block of code gets the number of matches...
      #...which haven't yet been decided on.
      num_matches_remaining_to_be_decided_on=0 
      for o in matched_organisations.objects.filter(volunteer_owner_id=request.user.id):
            num_matches_remaining_to_be_decided_on+=1                                       
            for org in accepted_organisations.objects.filter(volunteer_owner_id=request.user.id):
                if o.id_of_matched_organisation == org.id_of_accepted_organisation:
                    num_matches_remaining_to_be_decided_on -= 1
      #^ What this code does is for each match it adds one to the variable but it then ...
      #...subtracts one from the variable if that match appears in the accepted_organisations...
      #... objects as well. 

      #This if block is to make sure a user can't access this page with no matches!!!
      if num_matches_remaining_to_be_decided_on>0:
            num_matches=matched_organisations.objects.filter(volunteer_owner_id=request.user.id).count()
            if num_matches==0:
                  return redirect('/error/')
            else:
                  user_volunteer_profile=volunteer_profile.objects.filter(owner_id=request.user.id).get()

                  if request.method != 'POST':
                        #^ i.e If it's the user's initial request and... 
                        #...they're NOT saving the inputs to the form, ...
                        #...then an instance of the form is created with the user passed...
                        #...as the parameter. This is because the form needs the user ... 
                        #... passed to is as it needs to dynamically generate the choice field!
                        form=accept_reject_form(user=request.user)

                  else:#post data is submitted so process form inputs.
                        form=accept_reject_form(data=request.POST, user=request.user)
                        if form.is_valid:
                              new_accepted_organisation=form.save(commit=False)

                              new_accepted_organisation.volunteer_owner_id=request.user.id
                              #The volunteer_owner_id field is filled here as the form doesn't ...
                              #...take input for that field.
                              new_accepted_organisation.save()
                              return redirect('/volunteer/homepage/')

                  args={'form':form}
                  return render(request, 'find_a_volunteer_dir/accept_or_reject_matches.html',args)
      
      else:
            return redirect('/error/')


@volunteer_with_one_volunteer_profile_only 
def view_accepted_organisations(request):

      num_accepted_orgs=accepted_organisations.objects.filter(volunteer_owner_id=request.user.id,decision="Accept").count()
      if num_accepted_orgs>0:      
      #^This conditions is necessary to access the functionality of this page.

            #These 4 lists below are needed to pass the information...
            #...about the volunteer user's accepted organisations to ...
            #... the template.
            names=[]
            id_list=[]
            compatibility_score_list=[]
            verified_list=[]
            
            for org in accepted_organisations.objects.filter(volunteer_owner_id=request.user.id, decision="Accept"):
            #^In the above filter clause, objects have to satisfy both the 2 conditions.
                  org_profile=organisation_profile.objects.filter(owner_id_id=org.id_of_accepted_organisation).get()
                  names.append(org_profile.name)
                  id_list.append(org.id_of_accepted_organisation)
                  org_in_matches=matched_organisations.objects.filter(volunteer_owner_id=request.user.id,
                        id_of_matched_organisation=org.id_of_accepted_organisation).get()
                  compatibility_score_list.append(org_in_matches.organisation_compatibility_score)
                  if verification_details.objects.filter(owner_id=org.id_of_accepted_organisation, verified="True").count()==0:
                        verified_list.append('[Not verified]')
                  else:
                        verified_list.append('[Verified]')
            #^The above for loop fills the 4 lists with a particular value for each of the user's accepted organisations.    

            #The block of code below combines the 4 lists into one lists of lists where each sublist has 4 elements, ...
            #...one from each of the separate lists.      
            name_id_compatibility_verified_list=[]
            for count in range(0,len(names)):
                  name_id_compatibility_verified_list.append((names[count], id_list[count],
                        compatibility_score_list[count], verified_list[count]))

            args={"name_id_compatibility_verified_list":name_id_compatibility_verified_list}
            return render(request, 'find_a_volunteer_dir/view_accepted_organisations.html',args)
      else:
            return redirect('/error/')


@organisations_only
def organisation_homepage(request):
      
      num_volunteers_who_accepted=accepted_organisations.objects.filter(
            id_of_accepted_organisation=request.user.id,decision="Accept").count()     
      num = organisation_profile.objects.filter(owner_id=request.user.id).count()
      args={'num_profiles':num,'num_volunteers_who_accepted':num_volunteers_who_accepted}
      #These are the only arguments which need to be passed to the template as they are...
      #... the only variables which what the template displays depends on.
      return render(request, 'find_a_volunteer_dir/organisation_homepage.html',args)

@organisations_only
def new_organisation_profile(request):
      if organisation_profile.objects.filter(owner_id=request.user.id).count()==0:
      #The above checks that the user actually has an organisation profile to edit.
      #If they don't, they are redirected to the error page.
      
            if request.method != 'POST':
                  form=organisation_profile_form()
            #^ A blank instance of the form is created if the request is not a "POST" one.

            else:
                  form=organisation_profile_form(data=request.POST)
                  if form.is_valid():
                        new_organisation_profile=form.save(commit=False)
                        new_organisation_profile.owner_id=CustomUser.objects.get(id=request.user.id) 
                        #Here the owner_id field of the new_organisation_profile object is...
                        #... filled as the form doesn't take input for this field.
                        #The reason that the field is filled with a custom user object and...
                        #... not an integer is because in the organisation_profile model,...
                        #...the owner_id field is defined as a OneToOne field with the CustomUser model.                  
                        new_organisation_profile.save()
                        return redirect('/organisation/homepage/')
            args={'form':form}
            return render(request, 'find_a_volunteer_dir/new_organisation_profile.html',args)
      else:
            return redirect('/error/')


@organisation_with_one_organisation_profile_only
def view_organisation_profile(request):      
      user_organisation_profile=organisation_profile.objects.filter(owner_id=request.user.id).get()
      #The above line gets the volunteer_profile of the current user and that is the only...
      #...argument necessary to be passed to the template.
      args={'organisation_profile':user_organisation_profile}
      return render(request, 'find_a_volunteer_dir/view_organisation_profile.html',args)
     

@organisation_with_one_organisation_profile_only
def edit_organisation_profile(request):    
      user_organisation_profile=organisation_profile.objects.filter(owner_id=request.user.id).get()
      #^This gets the organisation_profile of the user making the request.
      if request.method != 'POST':
            form=organisation_profile_form(instance=user_organisation_profile)
            #^An instance of the form is created and pre-filled with the details of the...
            #...user's organisation profile.

      else:
            form=organisation_profile_form(instance=user_organisation_profile, data=request.POST)
            if form.is_valid:
                  form.save()
                  return redirect('/organisation/homepage/')
            #^If POST data is submitted, then the inputs are processed and the changes are saved...
            #... and the object is updated in the database.

      args={'form':form}
      return render(request, 'find_a_volunteer_dir/edit_organisation_profile.html',args)


@organisation_with_one_organisation_profile_only      
def view_volunteers_who_have_accepted(request):

      num_volunteers_who_accepted=accepted_organisations.objects.filter(id_of_accepted_organisation=request.user.id,
      decision="Accept").count()
      if num_volunteers_who_accepted>0:      
      #This condition is necessary to access the functionality of this page.

            #These 4 lists are needed to pass the necessary information about which volunteers accepted the organisation...
            #...to the template.
            names=[]
            id_of_volunteers=[]
            compatibility_score=[]
            verified_list=[]

            for org in accepted_organisations.objects.filter(id_of_accepted_organisation=request.user.id, decision="Accept"):
            #In the above filter clause, objects have to satisfy both the 2 conditions.      
                  volunteer=volunteer_profile.objects.filter(owner_id_id=org.volunteer_owner_id_id).get()
                  names.append(volunteer.name)
                  id_of_volunteers.append(org.volunteer_owner_id_id)
                  corresponding_match = matched_organisations.objects.filter(volunteer_owner_id=org.volunteer_owner_id_id,
                  id_of_matched_organisation=request.user.id).get()
                  compatibility_score.append(corresponding_match.organisation_compatibility_score)
                  if verification_details.objects.filter(owner_id=org.volunteer_owner_id_id, verified="True").count()==0:
                        verified="[Not verified]"
                  else:
                        verified="[Verified]"
                  verified_list.append(verified)
            #The above for loop fills all the 4 lists with a particular value for each of the user's accepted organisations.

            #Below, the 4 lists are combined into a single list of lists.
            name_id_compatibility_verified_list=[]
            for count in range(0,len(names)):
                  name_id_compatibility_verified_list.append((names[count], id_of_volunteers[count], compatibility_score[count], 
                  verified_list[count]))

            args={'name_id_compatibility_verified_list':name_id_compatibility_verified_list}
            return render(request, 'find_a_volunteer_dir/view_volunteers_who_have_accepted.html',args)            
      else:
            return redirect('/error/')


@organisation_with_one_organisation_profile_only
def view_accepted_volunteer_profile(request,volunteer_id):

      #When this page/view is requested, a volunteer_id is passed.
      #I have to first make sure there exists a volunteer with...
      #that id and that that volunteer has a volunteer profile.
      #The block of code below does that.
      volunteer_exists=False 
      for volunteer in volunteer_profile.objects.all():
            if volunteer.owner_id_id==volunteer_id:
                  volunteer_exists=True

      #Only organisations who have been accepted by the volunteer can view...
      #...the volunteer's profile which is why the block below is needed.
      if volunteer_exists:
            org_has_access=False
            for accepted in accepted_organisations.objects.filter(id_of_accepted_organisation=request.user.id,decision="Accept"):
                  if accepted.volunteer_owner_id_id == volunteer_id:
                        org_has_access=True 

            if org_has_access:
                  #The line below gets the volunteers profile details. The details can be accessed by...
                  #... doing volunteer_details.[field_name]
                  volunteer_details=volunteer_profile.objects.get(owner_id=volunteer_id)
                  if verification_details.objects.filter(owner_id=volunteer_id, verified="True").count()==0:
                        verified="[Not verified]"
                  else:
                        verified="[Verified]"

                  args={"volunteer_profile":volunteer_details,"verified":verified}
                  return render(request,'find_a_volunteer_dir/view_accepted_volunteer_profile.html',args)
            else:
                  return redirect('/error/')

      else:
            return redirect('/error/')



@must_be_logged_in
def verify_account(request):
      #The line below makes sure you can only access this page if you...
      #...are not already verified (i.e you don't have a ...
      #...verification object with the verified field=True...
      # ...and the owner_id field being your id).
      if verification_details.objects.filter(owner_id=request.user.id, 
                                             verified="True").count()==0: 
            user_type=request.user.user_type
            args={"user_type":user_type}
            return render(request,'find_a_volunteer_dir/verify_account.html',args)
      else:
            return(redirect('/error/'))

import io
import base64

@must_be_logged_in
def verify_account_captcha(request):
      #The below if statement makes sure that already verified users...
      #...can't access this page.
      if verification_details.objects.filter(owner_id=request.user.id,
                                             verified="True").count()==0:

            if request.method != 'POST': 
            #^^If the request method !=POST then the user is first requesting...
            #...page so a blank instance of the form has to be created.
            
                  form=captcha_verification_form()
                  alphabet=["A","B","C","D","E","F","G","H","I","J","K","L",
                  "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
                  verification_word=""
                  
                  #Because the user  is first requesting the page, the ...
                  #...captcha and verification word must be generated.
                  list_of_modified_image_arrays=[]
                  #^This list will store a 2D array of the raw numbers ...
                  #...representing the images.
                  for count in range(0,4):
                  #^The captcha will have 4 letters, hence the range of this loop.
                      letter=alphabet[random.randint(0,25)]
                      verification_word=verification_word+letter
                      source_image=letter+".png"
                      #^Inside the "alphabet_images" folder, there are...
                      #...normal  pngs of the 26 letters. The modifications...
                      #...are applied to these base images. The line above...
                      #...these comments gets the filename of the particular image.

                      modification=random.randint(0,2)
                      #For each of the 4 letters, there are 3 possible modifications...
                      #...which can be applied to the letter. Each of these...
                      #...letter_modification_[int] functions takes in an image and...
                      #....outputs out a raw 2D array representing the modified letter.
                      changed_letter=0
                      if modification==0:
                          changed_letter=letter_modification_1(source_image)
                      if modification==1:
                          changed_letter=letter_modification_2(source_image)
                      if modification==2:
                          changed_letter=letter_modification_3(source_image)
                      list_of_modified_image_arrays.append(changed_letter)
                      
                  combined_image=concatenate_4_image_arrays(
                        list_of_modified_image_arrays[0],
                        list_of_modified_image_arrays[1],
                        list_of_modified_image_arrays[2],
                        list_of_modified_image_arrays[3])
                  #The 4 elements of the list are each a 2D array of raw values...
                  #...representing a modified letter. These 4 arrays have to be...
                  #...combined into one large raw 2D array and then this array...
                  #...has to be converted into a displayable png image. This is...
                  #...done by the concatenate_4.... function above.

                  user_id=request.user.id
                  img_src=r'''C:\Users\arunh\Python NEA\find_a_volunteer\user_images\
                        user_captcha_images\user_'+str(user_id)+'_captcha.jpeg'''
                  #The path of where this image will be saved has to be assigned...
                  #...to this img_src variable so that it can be passed to the...
                  #...template so that it can know which image to display.

                  combined_image.save('''C:/Users/arunh/Python NEA/find_a_volunteer/
                  user_images/user_captcha_images/user_%i_captcha.jpeg' %user_id,'jpeg''')
                  #Saving the image to this url required adding the user_images...
                  #...directory to the MEDIA_URL and MEDIA_ROOT in settings.py.
                  #Also, because of the OverwriteStorage() in the image upload...
                  #...model, each user can only have 1 captcha stored to the...
                  #...web host machine at a time as when a new one is generated,...
                  #...it has the same filename and overwrites the previous one.
                  #This helps prevent storage becoming unnecessary filled by captcha images.

            else:
            #If the request is a POST one, the form inputs must be processed and saved.
                  form=captcha_verification_form(data=request.POST)
                  if form.is_valid(): 
                        data=form.cleaned_data
                        answer=data['captcha_answer']
                        verification_word=request.POST.get('hidden_verification_word')
                        #The verification_word was generated in the other conditional...
                        #...statement. If I generated it outside the get/post conditional...
                        #...statements then the verification word would be generated twice;
                        #Once when the user requested this view with a GEt request ...
                        #...and again when the user requested this view with a POST request...
                        #...which would be an issue as the CAPTCHA would represent a...
                        #...different verification word then the one I would compare...
                        #...the user's answer to.
                        #To pass the verficiation word from the GET conditional branch to this...
                        #...one, I pass it from the GET request as a hidden input with the form...
                        #...so that it can be accessed from the form in the line above these...
                        #... comments.

                        
                        if answer == verification_word:
                              #If the user's answer is what the captcha was actually representing...
                              #... , then the user is verified so this branch runs. 

                              new_verification_details=form.save(commit=False)
                              new_verification_details.owner_id=request.user.id
                              new_verification_details.verified=True
                              new_verification_details.save()
                              #A new_verification_details object representing this user's ...
                              #...verification is saved to the database.
                              return redirect('/')
                        
                        else: 
                              #If the user's answer is wrong then the the page is refreshed...
                              #... and thus the captcha is also regenerated to indicate...
                              #...to them that they have got it wrong.
                              #Also, no object is saved as verification_details objects...
                              #...are only saved when the verified field would be True,...
                              #...as storing the objects where verified=False would...
                              #...just be a waste of storage space. 
                              return redirect('/verify_account/captcha/') 

                  else:
                        return redirect('/verify_account/captcha/')
            args={'form':form,'img_src':img_src,'verification_word':verification_word}
            #The img src is passed to the template so that it knows which image to be...
            #...displayed as there is up to 1 captcha image for each user so it needs...
            #...to display the right one!

            return render(request,'find_a_volunteer_dir/verify_account_captcha.html',args)
      else:
            return(redirect('/error/'))



import keras
import tensorflow as tf
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model as load_model_keras
import numpy as np
#^^^ These imports are used for ...
#... loading / running the neural network. 


#This function loads and prepares an image.
def load_image(filename):
	img = load_img(filename, color_mode="grayscale", target_size=(28, 28))
      #^ First, the image is loaded in grayscale.
	
	img = img_to_array(img)
      #^The image is then converted to a 2D array.
	
	img = img.reshape(1, 28, 28, 1)
      #^Next, the image is reshaped and made into a single channel img.
	
	img = img.astype('float32')
      #^The pixel values are then converted from ints into "float32"s so that...
      #...in the next line, they can be divided by 255.

	img = img / 255.0
      #The values of each pixel are then normalised (divided by 255) to be in the... 
      #...range 0 to 1 as the neural network model was trained on images...
      #...with pixel values in this range.
	return img


 
# This functions loads an image and then applies...
#...the model to the image to predict the class.
def run_model(filename):
	img = load_image(filename)
      #^The image is first loaded and prepped.
	model = load_model_keras(r'''C:\Users\arunh\Python NEA\find_a_volunteer\
                               find_a_volunteer_dir\final_model.h5''')
	#^Next the neural network model is loaded from the "final_model.h5" file.
      
	digit=np.argmax(model.predict(img), axis=-1)
      #^Next, the digit which is in the image is predicted!
	return(digit[0])
      #This digit is returned.
 






@must_be_logged_in      
def verify_account_handwritten_digit(request):

      if verification_details.objects.filter(owner_id=request.user.id, 
                                             verified="True").count()==0:
      #^This makes sure only users who are not yet verified can access this page.
            
            if request.method!='POST':
                  form=upload_image_form()
                  digit = random.randint(0,9)
            #^If the request is a GET request, then a blank instance of the...
            #...upload_image_form is created and a random digit is generated.
                  
            else:
                  form=upload_image_form(request.POST,request.FILES)
                  
                  if form.is_valid():
                        image_upload.objects.filter(user_id_of_uploader=request.user.id).delete()
                        #^ First, all image_upload objects whose user_id_of_uploader...
                        #...field = the user's id are deleted as they are now...
                        #...irrelevant as all image_upload objects for a certain...
                        #...user store the same image_path as the user's image...
                        #...is saved to the same path each time.

                        
                        digit=int(request.POST.get('hidden_digit'))
                        #^ The digit which the user's uploaded image is meant to be...
                        #... is gathered from the hidden field of the form.

                        image=form.save(commit=False)
                        image.user_id_of_uploader=request.user.id
                        image.save()
                        #^ The form is saved to create a new image_upload object.
                    
                        
                        user_id=request.user.id
                        file_path='''C:/Users/arunh/Python NEA/find_a_volunteer/
                        user_images/user_uploaded_images/'''+str(user_id)+'.png'
                        #^Because a user's image is always saved with the same filename...
                        #...and overwrites the previously saved one, the file path above...
                        #...is where the user's upload image is stored.
                        
                        interpreted_digit=run_model(file_path)
                        #This applies my neural network to the user's image file...
                        #... at the file path using the run_model() function.
                        
                        if interpreted_digit==digit:
                        #^The above conditional statement is true if the user...
                        #...uploads an image where they've written the right digit...
                        #...and my neural network successfully  
                              new_verification_details=verification_details.objects.create(owner_id=request.user.id,
                              interpreted_written_digit=interpreted_digit,verified=True)
                              
                              return redirect('/')
                        else:
                              #If the neural network has failed...
                              #... or the user has written the incorrect digit...
                              #... , the page is refreshed.
                              return redirect('/verify_account/handwritten_digit/')
                  else:
                        
                        return redirect('/verify_account/handwritten_digit/')

            args={'digit':digit,'form':form}      
            return render(request,'find_a_volunteer_dir/verify_account_handwritten_digit.html',args)

      else:
            return(redirect('/error/'))
      


      
