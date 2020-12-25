from django.utils.crypto import get_random_string


def create_unique_code(obj):
    random_code = get_random_string(32)
    while type(obj).objects.filter(code=random_code).exists():
        random_code = get_random_string(32)
    return random_code