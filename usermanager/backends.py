from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("Auth backend received:", username, password)
        if username is None or password is None:
            print("Either username or password is None")
            return None

        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
            print("Found user:", user, "is_active?", user.is_active)
        except UserModel.DoesNotExist:
            print("No user found for:", username)
            return None

        # Test password check
        pw_ok = user.check_password(password)
        print("Password check:", pw_ok)

        can_auth = self.user_can_authenticate(user)
        print("User can_authenticate:", can_auth)

        if pw_ok and can_auth:
            print("Authentication successful!")
            return user

        print("Authentication failed after checks")
        return None