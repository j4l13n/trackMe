import graphene
from django.contrib.gis.geos import Point
from graphql_jwt.decorators import login_required
from ..types.traking_types import LocationInput, TrackType
from ...models import Tracking
from trackme.utils.app_utils.validators import validator


class TrackMutation(graphene.Mutation):
    """
    Tracking mutation for saving user's location

    Args:
        device (str): device id that was tracked
        geometry (dic): dictionary of lon and lat values
    """
    success = graphene.String()
    track = graphene.Field(TrackType)

    class Arguments:
        device = graphene.String(required=True)
        geometry = graphene.Argument(LocationInput, required=True)

    @login_required
    def mutate(self, info, **kwargs):
        # declare variables
        user = info.context.user
        device = kwargs.get('device')
        geometry = kwargs.get('geometry')

        # validate geometry daca
        geometry = validator.check_geometry_point(
            geometry['lon'],
            geometry['lat']
        )

        # create the point using the geometry info
        geometry = Point(geometry['lon'], geometry['lat'])

        # save data in the db
        track = Tracking(
            geometry=geometry,
            device=device
        )
        track.user = user
        track.save()
        success = "You have added your location successfully"
        return TrackMutation(
            success=success, track=track)


class Mutation(graphene.ObjectType):
    tracking = TrackMutation.Field()
