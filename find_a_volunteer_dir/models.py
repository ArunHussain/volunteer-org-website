from django.db import models #every model I define inherits from Django's inbuilt models.Model
from django.conf import settings #details from the settings.py file are used in multiple models.
from django.core.files.storage import FileSystemStorage
#^This is used in the OverwriteStorage class definition where FileSystemStorage is inherited from.
import os # This is used for manipulating file paths in the rename_and_path function. 

# Create your models here.

'''
class BaseEntity(models.Model): # this inherits from the parent class Model inncluded in Django.
    #The parent class for volunteers and organisations
    self_description=models.CharField(max_length=200)
''' #actually a base class is kinda useless as the organisatoins nad volunteers are quite different.


class volunteer_profile(models.Model):
    owner_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#settings.AUTH_USER_MODEL is where I tell Django to use my custom user model.
#Therefore line 15 tells Django to create the OneToOne relationship between this field and my custom user model.
    activity_choices=(
        ("Admin","Admin"),
        ("Animal care","Animal care"),
        ("Babysitting","Babysitting"),
        ("Cooking","Cooking"),
        ("Cleaning","Cleaning"),
        ("Education","Education"),
        ("Elder care help","Elder care help"),
        ("Fundraising","Fundraising"),
        ("Music","Music"),
        )
    first_preferred_activity = models.CharField(max_length=40,choices=activity_choices)
    second_preferred_activity = models.CharField(max_length=40,choices=activity_choices, blank=True)
    #^blank = true means these fields are not required.
    third_preferred_activity = models.CharField(max_length=40,choices=activity_choices, blank=True)
    contact_details = models.CharField(max_length=70)
    self_description= models.CharField(max_length=300)
    age=models.IntegerField()

    time_choices=( #This shows the choices for each [day]_availability field.
        ("Morning","Morning"),
        ("Afternoon","Afternoon"),
        ("Evening","Evening"),
        ("All day","All day"),
        ("None","None"),
        )
    monday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    tuesday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    wednesday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    thursday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    friday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    saturday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    sunday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    name=models.CharField(max_length=30)
    postcode=models.CharField(max_length=10, blank=True)

    def __str__(self):
        return(self.name)


    
                                    #with the 2 classes below, essentially what I want is for the field of the model to have a list of elements. This is only possible if I use postgreSQL or json. 
            #organisations can't accept volunteers because volunteers accept organisations.

#Each instance of this model represents 1 match between...
#... a single organisation and a single volunteer.
class matched_organisations(models.Model):
    volunteer_owner_id=models.IntegerField()
    id_of_matched_organisation = models.IntegerField() 
    organisation_compatibility_score=models.IntegerField()

   
    '''
    class Meta:
        verbose_name_plural='matched_organisations'
    def __str__(self):
        return(self.volunteer.name + "'s matched organisations")#I want the text representing matched organisations to be...
       #the bit above is how you access fields of foreign key   #.. [name of volunteer] + "'s matched organisations".
                                                        #this means I have to access fields of this class' foreign key!
'''
class accepted_organisations(models.Model): 
    volunteer_owner_id=models.IntegerField()
    id_of_accepted_organisation=models.IntegerField()
    
    #These are the 2 decisions a volunteer can make on a matched organisation.
    decisions_choices=(
        ("Accept","Accept"),
        ("Reject","Reject"),
        )
    decision=models.CharField(max_length=15,choices=decisions_choices) 
#^ despite the user only having 2 choices, both of which are <15 characters ...
#... a CharField must have a "max_length" defined.


