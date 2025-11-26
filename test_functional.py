import pytest
from unittest.mock import patch
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
    msg = signup("new_user", "Valid123!")
    assert msg == "Signup successful."
    assert "new_user" in user_db

    assert login("new_user", "Valid123!") is True
    assert user_profiles["new_user"]["last_login"] is not None

    profile = view_profile("new_user")
    assert profile["name"] == "new_user"
    assert profile["email"] is None

@patch("your_module.smtplib.SMTP")
def test_password_reset_flow(mock_smtp):
    result = send_reset_email("john_doe")
    assert result == "Password reset email sent."
    assert mock_smtp.called

def test_update_profile_flow():
    assert login("john_doe", "Secure123!") is True

    msg = update_profile("john_doe", name="Johnny", email="johnny@mail.com")
    assert msg == "Profile updated successfully."

    profile = view_profile("john_doe")
    assert profile["name"] == "Johnny"
    assert profile["email"] == "johnny@mail.com"

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
    result = signup("john_doe", "Something123!")
    assert result == "User already exists."


def test_signup_invalid_password():
    result = signup("someone", "weak")
    assert result == "Invalid password format."

def test_view_profile_not_found():
    assert view_profile("ghost") == "Profile not found."

@patch("your_module.smtplib.SMTP")
def test_password_reset_no_email(mock_smtp):
    user_profiles["jane_doe"]["email"] = None
    result = send_reset_email("jane_doe")
    assert result == "Email not set."
    mock_smtp.assert_not_called()
