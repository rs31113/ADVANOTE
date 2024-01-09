import projects.models


def project_count_process(request):
    if request.user.is_authenticated:
        project_count = projects.models.Project.objects.get_all_user_projects(
            request.user,
        ).count()
        return {"project_count": project_count}
    return {}


__all__ = ()
