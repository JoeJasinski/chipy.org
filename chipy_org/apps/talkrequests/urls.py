from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.TalkRequestList.as_view(), name="talkrequests_list"),
]
