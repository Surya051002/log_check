def login(username, password):
    user = database.find_user(username)

    if user.password == password:
        return {"token": generate_token(user)}

    return {"error": "Invalid credentials"}