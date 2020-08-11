import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug

from trackme.apps.authentication.schema.mutations.auth_mutations import \
    Mutation as AuthMutations


class Query(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')
    pass


class Mutation(AuthMutations):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(mutation=Mutation, query=Query)
