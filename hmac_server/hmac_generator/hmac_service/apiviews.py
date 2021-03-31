import hmac
import hashlib

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser
from rest_framework import status

from django.conf import settings


class GenerateHMAC(APIView):
    parser_classes = (FormParser,)

    def post(self, request, format=None, *args, **kwargs):
        """Generate an HMAC token for a request body, and return the parsed body with the HMAC signature"""
        signing_algorithm = request.headers.get("X-Hmac-Signing", "sha1")
        if signing_algorithm == "sha1":
            digestmod = hashlib.sha1
        elif signing_algorithm == "sha224":
            digestmod = hashlib.sha224
        else:
            return Response(
                "Invalid signing algorithm", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get the raw body given to us
            body = request.body.decode("utf-8")
        except UnicodeDecodeError:
            return Response("Invalid UTF8", status=status.HTTP_400_BAD_REQUEST)
        # Get the parsed body
        data = request.data.copy()

        # Make the HMAC of the raw body
        digest = hmac.new(
            settings.SECRET_KEY.encode(), body.encode(), digestmod
        ).hexdigest()

        # Update the parsed body with the digest
        data.update({"signature": digest})

        # Send it back
        return Response(data, status=status.HTTP_201_CREATED)
