from django.contrib import admin
from find_a_volunteer_dir.models import volunteer_profile, organisation_profile,  matched_organisations,  accepted_organisations

# Register your models here.
admin.site.register(volunteer_profile)

admin.site.register(organisation_profile)


admin.site.register(matched_organisations)

admin.site.register(accepted_organisations)
