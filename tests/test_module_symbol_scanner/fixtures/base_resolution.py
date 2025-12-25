"""Test module for base class resolution."""

from django.db import models
from rest_framework import serializers


class MySerializer(serializers.Serializer):
    """A serializer inheriting from rest_framework."""

    name = serializers.CharField()


class MyModel(models.Model):
    """A model inheriting from django.db."""

    pass


class LocalBase:
    """A local base class."""

    pass


class Child(LocalBase):
    """A class inheriting from a local base."""

    pass
