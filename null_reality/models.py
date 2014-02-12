from django.db import models, IntegrityError

from null_reality.fields import NULLABLE_FIELDS


class NullCheckerModel(models.Model):
    """
    By default, Django does not respect the null=False requirement on CharField
    and instead inserts an empty string.  For sane people who actually want
    CharFields to throw IntegrityErrors if the value for the field is None,
    use this class.
    
    Notes:
        If you use Django's default text-based fields (e.g., CharField,
        TextField) with NullCheckerModel, it will respect Django's default
        behaviors for those fields. To get the null checking behaviors 
        promised by this class, please use the nullable field classes in
        fields.py
    """
    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if type(field) in NULLABLE_FIELDS and getattr(self, field.name) is None:
                    raise IntegrityError("%s.%s may not be null" %
                                         (self._meta.db_table, field.name))
        super(NullCheckerModel, self).save(*args, **kwargs)
    
    class Meta:
        abstract = True