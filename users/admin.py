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
    fieldsets = (
        (None, {'fields': ('username', 'password', 'agency')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser'),
                'description': 'Just Spaces has two levels of user \
                    permissions: <b>staff users</b> and <b>field users</b>. \
                    Staff users can use all functions of the site, while field \
                    users are limited to running surveys. For staff users, \
                    select both "Staff status" and "Superuser status" below. \
                    For field users, select neither.'
            }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(JustSpacesUser, JustSpacesUserAdmin)
