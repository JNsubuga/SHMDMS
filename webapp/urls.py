from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from pathlib import Path

###############
urlpatterns = [
    path("", views.index, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("users/", views.users, name="users"),
    path("user/add/", views.Adduser, name="add_user"),
    path("user/<int:userid>/update/", views.updateuser, name="update_user"),
    path("roles/", views.Roles, name="roles"),
    ### Logout
    path("logout/", views.logout, name="logout"),
    path("access-denied/", views.AccessDenied, name="access_denied"),
    path("received-documents/", views.receivedDocuments, name="received_documents"),
]
urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)