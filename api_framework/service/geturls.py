from django.conf.urls import url, include

from .getmethods import ServiceGetMethods

def ServiceGetUrls(class_instance, endpoint):
    urls = []
    for method in ServiceGetMethods(class_instance):
        urls.append(url(method.name + '/', method.serviceMethod))
    
    return url('^' + endpoint + '/', include(urls))
