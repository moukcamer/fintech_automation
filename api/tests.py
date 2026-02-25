from django.contrib.auth import get_user_model
import uuid

User = get_user_model()
def create_test_user():
    return User.objects.create_user(
        email=f"user_{uuid.uuid4()}@example.com",
        password="1234"
)