class organisation_profile(models.Model):
    owner_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#Like with the volunteer_profile, this has a OneToOne relationship with the user.
    activity_choices=(
        ("Admin","Admin"),
        ("Animal care","Animal care"),
        ("Babysitting","Babysitting"),
        ("Cooking","Cooking"),
        ("Cleaning","Cleaning"),
        ("Education","Education"),
        ("Elder care help","Elder care help"),
        ("Fundraising","Fundraising"),
        ("Music","Music"),
        )
    available_activity_1 = models.CharField(max_length=40,choices=activity_choices)
    available_activity_2 = models.CharField(max_length=40,choices=activity_choices, blank=True)
    available_activity_3 = models.CharField(max_length=40,choices=activity_choices, blank=True)
    desired_age_lower_bound=models.IntegerField()
    desired_age_upper_bound=models.IntegerField()
    contact_details = models.CharField(max_length=70)
    postcode = models.CharField(max_length=10) #This is not optional unlike for volunteers.
    self_description= models.CharField(max_length=300)
    name = models.CharField(max_length=40)
    
    time_choices=( 
        ("Morning","Morning"),
        ("Afternoon","Afternoon"),
        ("Evening","Evening"),
        ("All day","All day"),
        ("None","None"),
        )
    monday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    tuesday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    wednesday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    thursday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    friday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    saturday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )
    sunday_availability=models.CharField(
        max_length=20,
        choices=time_choices,
        )

    def __str__(self):  #this is the text Django uses to show an organisation.
        return self.name
    

#For the below classes,:
    #these are volunteers who have matched with them. Organisations can't generate matches only volunteers can. 
    #these are volunteers who have matched with then accepted the organisation.

'''
#THIS is useless.    
class matched_volunteers(models.Model): 
    organisation=models.ForeignKey(organisation_profile, on_delete=models.CASCADE)
    matched = models.TextField()
    class Meta:
        verbose_name_plural='matched_volunteers'
    def __str__(self):
        return(self.organisation.name + "'s matched volunteers")

class accepted_volunteers(models.Model):
    organisation_owner_id=models.ForeignKey(organisation_profile, to_field='owner_id', on_delete=models.CASCADE)
    id_of_volunteer=models.IntegerField()
    decisions_choices=(
        ("Accept","Accept"),
        ("Reject","Reject"),
        )
    decision=models.CharField(max_length=15,choices=decisions_choices,default="reject")
    class Meta:
        verbose_name_plural='accepted_volunteers'
    def __str__(self):
        return(self.organisation.name + "'s accepted volunteers")
'''


class verification_details(models.Model):
    owner_id=models.IntegerField() 
    #^this is the id of the user a particular instance of this model corresponds to.
    captcha_answer=models.CharField(max_length=20,blank=True)
    #^This is the user's answer to what they think the captcha says.
    interpreted_written_digit=models.CharField(max_length=1,blank=True)
    #^this is the output of the digit recognition neural network.
    verified=models.BooleanField()
    






# When a user uploads an image and it is saved to the website hosting machine, by default it is...
#... saved with the original filename the user had on their local machine. The issue with this...
#...is that it is not a meaningful file name. Changing the filename when storing the file on...
#...the web hosting machine to "[user_id_of_uploader].png" means that the user who uploaded...
#...a certain file can be easily found out. Additionally it means that 


def rename_and_path(instance, filename): 
    path='C:/Users/arunh/Python NEA/find_a_volunteer/user_images/user_uploaded_images/'
    #^This is the file directory where I store the images uploaded by users.
    file_extension="png"
    filename = '{}.{}'.format(str(instance.user_id_of_uploader), file_extension)  
    #^The above is the new filename
    return os.path.join(path, filename)#This joins the filename to the path in line 229.


    
#this is used to overwrite images with the same filename as the file currently trying to be saved.
class OverwriteStorage(FileSystemStorage): 
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
            #^The above line removes the pre-existing file with the same name
        return name



class image_upload(models.Model): 
    user_id_of_uploader=models.IntegerField()
    #^This is the id of the user who uploaded the image.
    image=models.ImageField(storage=OverwriteStorage(), upload_to=rename_and_path) 
    #the "OverwriteStorage()" part makes sure that Django overwrites files with the same name, ...
    #...instead of storing the file with a random sequence of letters appended to the end...
    #...of the filename, when saving the user's image file to ensure each user can only ...
    #... have 1 image file saved to the machine hosting the website.

