from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from .models import image_upload, organisation_profile, volunteer_profile, accepted_organisations, matched_organisations, verification_details
import requests


#the below is extending Django's default UserCreationForm as currently...
#...it only allows the user to input username and password...
#... but with the custom user model they have to be able to...
#... input for the user type field as well.
class UserCreationForm(UserCreationForm):
    user_type_choices=(
        ("volunteer",'volunteer'),
        ("organisation",'organisation'),
        )
    #To implement Choices in a model definition, a CharField with a choices...
    #... parameter is required but in the form, a ChoiceField with a choices...
    #... parameter can be used.
    user_type=forms.ChoiceField(choices=user_type_choices,required=True)   
    #^Required=True makes it so that users have to choose their type.
    
#Inside the "class Meta:" part, the model which the form takes data for is chosen.
#Additionally, the particular fields of that model which the form is going to be ...
#...taking user inputs for are chosen.
    class Meta: 
        model = CustomUser 
        fields = ('username', 'user_type', 'password1', 'password2')
#^username, password1 and password2 are fields of Django's default user model.

#The default UserCreationForm's save function has to be overriden...
#...to make sure the user_type input is also saved to the user model.
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.user_type = self.cleaned_data["user_type"] 
        if commit:
            user.save()
        return user


class volunteer_profile_form(forms.ModelForm):
    
    class Meta:
        model=volunteer_profile
        fields=['name','self_description','contact_details','age','postcode',
        'first_preferred_activity', 'second_preferred_activity','third_preferred_activity',
        'monday_availability','tuesday_availability','wednesday_availability',
        'thursday_availability','friday_availability','saturday_availability','sunday_availability']
#This form is going to be taking user inputs for every field of the volunteer_profile EXCEPT for the...
#...owner_id as this field will be given a value in the relevant view instead as the owner_id of a...
#...volunteer_profile is not up for the user to decide!

        labels={
            'self_description':'A brief self description',
            'first_preferred_activity':'Your most preferred volunteering activity to do',
            'second_preferred_activity':'Your second most (optional)',
            'third_preferred_activity':'Your third most (optional)'
        }     
#^The labels dictionary is where I define the labels for the fields. All the fields without a...
#...defined label don't have one because the default label Django will automatically give them is adequate.


class organisation_profile_form(forms.ModelForm):
    class Meta:
        model=organisation_profile
        fields=['name','self_description','contact_details','postcode','desired_age_lower_bound',
        'desired_age_upper_bound','available_activity_1','available_activity_2','available_activity_3',
        'monday_availability','tuesday_availability','wednesday_availability','thursday_availability',
        'friday_availability','saturday_availability','sunday_availability']
#Similarly to the volunteer_profile_form, this form will take user inputs for every field...
#...except for the owner_id.

        labels={
            'self_description':'A brief self description',
            'available_activity_1':'Available volunteering activity 1',
            'available_activity_2':'Available volunteering activity 2 (optional)',
            'available_activity_3':'Available volunteering activity 3 (optional)'
        }
#Similarly to the volunteer_profile_form, all the fields without a defined label...
#...don't have one as Django gives them a suitable default label.
        
        

class accept_reject_form(forms.ModelForm):

# this is where I dynamically fill my choice field for what organisation you're making a choice on from your matches.
    def __init__(self, user, *args, **kwargs): 
        super(accept_reject_form, self).__init__(*args, **kwargs)
        choices_for_accepting_or_rejecting=[] 
        #^This list will contain the matched organisations the particular user who is filling this form has...
        #...and can therefore make a decision on.
        
        #The below line iterates through every matched_organisation object associated with the user filling the form.
        for o in matched_organisations.objects.filter(volunteer_owner_id=user.id):
            already_has_been_decided_on = False #Matches which have already been decided on should not be available...
            #...for the user to make a decision on which is why this boolean is necessary.

            for org in accepted_organisations.objects.filter(volunteer_owner_id=user.id):
                if o.id_of_matched_organisation == org.id_of_accepted_organisation:
                    already_has_been_decided_on=True #For a match with a particular volunteer_owner_id and id_of_matched_organisation, ...
                    #...if there is an accepted_organisation object whose own volunteer_owner_id == volunteer_owner_id and whose...
                    #...id_of_accepted_organisation == id_of_matched_organisation...
                    #...then that match has already been decided on.

            if not already_has_been_decided_on:
                choices_for_accepting_or_rejecting.extend([(o.id_of_matched_organisation,
                str(organisation_profile.objects.get(owner_id=o.id_of_matched_organisation).name)+ " [ID:"+str(o.id_of_matched_organisation)+"]")])

                #^Matched_organisations which have not been decided on are added to the list.
                #The str(..) part is what is displayed for each choice in the form and the "o.id_of_matched_organisation" is what is taken...
                #...as the user's input if they select that choice.

        self.fields['id_of_accepted_organisation'] = forms.ChoiceField(
            choices=choices_for_accepting_or_rejecting,
            label="Organisation" #The label has to be defined here as well in this particular situation.
        )

    class Meta:
        model=accepted_organisations
        fields=['id_of_accepted_organisation','decision']
        labels={'id_of_accepted_organisation':'Organisation','decision':'Decision'}



    
class captcha_verification_form(forms.ModelForm):
    class Meta:
        model=verification_details
        fields=['captcha_answer'] 
        #^This form only takes the user's input for this one field.
        #Django will automatically give the label "Captcha answer:" which is fine.

class upload_image_form(forms.ModelForm):
    class Meta:
        model=image_upload
        #This form doesn't take inputs for the verification_details model as...
        #...it is only used for letting the user upload an image.
        fields=['image']
        labels={'image':'Upload image:'}
    
        
        
