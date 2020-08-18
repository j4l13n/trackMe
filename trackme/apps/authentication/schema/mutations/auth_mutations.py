import graphene

from .register_user import RegisterUser
from .login_user import LoginUser
from .user_agreement import Agreement


class Mutation(graphene.ObjectType):
    register = RegisterUser.Field()
    login = LoginUser.Field()
    agreement = Agreement.Field()
