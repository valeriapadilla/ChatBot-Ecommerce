def test_chat_message(client):
    # Login primero
    login_resp = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Enviar mensaje al chat
    response = client.post("/api/chat/message", json={
        "message": "How many computers are available?"
    }, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data 