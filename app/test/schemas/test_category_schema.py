import pytest
from app.schemas.category import Category


def test_category_schema():
    category = Category(
        name="Categoria Teste",
        slug="categoria-teste"
    )

    assert category.dict() == {
        "name": "Categoria Teste",
        "slug": "categoria-teste"
    }


def test_category_schema_invalid_slug():
    with pytest.raises(ValueError):
        category = Category(
        name="Categoria Teste",
        slug="categoria teste"
    )
        
    with pytest.raises(ValueError):
        category = Category(
        name="Categoria Teste",
        slug="cãt"
    )
        
    with pytest.raises(ValueError):
        category = Category(
        name="Categoria Teste",
        slug="Categoria"
    )
