import random
import uuid


def create_id():
    return random.randint(1000000, 100000000000000)


def generate_uuid():
    return uuid.uuid4()
