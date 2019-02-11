from django.views.generic import TemplateView

class CreateNewSurvey(TemplateView):
    template_name = "create_new_survey.html"

# Create pong route
from django.http import HttpResponse

def pong(request):
    try:
        from .deployment import DEPLOYMENT_ID
    except ImportError:
        return HttpResponse('Bad deployment', status=401)

    return HttpResponse(DEPLOYMENT_ID)
