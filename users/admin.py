from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import JustSpacesUser
from surveys.forms import JustSpacesForm
from django.utils.translation import ugettext_lazy as _


class JustSpacesUserCreationForm(UserCreationForm, JustSpacesForm):

    class Meta(UserCreationForm.Meta):
        model = JustSpacesUser
        fields = UserCreationForm.Meta.fields + ('email', 'agency',)


class JustSpacesUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = JustSpacesUser
        fields = ('agency', 'email')


class JustSpacesUserAdmin(UserAdmin):
    permissions_description = 'Just Spaces has three levels of user \
        permissions:<br /><br /> \
        1. <b>Field users</b> can run published surveys.<br /> \
        2. <b>Staff users</b> have all the permissions of field users. They can \
            also create, edit, and delete Agencies, Studies, Study Areas, \
            Surveys, and Locations. They can publish surveys so they can \
            be run by field users. Staff users can also view all collected \
            data and design data visualizations on the collected data pages.<br /> \
        3. <b>Superusers</b> have all the permissions of staff users. They can \
        also create, edit, and delete other users. <b>All superusers should \
        also have "Staff status" selected below</b>.<br />'

    fieldsets = (
        (None, {'fields': ('username', 'password', 'agency')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser'),
                'description': permissions_description,
            }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(JustSpacesUser, JustSpacesUserAdmin)
