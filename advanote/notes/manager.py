import django.db.models.manager


class NoteManager(django.db.models.manager.Manager):
    def get_user_notes(self, user_id):
        return self.get_queryset().filter(owner=user_id)


__all__ = ()
