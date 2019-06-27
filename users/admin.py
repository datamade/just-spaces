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
    permissions_description = 'This app employs three classes of \
        users:<br /><br /> \
        1. <b>Field users</b> can run published surveys. <b>To create a \
            field user, check \'Active\' below.</b><br /> \
        2. <b>Staff users</b> have all the permissions of field users. They \
            can also create, edit, and delete Agencies, Studies, Study Areas, \
            Surveys, and Locations. They can publish surveys so they can be \
            run by field users. Staff users can also view all collected data \
            and design data visualizations on the collected data pages. <b>To \
            create a staff user, check \'Active\' and \'Staff status\' \
            below.</b><br /> \
        3. <b>Superusers</b> have all the permissions of staff users. They \
            can also create, edit, and delete other users. Only superusers \
            can set and change user passwords. <b>To create a superuser, \
            check all the boxes below.</b>'

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
