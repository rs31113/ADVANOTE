import django.db.models
import django.db.models.manager


class ProjectManager(django.db.models.manager.Manager):
    def get_user_projects(self, user_id):
        return self.get_queryset().filter(owner=user_id)

    def get_all_members(self, project_id):
        return self.get_queryset().filter(id=project_id)

    def get_all_user_projects(self, user_id):
        return (
            self.get_queryset()
            .filter(
                django.db.models.Q(
                    owner=user_id,
                )
                | django.db.models.Q(
                    members=user_id,
                ),
            )
            .distinct()
        )


__all__ = ()
