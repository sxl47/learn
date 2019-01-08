from django.http import HttpResponse, JsonResponse

from task import tasks


def hello(request):
    return HttpResponse("Hello world ! ")


def add(request):
    re_data = {
        'code': 0,
        'data': tasks.add(2, 3),
    }

    return JsonResponse(re_data)
