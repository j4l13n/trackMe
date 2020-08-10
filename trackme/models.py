from django.db import models
from django.conf import settings

from .manager import BaseManager
from trackme.utils.app_utils.generetors import ID_LENGTH, id_generater

class BaseModel(models.Model):
    """
    Base model for all models in the system

    Args:
        created_at: Holds date/time for when an object was created.
        updated_at: Holds date/time for last update on an object.
        deleted_at: Holds date/time for soft-deleted objects.
        deleted_by: Holds user who soft-deleted an objects.
    """
    id = models.CharField(
        max_length=ID_LENGTH,
        default=id_generater, 
        primary_key=True,
        editable=False)
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now_add=True, null=True)
    delete_at = models.DateField(auto_now_add=True, null=True)
    delete_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE, blank=True,
                                  null=True)

    objects = BaseManager()
    all_objects = BaseManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, user=None):
        self.deleted_at = timezone.now()
        if user is not None:
            self.deleted_by = user
        self.save()

    def hard_delete(self):
        super(BaseModel, self).delete()

    def can_be_deleted_by(self, user, user_column="user"):
        """
        Check if a user can delete this instance
        Args:
            user(Object): user instance
            user_column(str): user column name, the foreign key
                            used to reference the user if not provided
                            'user' will be considered
        Returns:
            True: if the user is an admin or is the owner of this instance
                else False
        """

        if getattr(self, user_column, None) == user or user.is_admin:
            return True
        return False


