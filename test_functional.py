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

def test_full_signup_login_profile_flow():
    msg = signup("new_user", "Password123!")
    assert msg == "Signup successful."
    assert "new_user" in user_db
    assert login("new_user", "Password123!") is True
    assert user_profiles["new_user"]["last_login"] is not None
    profile = view_profile("new_user")
    assert profile["name"] == "new_user"
    assert profile["email"] is None

def test_update_profile_flow():
    assert login("john_doe", "Secure123!") is True
    msg = update_profile("john_doe", name="John", email="john@email.com")
    assert msg == "Profile updated successfully."
    profile = view_profile("john_doe")
    assert profile["name"] == "John"
    assert profile["email"] == "john@email.com"

def test_delete_account_flow():
    assert login("john_doe", "Secure123!") is True
    msg = delete_account("john_doe", "Secure123!")
    assert msg == "Account deleted."
    assert "john_doe" not in user_db
    assert "john_doe" not in user_profiles

def test_invalid_login_attempts():
    assert login("john_doe", "wrong_password") is False
    assert login("ghost_user", "anything") is False

def test_signup_existing_user():
    result = signup("john_doe", "Password123!")
    assert result == "User already exists."

def test_signup_invalid_password():
    result = signup("someone", "password")
    assert result == "Invalid password format."

def test_view_profile_not_found():
    assert view_profile("ghost") == "Profile not found."
