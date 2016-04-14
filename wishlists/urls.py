from rest_framework.authtoken.views import obtain_auth_token
from wishlists.views import APIDetailUpdateList, APIListCreateList, \
    APIDetailUpdateItem, APIListCreateItem, \
    APIDetailUpdatePledge, APIListCreatePledge
from django.conf.urls import url



urlpatterns = [
    url(r'^lists/(?P<pk>\d+)$', APIDetailUpdateList.as_view(),
        name='api_list_detail_update'),
    url(r'^lists/$', APIListCreateList.as_view(),
        name='api_list_list_create'),
    url(r'^items/(?P<pk>\d+)$', APIDetailUpdateItem.as_view(),
        name='api_item_detail_update'),
    url(r'^items/$', APIListCreateItem.as_view(),
        name='api_item_list_create'),
    url(r'^pledges/(?P<pk>\d+)$', APIDetailUpdatePledge.as_view(),
        name='api_pledge_detail_update'),
    url(r'^pledges/$', APIListCreatePledge.as_view(),
        name='api_pledge_list_create'),
    url(r'^api-token-auth/', obtain_auth_token),
]
