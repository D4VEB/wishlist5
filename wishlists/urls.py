from rest_framework.authtoken.views import obtain_auth_token
from wishlists.views import DetailUpdateDeleteList, ListCreateList, \
    DetailUpdateDeleteItem, ListCreateItem, \
    DetailUpdateDeletePledge, ListCreatePledge, ListCreateProfile, \
    DetailUpdateProfile, ListCreateUser
from django.conf.urls import url


urlpatterns = [
    url(r'^lists/(?P<pk>\d+)$', DetailUpdateDeleteList.as_view(),
        name='api_list_detail_update'),
    url(r'^lists/$', ListCreateList.as_view(),
        name='api_list_list_create'),
    url(r'^items/(?P<pk>\d+)$', DetailUpdateDeleteItem.as_view(),
        name='api_item_detail_update'),
    url(r'^items/$', ListCreateItem.as_view(),
        name='api_item_list_create'),
    url(r'^pledges/(?P<pk>\d+)$', DetailUpdateDeletePledge.as_view(),
        name='api_pledge_detail_update'),
    url(r'^pledges/$', ListCreatePledge.as_view(),
        name='api_pledge_list_create'),
    url(r'^profiles/$', ListCreateProfile.as_view(),
        name='api_profile_list_create'),
    url(r'^profiles/(?P<pk>\d+)$', DetailUpdateProfile.as_view(),
        name='api_profile_detail_update'),
    url(r'^users/$', ListCreateUser.as_view(),
         name='api_user_list_create'),
    url(r'^api-token-auth/', obtain_auth_token),
]
