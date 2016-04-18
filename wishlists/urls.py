from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url, include
from wishlists.views import ListCreateUser, DetailUpdateDeleteList, \
    ListCreateList, DetailUpdateDeleteItem, ListCreateItem, DetailPledge, \
    ListCreateProfile, DetailUpdateProfile, CreateCharge, ListPledge, \
    ListAllUsersList

urlpatterns = [
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^users/$', ListCreateUser.as_view(),
        name='api_user_list_create'),
    url(r'^lists/(?P<pk>\d+)$', DetailUpdateDeleteList.as_view(),
        name='api_list_detail_update'),
    url(r'^lists/$', ListCreateList.as_view(),
        name='api_list_list_create'),
    url(r'^alllists/$', ListAllUsersList.as_view(), name="all_users_lists"),
    url(r'^items/(?P<pk>\d+)$', DetailUpdateDeleteItem.as_view(),
        name='api_item_detail_update'),
    url(r'^items/$', ListCreateItem.as_view(),
        name='api_item_list_create'),
    url(r'^pledges/(?P<pk>\d+)$', DetailPledge.as_view(),
        name='api_pledge_detail'),
    url(r'^pledges/$', ListPledge.as_view(),
        name='api_pledge_list_create'),
    url(r'^profiles/$', ListCreateProfile.as_view(),
        name='api_profile_list_create'),
    url(r'^profiles/(?P<pk>\d+)$', DetailUpdateProfile.as_view(),
        name='api_profile_detail_update'),
    url(r'^$', ListCreateList.as_view()),
    url(r'^charges/', CreateCharge.as_view(), name = 'create_charge'),
]
