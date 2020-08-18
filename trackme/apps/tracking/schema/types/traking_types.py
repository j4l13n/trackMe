import graphene
import json
from graphene_django import DjangoObjectType
from django.contrib.gis.db import models
from graphene_django.converter import convert_django_field
from ...models import Tracking


class JSON(graphene.Scalar):
    @classmethod
    def serialize(cls, value):
        return json.loads(value.geojson)


@convert_django_field.register(models.PointField)
def convert_field_to_geojson(field, registry=None):
    return graphene.Field(
        JSON,
        description=field.help_text,
        required=not field.null)


class LocationInput(graphene.InputObjectType):
    lat = graphene.Float()
    lon = graphene.Float()


class TrackType(DjangoObjectType):
    """
    Tracking mode type
    """
    class Meta:
        model = Tracking
