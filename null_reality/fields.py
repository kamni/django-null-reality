"""
Text-based fields that respect null=False. Available fields include:

* NullableCharField
* NullableCommaSeparatedIntegerField
* NullableEmailField
* NullableSlugField
* NullableTextField
* NullableURLField

Please use these fields with a NullCheckerModel child class
"""

from django.db import models


class NullableField(models.Field):
    """
    Eliminates Django's tendency to override nulls with empty strings when you
    want a model field to respect null=False. Should be used in conjunction 
    with a child class of NullCheckerModel.
    """
    def get_default(self):
        if not self.null:
            return None
        
        # if self.null is True, will still set value to empty string to 
        # prevent issues with the database
        return super(NullableField, self).get_default()
    
    def south_field_triple(self):
        """Makes this field compatible with south, if installed"""
        try:
            from south.modelsinspector import introspector
        except ImportError:
            # apparently we don't need to worry about South
            return "", (), {}
        
        parent_cls = type(self).__bases__[0]
        field_class = ".".join((parent_cls.__module__, parent_cls.__name__))
        args, kwargs = introspector(self)
        return field_class, args, kwargs


class NullableCharField(models.CharField, NullableField):
    pass


class NullableCommaSeparatedIntegerField(models.CommaSeparatedIntegerField, NullableField):
    pass


class NullableEmailField(models.EmailField, NullableField):
    pass


class NullableSlugField(models.SlugField, NullableField):
    pass


class NullableTextField(models.TextField, NullableField):
    pass


class NullableURLField(models.URLField, NullableField):
    pass


NULLABLE_FIELDS = (NullableField, NullableCharField, 
                   NullableCommaSeparatedIntegerField, NullableEmailField,
                   NullableSlugField, NullableTextField, NullableURLField)

