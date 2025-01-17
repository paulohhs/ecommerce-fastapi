import pytest
from app.schemas.product import Product, ProductInput


def test_product_schema():
    product = Product(
        name="Produto Teste",
        slug="produto-teste",
        price=22.99,
        stock=22,
    )

    assert product.dict() == {
        "name": "Produto Teste",
        "slug": "produto-teste",
        "price": 22.99,
        "stock": 22,
    }


def test_product_schema_invalid_slug():
    with pytest.raises(ValueError):
        product = Product(
            name="Produto Teste",
            slug="produto teste",
            price=22.99,
            stock=22,
        )
        
    with pytest.raises(ValueError):
        product = Product(
            name="Produto Teste",
            slug="próduto",
            price=22.99,
            stock=22,
        )
        
    with pytest.raises(ValueError):
        product = Product(
            name="Produto Teste",
            slug="Produto-teste",
            price=22.99,
            stock=22,
        )


def test_product_schema_invalid_price():
    with pytest.raises(ValueError):
        product = Product(
            name="Produto Teste",
            slug="produto-teste",
            price=0,
            stock=22,
        )


def test_product_input_schema():
    product = Product(
        name="Produto Teste",
        slug="produto-teste",
        price=22.99,
        stock=22,
    )

    product_input = ProductInput(
        category_slug="categoria-teste",
        product=product
    )

    assert product_input.dict() == {
        "category_slug": "categoria-teste",
        "product": {
            "name": "Produto Teste",
            "slug": "produto-teste",
            "price": 22.99,
            "stock": 22,
        }
    }
