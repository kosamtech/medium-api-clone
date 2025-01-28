from rest_framework import status
from rest_framework.exceptions import APIException


class CantFollowYourself(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You can't follow yourself."
    default_code = "forbidden"
