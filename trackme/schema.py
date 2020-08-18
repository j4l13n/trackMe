import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug

from trackme.apps.authentication.schema.mutations.auth_mutations import \
    Mutation as AuthMutations
from trackme.apps.tracking.schema.mutations.tracking_mutation import \
    Mutation as TrackMutations
from trackme.apps.tracking.schema.queries.tracking_queries import \
    Query as TrackQueries


class Query(
    graphene.ObjectType,
    TrackQueries):
    debug = graphene.Field(DjangoDebug, name='_debug')
    pass


class Mutation(
    AuthMutations,
    TrackMutations):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(mutation=Mutation, query=Query)
