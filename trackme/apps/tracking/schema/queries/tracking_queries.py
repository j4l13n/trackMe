import graphene
from ...schema.types.traking_types import TrackType
from ...models import Tracking


class Query(graphene.AbstractType):
    all_tracks = graphene.List(TrackType)

    def resolve_all_tracks(self, info, **kwargs):
        return Tracking.objects.all()
