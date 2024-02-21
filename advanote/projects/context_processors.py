import projects.models


def projects_count(request):
    if request.user.is_authenticated:
        projects_count = projects.models.Project.objects.get_all_user_projects(
            request.user,
        ).count()
    else:
        projects_count = 0
    return {"projects_count": projects_count}


__all__ = ()
