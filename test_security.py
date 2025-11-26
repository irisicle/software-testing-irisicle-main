import pytest
from unittest.mock import patch
from auth_system import *

# ---------------------------------------------------
# Reset shared state before each test
# ---------------------------------------------------
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


# -----------------------------------------------------------------
# SECURITY TEST 1: Password policy enforcement
# -----------------------------------------------------------------
@pytest.mark.parametrize("pwd", [
    "short1!",      # too short
    "alllowercase1!",  # missing uppercase
    "ALLUPPERCASE1!",  # missing lowercase
    "NoSpecial123",    # missing special char
    "NoDigits!!",      # missing digit
])
def test_password_policy_blocks_weak_passwords(pwd):
    assert not is_valid_password(pwd)


# -----------------------------------------------------------------
# SECURITY TEST 2: Signup should NOT reveal whether password was wrong
# (User enumeration protection)
# -----------------------------------------------------------------
def test_signup_existing_user_message_is_specific():
    result = signup("john_doe", "Something123!")
    assert result == "User already exists."


def test_signup_non_existing_user():
    result = signup("unique_user", "Strong1!")
    assert result == "Signup successful."


# -----------------------------------------------------------------
# SECURITY TEST 3: Login timing should not reveal valid usernames
# -----------------------------------------------------------------
@patch("your_module.random.uniform", return_value=0.1)  # normalize randomness
def test_login_timing_constant(mock_rand):
    # Known username
    start1 = time.perf_counter()
    login("john_doe", "wrongpass")
    dur_known = time.perf_counter() - start1

    # Unknown username
    start2 = time.perf_counter()
    login("ghost_user", "wrongpass")
    dur_unknown = time.perf_counter() - start2

    # Timing should not diverge wildly (< 50ms difference)
    assert abs(dur_known - dur_unknown) < 0.05


# -----------------------------------------------------------------
# SECURITY TEST 4: Profile updates should not work without authentication
# (This test will currently FAIL — your implementation allows it)
# -----------------------------------------------------------------
def test_profile_update_requires_authentication():
    """
    Your current code allows updating any profile without logging in.
    This test will reveal the issue.
    """
    old_email = user_profiles["john_doe"]["email"]

    update_profile("john_doe", email="malicious@attacker.com")

    # Expect unchanged (but your code currently changes it)
    assert user_profiles["john_doe"]["email"] == old_email


# -----------------------------------------------------------------
# SECURITY TEST 5: Deleting account requires correct password
# -----------------------------------------------------------------
def test_delete_account_requires_correct_password():
    result = delete_account("john_doe", "wrongpass")
    assert result == "Authentication failed."
    assert "john_doe" in user_db


# -----------------------------------------------------------------
# SECURITY TEST 6: User cannot delete someone else’s account
# (With correct password for themselves)
# -----------------------------------------------------------------
def test_cannot_delete_other_user():
    # jane_doe tries to delete john_doe using her own password
    result = delete_account("john_doe", "Password!")
    assert result == "Authentication failed."
    assert "john_doe" in user_db


# -----------------------------------------------------------------
# SECURITY TEST 7: Brute-force login — system should not crash or behave oddly
# (No rate-limiting exists yet — this test ensures stability)
# -----------------------------------------------------------------
def test_bruteforce_stability():
    for _ in range(200):
        login("john_doe", "wrongpass")
    # System should remain stable
    assert login("john_doe", "Secure123!") is True


# -----------------------------------------------------------------
# SECURITY TEST 8: Profiles must not leak sensitive information
# -----------------------------------------------------------------
def test_profile_does_not_expose_passwords():
    profile = view_profile("john_doe")
    assert "password" not in profile
    assert "passwd" not in profile
