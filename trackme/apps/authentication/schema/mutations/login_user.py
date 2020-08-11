import graphene
from graphql import GraphQLError
from django.contrib.auth import authenticate

from ..types.auth_types import UserType
from ...models import User
from trackme.utils.messages.auth_messages import \
    AUTH_ERROR_RESPONSES, AUTH_SUCCESS_RESPONSES
from trackme.utils.auth_utils.tokens import generate_tokens


class LoginUser(graphene.Mutation):
    """
    Login a user with their credentials
    args:
        email(str): user's email
        password(str): user's password
    returns:
        success(str): success messsage confirming login
        token(str): JWT authorization token used to validate the login
        user(obj): 'User' object containing details of the logged in user
    """

    success = graphene.String()
    token = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        success = AUTH_ERROR_RESPONSES["invalid_credentials"]

        user = User.objects.filter(email=email).first()

        if not user:
            raise GraphQLError(success)

        if user.is_active:
            user_auth = authenticate(username=email, password=password)

            if not user_auth:
                raise GraphQLError(_(message))

            success = AUTH_SUCCESS_RESPONSES["login_success"]

            token = generate_tokens(user_auth)

            return LoginUser(success=success, token=token, user=user_auth)
                             
        return GraphQLError(AUTH_ERROR_RESPONSES["not_active"])
