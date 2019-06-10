from django.shortcuts import render
from django.template import RequestContext, loader
import json

from gears_manager import glo_stepper

# Create your views here.

from django.http import HttpResponse

def index(request):
    template = loader.get_template('gears_ui/index.html')
    context = RequestContext(request, {});
    return HttpResponse(template.render(context))

def setFreq(request):
    glo_stepper.set_freq(int(request.GET.get("freq", "0")))

    return HttpResponse("okey dokey")

def setEnable(request):
    glo_stepper.enable(request.GET.get("value", "0") == "1")

    return HttpResponse("okey dokey")

def getStatus(request):
    result = {"freq": glo_stepper.get_freq(),
              "enabled": glo_stepper.get_enabled()}

    return HttpResponse(json.dumps(result), content_type='application/javascript')
