import graphene

from .register_user import RegisterUser
from .login_user import LoginUser

class Mutation(graphene.ObjectType):
    register = RegisterUser.Field()
    login = LoginUser.Field()
