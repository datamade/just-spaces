from django.contrib import admin
from django.contrib.auth.models import Group, User
from countries_plus.admin import Country
from languages_plus.admin import Language, CultureCode
from fobi.admin import FormElement, FormEntry, FormHandler, \
                       FormWizardEntry, FormWizardHandler
from users.admin import JustSpacesUserAdmin

admin.site.unregister(Group)

admin.site.unregister(Country)

admin.site.unregister(Language)
admin.site.unregister(CultureCode)

admin.site.unregister(FormElement)
admin.site.unregister(FormEntry)
admin.site.unregister(FormHandler)
admin.site.unregister(FormWizardEntry)
admin.site.unregister(FormWizardHandler)

admin.site.register(User, JustSpacesUserAdmin)
