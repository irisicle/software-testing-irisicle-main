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

@pytest.mark.parametrize("pwd", [
    "short1!",         # too short
    "alllowercase1!",  # missing uppercase
    "ALLUPPERCASE1!",  # missing lowercase
    "NoSpecial123",    # missing special char
    "NoDigits!",       # missing digit
])

def test_password_policy_block_weak_passwords(pwd):
    assert not is_valid_password(pwd)

def test_signup_existing_user():
    result = signup("john_doe", "Something123!")
    assert result == "User already exists."

def test_signup_non_existing_user():
    result = signup("new_user", "Strong1!")
    assert result == "Signup successful."

def test_login_timing_constant():
    # Existing user
    start1 = time.perf_counter()
    login("john_doe", "wrongpw")
    dur_known = time.perf_counter() - start1
    # Unknown user
    start2 = time.perf_counter()
    login("ghost_user", "wrongpw")
    dur_unknown = time.perf_counter() - start2

    assert abs(dur_known - dur_unknown) < 0.05

def test_delete_account():
    result = delete_account("john_doe", "wrongpw")
    assert result == "Authentication failed."
    assert "john_doe" in user_db

def test_cannot_delete_other_user():
    result = delete_account("john_doe", "Password!")
    assert result == "Authentication failed."
    assert "john_doe" in user_db

def test_bruteforce_stability():
    for _ in range(200):
        login("john_doe", "wrongpw")
    assert login("john_doe", "Secure123!") is True

def test_profile_does_not_expose_passwords():
    profile = view_profile("john_doe")
    assert "password" not in profile
    assert "passwd" not in profile
