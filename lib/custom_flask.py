from flask import Flask
from lib.response import JsonResponse


class CustomFlask(Flask):
    response_class = JsonResponse
