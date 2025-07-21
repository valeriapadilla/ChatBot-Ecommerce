def test_get_products(client):
    response = client.get("/api/products/")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)


def test_get_product_detail(client):
    response = client.get("/api/products/")
    products = response.json()
    if products:
        product_id = products[0]["id"]
        detail_response = client.get(f"/api/products/{product_id}")
        assert detail_response.status_code == 200
        product = detail_response.json()
        assert "name" in product
        assert "price" in product 