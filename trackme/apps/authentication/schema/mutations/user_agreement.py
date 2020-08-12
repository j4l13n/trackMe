import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from trackme.utils.app_utils.database import get_model_object
from ...models import User
from trackme.utils.app_utils.validators import validator


class Agreement(graphene.Mutation):
    """
    Agreement mutation allow a user to accept the agreement

    Args:
        agreement (str): agreement value

    Returns:
        success: success message after agreement sent
    """
    success = graphene.String()

    class Arguments:
        agreement = graphene.String(required=True)

    @login_required
    def mutate(self, info, **kwargs):
        # declare variables
        user = info.context.user
        agreement = kwargs.get("agreement")

        user_instance = get_model_object(User, 'id', user.id)

        # check if agreement is valid
        agreement = validator.is_valid_agreement(agreement)

        # add agreement to the model
        user_instance.agreement = agreement
        user_instance.save()

        agree_res = user_instance.agreement

        if agree_res == "DIS":
            agree_res = "Disallowed"
        elif agree_res == "AL":
            agree_res = "Allowed"
        else:
            raise GraphQLError("\
                Something went wrong updating agreement")

        success = "You have updated you agreement to {}".format(
            agree_res)
        return Agreement(success=success)
