from django.contrib.auth.models import update_last_login
from graphql_jwt.utils import jwt_encode, jwt_payload
from rest_framework.authtoken.models import Token


def generate_tokens(user):
    """
    generate tokens
    Args:
        user(Object): user's object from the database
    Returns:
        token, rest_token(tuple)
    """
    update_last_login(sender=None, user=user)

    # token to access GraphQL-based views
    payload = jwt_payload(user)
    token = jwt_encode(payload)

    return token
