import pytest
from auth_system import *

@pytest.fixture(autouse=True)
def reset_data():
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

def test_login_success():
    assert login("john_doe", "Secure123!") is True
    assert user_profiles["john_doe"]["last_login"] is not None

def test_login_failure():
    assert login("john_doe", "wrong") is False

def test_signup_success():
    msg = signup("new_user", "Password123!")
    assert msg == "Signup successful."
    assert "new_user" in user_db

def test_signup_user_exists():
    msg = signup("john_doe", "Secure123!")
    assert msg == "User already exists."

def test_signup_invalid_password():
    msg = signup("someone", "weak")
    assert msg == "Invalid password format."

def test_valid_password():
    assert is_valid_password("Strong1!")

def test_invalid_password_no_uppercase():
    assert not is_valid_password("password")

def test_invalid_password_no_special():
    assert not is_valid_password("Password123")

def test_invalid_password_too_short():
    assert not is_valid_password("pw")

def test_send_reset_email_email_not_set():
    user_profiles["john_doe"]["email"] = None
    assert send_reset_email("john_doe") == "Email not set."

def test_send_reset_email_user_not_found():
    assert send_reset_email("ghost") == "User not found."

def test_view_profile_success():
    profile = view_profile("john_doe")
    assert profile["name"] == "John"

def test_view_profile_not_found():
    assert view_profile("ghost") == "Profile not found."

def test_update_profile_name():
    update_profile("john_doe", name="John")
    assert user_profiles["john_doe"]["name"] == "John"

def test_update_profile_email():
    update_profile("john_doe", email="new@email.com")
    assert user_profiles["john_doe"]["email"] == "new@email.com"

def test_update_profile_user_not_found():
    assert update_profile("ghost") == "User not found."

def test_delete_account_success():
    msg = delete_account("john_doe", "Secure123!")
    assert msg == "Account deleted."
    assert "john_doe" not in user_db
    assert "john_doe" not in user_profiles

def test_delete_account_auth_failed():
    assert delete_account("john_doe", "wrong") == "Authentication failed."

