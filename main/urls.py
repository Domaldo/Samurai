from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("", views.Home.as_view(), name="home"),

    path("locksmith-create/", views.l_create.as_view(), name="locksmith-create"),
    path("locksmith-search/", views.l_search, name="locksmith-search"),
    path("locksmith-list/", views.l_list.as_view(), name="locksmith-list"),
    path("locksmith-data/<int:pk>", views.l_data.as_view(), name="locksmith-data"),

    path("contract/<int:pk>", views.Contract.as_view(), name="contract"),
    path("contract/list/", views.Contract_List.as_view(), name="contract_list"),
    path("contract/status/<int:pk>/<str:status>", views.Contract_Status.as_view(url='/contract/list'), name="contract_status"),
    path("rating/", views.Vote.as_view(url='/locksmith-search'), name="vote"),
]
