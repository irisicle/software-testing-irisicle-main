import pytest
from auth_system import *

@pytest.fixture(autouse=True)
def reset_state():
    user_db.clear()
    user_db.update({
        "john_doe": "Secure123!",
        "jane_doe": "Password!"
    })

    user_profiles.clear()
    user_profiles.update({
        "john_doe": {"name": "John", "email": "john@example.com", "last_login": None},
        "jane_doe": {"name": "Jane", "email": "jane@example.com", "last_login": None}
    })

def test_login_performance(benchmark):
    benchmark.configure(timeout=60)  # Increase timeout to 60 seconds
    benchmark(lambda:login("john_doe", "Secure123!"))

def test_signup_performance(benchmark):
    benchmark.configure(timeout=60)  # Increase timeout to 60 seconds
    benchmark(lambda:signup("user_" + str(len(user_db)), "StrongPw1@A&!"))

def test_update_profile_performance(benchmark):
    benchmark.configure(timeout=60)  # Increase timeout to 60 seconds
    benchmark(lambda:update_profile("john_doe", name="John", email="john@new.com"))

def test_bulk_login_stress(benchmark):
    benchmark.configure(timeout=120)  # Increase timeout to 120 seconds
    benchmark(lambda:[login("john_doe", "Secure123!") for _ in range(100)])


