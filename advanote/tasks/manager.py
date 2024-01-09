import django.db.models.manager


class TasksManager(django.db.models.manager.Manager):
    def get_user_tasks(self, user_id):
        return self.get_queryset().filter(owner=user_id)


__all__ = ()
