from django.views.generic import TemplateView

class CreateNewSurvey(TemplateView):
    template_name = "create_new_survey.html"

# Create pong route
def pong(request):
    from django.http import HttpResponse

    try:
        from justspaces.deployment import DEPLOYMENT_ID
    except ImportError as e:
        return HttpResponse('Bad deployment {}'.format(e), status=401)

    return HttpResponse(DEPLOYMENT_ID)
