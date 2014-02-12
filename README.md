# django-null-reality

Django currently ignores null=False in text-based field validation, and
instead automatically converts None to an empty string. Django's admin
interface does catch empty fields that aren't supposed to be empty; however if
you have an app that relies on custom interfaces that create models
programmatically, you may run into situations where Django silently commits
models to the database when None values are passed, instead of throwing the
expected IntegrityError.

This project is intended to address this issue so that text-based fields throw
IntegrityErrors when None values are passed, just like other Django model
fields.

## Background and an Explanation of How this Works

Some databases do not allow NULL values to be stored for text-based fields. So
Django has made the very logical decision to default text-based fields to an
empty string in order to avoid conflicts.

However, as explained above, this can lead to unexpected behavior where Django
silently commits None values to the database as blank strings instead of
failing. This can then cascade to other errors when you have unique=True set on
the field, and can lead to difficulties troubleshooting bugs related to None
values when you actually do want to store blank strings in some cases.

This project provides an abstract model class and a series of nullable
text-based fields (explained in 'Usage' below). To remain compatible with
Django's choice to prevent errors with certain databases, the nullable fields
still set None values to an empty string if null=True. If null=False, the
fields leave None values alone, so it can then be used for validation purposes
during save. The abstract model class then overrides the default save method so
that it raises an IntegrityError if a None value is present and null=False for
that field, prior to it hitting a database that might not support null values.

In other words, this project provides the best of both worlds: null=False
validation and protection from databases that don't support NULL values for
text-based fields.

## Installation

This project is still in pre-alpha and is only available from github:

    pip install -e git+git://github.com/kamni/django-null-reality#egg=django-null-reality

## Usage

For models where you want to have null checking, simply subclass
NullCheckerModel and use the desired nullable fields from fields.py:

    from django.db import models
    from null_reality.models import NullCheckerModel
    from null_reality.fields import NullableCharField, NullableTextField

    class Beer(NullCheckerModel):
        name = NullableCharField(max_length=100, unique=True)
        rating = models.PositiveIntegerField(default=1)
        description = NullableTextField()

If you only want null checking on some of the fields of a model, it is
possible to mix and match fields, and the NullCheckerModel subclass will only
check against nullable fields:

    class MixTape(NullCheckerModel):
        name = NullableCharField(max_length=150, unique=True)
        message = models.CharField(max_length=255)

The field and model classes also will respect the possibility that you may want
blank strings in your text-based field -- they only check for None values. So
the following would raise an IntegrityError:

    beer = Beer.objects.create()

But this code would not:

    beer = Beer.objects.create(name='', description='')

Additionally, if you allow null fields, it will follow the Django practice of
converting None to a blank string:

    class Beer(NullCheckerModel):
        name = NullableCharField(max_length=100, unique=True, blank=True, null=True)

    beer = Beer.objects.create()
    beer.name    # u''
