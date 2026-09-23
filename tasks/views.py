from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import ProjectForm,TaskForm,ProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from datetime import date
def home(request):

    return redirect("dashboard")


def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("register")

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Account created successfully."
        )

        login(request, user)

        return redirect("dashboard")

    return render(
        request,
        "registration/register.html"
    )


def user_login(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                "Login successful."
            )

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "registration/login.html"
    )


def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("login")


@login_required(login_url="/login/")
def dashboard(request):

    # -----------------------------
    # PROJECT COUNT
    # -----------------------------

    projects_count = Project.objects.filter(
        user=request.user
    ).count()


    # -----------------------------
    # ALL TASKS
    # -----------------------------

    user_tasks = Task.objects.filter(
        project__user=request.user
    )


    total_tasks = user_tasks.count()


    # -----------------------------
    # TASK STATUS COUNTS
    # -----------------------------

    completed_tasks = user_tasks.filter(
        status="completed"
    ).count()


    todo_tasks = user_tasks.filter(
        status="todo"
    ).count()


    progress_tasks = user_tasks.filter(
        status="progress"
    ).count()


    pending_tasks = user_tasks.exclude(
        status="completed"
    ).count()


    # -----------------------------
    # TASK PROGRESS
    # -----------------------------

    if total_tasks > 0:

        completion_percentage = round(
            (completed_tasks / total_tasks) * 100
        )

    else:

        completion_percentage = 0


    # -----------------------------
    # DUE DATE INFORMATION
    # -----------------------------

    today = date.today()


    overdue_tasks = user_tasks.filter(
        due_date__lt=today
    ).exclude(
        status="completed"
    ).count()


    today_tasks = user_tasks.filter(
        due_date=today
    ).exclude(
        status="completed"
    ).count()


    upcoming_tasks = user_tasks.filter(
        due_date__gt=today
    ).exclude(
        status="completed"
    ).order_by(
        "due_date"
    )[:5]


    # -----------------------------
    # RECENT TASKS
    # -----------------------------

    recent_tasks = user_tasks.select_related(
        "project"
    ).order_by(
        "-created_at"
    )[:5]


    # -----------------------------
    # CONTEXT
    # -----------------------------

    context = {

        "projects_count": projects_count,

        "total_tasks": total_tasks,

        "completed_tasks": completed_tasks,

        "pending_tasks": pending_tasks,

        "todo_tasks": todo_tasks,

        "progress_tasks": progress_tasks,

        "completion_percentage": completion_percentage,

        "overdue_tasks": overdue_tasks,

        "today_tasks": today_tasks,

        "upcoming_tasks": upcoming_tasks,

        "recent_tasks": recent_tasks,

    }


    return render(
        request,
        "dashboard.html",
        context
    )
    
from django.shortcuts import render, redirect, get_object_or_404  
@login_required(login_url="/login/")
def project_create(request):

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():

            project = form.save(commit=False)

            project.user = request.user

            project.save()

            messages.success(
                request,
                "Project created successfully."
            )

            return redirect("project_list")

    else:

        form = ProjectForm()

    return render(
        request,
        "projects/project_form.html",
        {
            "form": form,
            "title": "Create Project"
        }
    )
    
@login_required(login_url="/login/")
def project_detail(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        user=request.user
    )

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project
        }
    )
    
@login_required(login_url="/login/")
def project_update(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        user=request.user
    )

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            instance=project
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Project updated successfully."
            )

            return redirect(
                "project_detail",
                project_id=project.id
            )

    else:

        form = ProjectForm(
            instance=project
        )

    return render(
        request,
        "projects/project_form.html",
        {
            "form": form,
            "title": "Edit Project"
        }
    )
@login_required(login_url="/login/")
def project_list(request):

    projects = Project.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects
        }
    )
    
@login_required(login_url="/login/")
def project_delete(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        user=request.user
    )

    if request.method == "POST":

        project.delete()

        messages.success(
            request,
            "Project deleted successfully."
        )

        return redirect("project_list")

    return render(
        request,
        "projects/project_confirm_delete.html",
        {
            "project": project
        }
    )
    
@login_required(login_url="/login/")
def task_list(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        user=request.user
    )

    tasks = project.tasks.all()

    # Search
    search = request.GET.get(
        "search",
        ""
    ).strip()

    # Status filter
    status = request.GET.get(
        "status",
        ""
    )

    # Priority filter
    priority = request.GET.get(
        "priority",
        ""
    )

    # Apply search
    if search:

        tasks = tasks.filter(
            title__icontains=search
        )

    # Apply status filter
    if status:

        tasks = tasks.filter(
            status=status
        )

    # Apply priority filter
    if priority:

        tasks = tasks.filter(
            priority=priority
        )

    # Newest tasks first
    tasks = tasks.order_by(
        "-created_at"
    )

    context = {
        "project": project,
        "tasks": tasks,

        "search": search,

        "selected_status": status,

        "selected_priority": priority,
    }

    return render(
        request,
        "tasks/task_list.html",
        context
    )
    
@login_required(login_url="/login/")
def task_create(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        user=request.user
    )

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(
                commit=False
            )

            task.project = project

            task.save()

            messages.success(
                request,
                "Task created successfully."
            )

            return redirect(
                "task_list",
                project_id=project.id
            )

    else:

        form = TaskForm()

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
            "project": project,
            "title": "Create Task",
        }
    )
@login_required(login_url="/login/")
def task_update(request, project_id, task_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        user=request.user
    )

    task = get_object_or_404(
        Task,
        id=task_id,
        project=project
    )

    if request.method == "POST":

        form = TaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Task updated successfully."
            )

            return redirect(
                "task_list",
                project_id=project.id
            )

    else:

        form = TaskForm(
            instance=task
        )

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
            "project": project,
            "title": "Edit Task",
        }
    )
    
@login_required(login_url="/login/")
def task_delete(request, project_id, task_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        user=request.user
    )

    task = get_object_or_404(
        Task,
        id=task_id,
        project=project
    )

    if request.method == "POST":

        task.delete()

        messages.success(
            request,
            "Task deleted successfully."
        )

        return redirect(
            "task_list",
            project_id=project.id
        )

    return render(
        request,
        "tasks/task_confirm_delete.html",
        {
            "task": task,
            "project": project
        }
    )
    
@login_required(login_url="/login/")
def profile(request):

    user = request.user

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=user
        )

    return render(
        request,
        "profile.html",
        {
            "form": form
        }
    )
@login_required(login_url="/login/")
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                "Your password was changed successfully."
            )

            return redirect("profile")

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        "change_password.html",
        {
            "form": form
        }
    )