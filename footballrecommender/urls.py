
from django.conf.urls import include, url
from django.contrib import admin

from

urlpatterns = [
    url(r'^recommender/', include('recommender.urls')),
    url(r'^admin/', admin.site.urls),
]
