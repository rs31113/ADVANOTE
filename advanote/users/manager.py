import django.contrib.auth.models
import django.db.models


class UserManager(django.contrib.auth.models.UserManager):
    def active(self):
        return (
            self.get_queryset()
            .filter(is_active=True)
            .select_related("profile")
        )

    def get_user(self, user_id):
        return (
            self.get_queryset()
            .filter(id=user_id)
            .select_related("profile")
            .only(
                "profile__birthday",
                "email",
                "first_name",
                "last_name",
                "username",
            )
        )


__all__ = ()
