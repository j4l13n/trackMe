import graphene
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from trackme.utils.app_utils.validators import validator
from trackme.utils.app_utils.generetors import Token
from trackme.utils.messages.auth_messages import \
    AUTH_SUCCESS_RESPONSES, AUTH_ERROR_RESPONSES
from ..types.auth_types import UserType



class RegisterUser(graphene.Mutation):
    """
    Mutation to register a user

    - Args:
        - username: String!
        - email: String!
        - phone_number: String!
        - password: String!

    - Returns:
        - user (User): return a registered user
        - success (Array): return success messages
        - errors (Array): return error messages
    """
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.List(graphene.String)
    errors = graphene.List(graphene.String)

    def mutate(self, info, **kwargs):
        # declare variables
        username = kwargs.get("username")
        email = kwargs.get("email")
        phone_number = kwargs.get("phone_number")
        password = kwargs.get("password")

        validate_fields = validator.is_register_fields(
            username,
            email,
            phone_number,
            password
        )

        try:
            user = get_user_model().objects.create_user(**validate_fields)
            user.is_active = True
            success = [AUTH_SUCCESS_RESPONSES['register_success']]
            user.save()
            return RegisterUser(
                success=success,
                user=user
            )
        except Exception as e:
            errors = [AUTH_ERROR_RESPONSES["register_error"].format(e)]
            return RegisterUser(errors=errors)
