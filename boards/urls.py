from django.urls import path
from . import views

app_name = "boards"

urlpatterns = [
    path("", views.post_list, name="list"),
    path("new/", views.post_create, name="create"),
    path("<int:pk>/", views.post_detail, name="detail"),
    path("<int:pk>/comment/", views.comment_create, name="comment_create"),
    path("<int:pk>/like/", views.post_like_toggle, name="like_toggle"),
    path("<int:pk>/edit/", views.post_update, name="update"),
    path("<int:pk>/delete/", views.post_delete, name="delete"),
    path("<int:pk>/comment/<int:comment_pk>/delete/", views.comment_delete, name="comment_delete"),
    path(
    "<int:pk>/comment/<int:comment_pk>/edit/",
    views.comment_update,
    name="comment_update",    
),
path(
    "<int:pk>/comment/<int:comment_pk>/edit/",
    views.comment_update,
    name="comment_update",
),
]