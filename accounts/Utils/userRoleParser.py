
import os
from InacheBackend import settings
from accounts.models import UserRoleFactory
import jwt


def parser(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[1]
        # print(DJANGO_SETTINGS_MODULE,ENVIRONMENT)
        environment = os.getenv('DJANGO_SETTINGS_MODULE', 'dev')
        env=environment.split('.')[2]
        if env == 'staging':
            secret_key = settings.staging.SECRET_KEY
        elif env == 'dev':
            secret_key = settings.dev.SECRET_KEY
        elif env == 'production':
            secret_key = settings.production.SECRET_KEY
        # Secret key used to sign the JWT token
        # secret_key=settings.staging.SECRET_KEY
        
        # Decode the JWT token
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        # Access the information from the token
        role_id = decoded_token.get("role_id") 
        if role_id is None:
            return None
        userRole=UserRoleFactory.objects.get(id=role_id)
    except IndexError as e:
        return None

    return userRole