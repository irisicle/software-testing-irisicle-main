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
    def run():
        login("john_doe", "Secure123!")

    benchmark(run)

def test_signup_performance(benchmark):
    def run():
        signup("user_" + str(len(user_db)), "StrongPw1@A&!")

    benchmark(run)

def test_update_profile_performance(benchmark):
    def run():
        update_profile("john_doe", name="John", email="john@new.com")

    benchmark(run)

def test_bulk_login_stress(benchmark):
    def run():
        for _ in range(100):
            login("john_doe", "Secure123!")

    benchmark(run)


