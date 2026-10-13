from simple_source import login


def test_login_with_empty_password():
    result = login("surya", "")

    assert result == {"error": "Bad Request"}