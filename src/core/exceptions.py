from fastapi import HTTPException


class ObjectDoesNotExist(Exception):
    pass


class TooBigRequest(Exception):
    pass


class CredentialsException(HTTPException):
    pass
