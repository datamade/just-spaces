from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def staff_required_custom_login(view):
    return staff_member_required(view, login_url=reverse_lazy('login'))
