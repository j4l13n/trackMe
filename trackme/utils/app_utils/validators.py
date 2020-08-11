import re
from graphql import GraphQLError


class Validators:
    """
        Validators
    """
    def __init__(self, email=None,
                 username=None,
                 phone_number=None,
                 password=None,
                 first_name=None):
        self.email = email
        self.username = username
        self.phone_number = phone_number
        self.password = password
        self.value = None
        self.first_name = first_name

    def strip_value(self, value):
        """
        Strip values of methods before validations
        Arguments:
            value: {String} any string
        """
        if value:
            self.value = value.strip()
            return self.value
        else:
            return None

    def is_email(self, email):
        """
        Validate email
        Arguments:
            email: {String} email value
        """
        self.email = self.strip_value(email)
        if re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]{2,5}$',
                    self.email) is None:
            raise GraphQLError("Invalid Email")
        return self.email

    def is_username(self, username):
        """
        Validate username
        Arguments:
            email: {String} username value
        """
        self.username = self.strip_value(username)
        if re.match(r'[a-zA-Z]', self.username) is None:
            raise GraphQLError("Invalid Username")
        return self.username

    def is_phone_number(self, phone_number):
        """
        Validate phone number
        Arguments:
            phone_number: {String} phone number value
        """
        self.phone_number = self.strip_value(phone_number)
        if re.match(r'(^[+0-9]{1,3})*([0-9]{10,11}$)',
                    self.phone_number) is None:
            raise GraphQLError("Invalid phone number")
        return self.phone_number

    def is_valid_password(self, password):
        """
        Validate password
        Arguments:
            password: {String} password value
        """
        self.password = self.strip_value(password)
        if re.match('(?=.{8,100})(?=.*[A-Z])(?=.*[0-9])',
                    self.password) is None:
            raise GraphQLError(
                'password must have at least 8 characters, '
                'a number and a capital letter.')
        return self.password

    def is_register_fields(self, username, email, phone_number, password):
        return {
            "username": self.is_username(username),
            "email": self.is_email(email),
            "phone_number": self.is_phone_number(phone_number),
            "password": self.is_valid_password(password),
        }


validator = Validators()
