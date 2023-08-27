
from django.urls import path
from . import views

app_name="find_a_volunteer_dir" #This tells django what the application namespace...
#...these urls refer to is.

#the first parameter is the pattern being matched. The pattern is the ...
    #... bit that comes after the domain name so a '' pattern means it is matching a url which is just the domain name.
    #the second part tells it what view to call when this url pattern is requested. The third part provides a name for..
    #.. this url so we can refer to it elsewhere.
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('volunteer/homepage/', views.volunteer_homepage, name='volunteer_homepage'),
    path('organisation/homepage/', views.organisation_homepage, name='organisation_homepage'),
    path('error/', views.error_page, name="error_page"),
    path('volunteer/new_volunteer_profile/',views.new_volunteer_profile,name='new_volunteer_profile'),
    path('volunteer/view_volunteer_profile/', views.view_volunteer_profile,name='view_volunteer_profile'),
    path('volunteer/edit_volunteer_profile/',views.edit_volunteer_profile,name='edit_volunteer_profile'),
    path('volunteer/generate_matches/',views.match_volunteer_with_organisations,name='match_volunteer_with_organisations'),
    path('volunteer/accept_or_reject_matches/',views.accept_or_reject_matches,name='accept_or_reject_matches'),
    path('organisation/new_organisation_profile',views.new_organisation_profile,name='new_organisation_profile'),
    path('organisation/view_organisation_profile',views.view_organisation_profile,name='view_organisation_profile'),
    path('organisation/edit_organisation_profile',views.edit_organisation_profile,name='edit_organisation_profile'),
    path('volunteer/view_matched_organisation_profile/<int:organisation_id>/',views.view_matched_organisation_profile,
        name='view_matched_organisation_profile'),     
    #^<int:[]> is used to indicate pagination i.e where there is an index number required for the page.
    path('volunteer/view_accepted_organisations',views.view_accepted_organisations,name='view_accepted_organisations'),
    path('organisation/view_volunteers_who_have_accepted',views.view_volunteers_who_have_accepted,
        name='view_volunteers_who_have_accepted'),
    path('organisation/view_accepted_volunteer_profile/<int:volunteer_id>/',views.view_accepted_volunteer_profile,
        name='view_accepted_volunteer_profile'),
    path('verify_account/',views.verify_account,name='verify_account'),
    path('verify_account/captcha/',views.verify_account_captcha,name="verify_account_captcha"),
    path('verify_account/handwritten_digit/',views.verify_account_handwritten_digit,name="verify_account_handwritten_digit"),
]
