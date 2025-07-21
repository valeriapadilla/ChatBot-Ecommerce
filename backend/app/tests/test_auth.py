def test_signup_and_login(client):
    # Signup
    response = client.post("/api/auth/signup", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 201 or response.status_code == 400  # 400 si el usuario ya existe

    # Login
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data 