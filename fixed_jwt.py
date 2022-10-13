from rest_framework_simplejwt.authentication import JWTAuthentication

HTTP_HEADER_ENCODING = 'iso-8859-1'


class FixedJWTAuthentication(JWTAuthentication):
    """
    JWTAuthentication с исправленным парсингом токена.
    """

    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.GET.get("Authorization")

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header
