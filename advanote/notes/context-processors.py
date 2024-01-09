import tasks.models


def tasks_count(request):
    if request.user.is_authenticated:
        tasks_count = tasks.models.Task.objects.filter(
            owner=request.user,
        ).count()
    else:
        tasks_count = 0
    return {"tasks_count": tasks_count}


__all__ = ()
