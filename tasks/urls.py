from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),
    path(
    "projects/",
    views.project_list,
    name="project_list"
    ),
    path(
    "projects/create/",
    views.project_create,
    name="project_create"
    ),
    path(
    "projects/<int:project_id>/",
    views.project_detail,
    name="project_detail"
    ),
    path(
    "projects/<int:project_id>/edit/",
    views.project_update,
    name="project_update"
    ),
    path(
    "projects/<int:project_id>/delete/",
    views.project_delete,
    name="project_delete"
    ),
    path(
    "projects/<int:project_id>/tasks/",
    views.task_list,
    name="task_list"
    ),
    path(
    "projects/<int:project_id>/tasks/create/",
    views.task_create,
    name="task_create"
    ),
    path(
    "projects/<int:project_id>/tasks/<int:task_id>/edit/",
    views.task_update,
    name="task_update"
    ),
    path(
    "projects/<int:project_id>/tasks/<int:task_id>/delete/",
    views.task_delete,
    name="task_delete"
    ),
    path(
    "profile/",
    views.profile,
    name="profile"
   ),
    path(
    "change-password/",
    views.change_password,
    name="change_password"
    ),

]