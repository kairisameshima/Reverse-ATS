def test_get_all_applications(client):
    response = client.get("/application/all")
    assert response.status_code == 200
    assert response.json == {"applications": []}
