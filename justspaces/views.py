# Create pong route
def pong(request):
    from django.http import HttpResponse

    try:
        from .deployment import DEPLOYMENT_ID
    except ImportError as e:
        return HttpResponse('Bad deployment {}'.format(e), status=401)

    return HttpResponse(DEPLOYMENT_ID)
