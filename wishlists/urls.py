from rest_framework.authtoken.views import obtain_auth_token
from wishlists.views import DetailUpdateList, ListCreateList, \
    DetailUpdateItem, ListCreateItem, \
    DetailUpdatePledge, ListCreatePledge, ListCreateProfile, \
    DetailUpdateProfile, ListCreateUser
from django.conf.urls import url


urlpatterns = [
    url(r'^lists/(?P<pk>\d+)$', DetailUpdateList.as_view(),
        name='api_list_detail_update'),
    url(r'^lists/$', ListCreateList.as_view(),
        name='api_list_list_create'),
    url(r'^items/(?P<pk>\d+)$', DetailUpdateItem.as_view(),
        name='api_item_detail_update'),
    url(r'^items/$', ListCreateItem.as_view(),
        name='api_item_list_create'),
    url(r'^pledges/(?P<pk>\d+)$', DetailUpdatePledge.as_view(),
        name='api_pledge_detail_update'),
    url(r'^pledges/$', ListCreatePledge.as_view(),
        name='api_pledge_list_create'),
    url(r'^profiles/$', ListCreateProfile.as_view(),
        name='api_profile_list_create'),
    url(r'^profiles/(?P<pk>\d+)$', DetailUpdateProfile.as_view(),
        name='api_profile_detail_update'),
    url(r'^users/$', ListCreateUser.as_view(),
         name='api_profile_list_create'),
    url(r'^api-token-auth/', obtain_auth_token),
]
