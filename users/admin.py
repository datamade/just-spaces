from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import JustSpacesUser
from surveys.forms import JustSpacesForm


class JustSpacesUserCreationForm(UserCreationForm, JustSpacesForm):

    class Meta(UserCreationForm.Meta):
        model = JustSpacesUser
        fields = UserCreationForm.Meta.fields + ('email', 'agency',)


class JustSpacesUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = JustSpacesUser
        fields = ('agency', 'email')


class JustSpacesUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('agency',),
        }),
    )


admin.site.register(JustSpacesUser, JustSpacesUserAdmin)
