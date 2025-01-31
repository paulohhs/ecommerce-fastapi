import pytest
from fastapi.exceptions import HTTPException
from app.db.models import Product as ProductModel
from app.schemas.product import Product, ProductOutput
from app.use_cases.product import ProductUseCases


def test_add_product_uc(db_session, categories_on_db):
    product = Product(
        name="Produto Teste",
        slug="produto-teste",
        price=22.99,
        stock=22,
    )

    uc = ProductUseCases(db_session)
    uc.add_product(product=product, category_slug=categories_on_db[0].slug)

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 1
    assert products_on_db[0].name == product.name
    assert products_on_db[0].slug == product.slug
    assert products_on_db[0].price == product.price
    assert products_on_db[0].stock == product.stock
    assert products_on_db[0].category.name == categories_on_db[0].name

    db_session.delete(products_on_db[0])
    db_session.commit()


def test_add_product_uc_invalid_category(db_session):
    product = Product(
        name="Produto Teste",
        slug="produto-teste",
        price=22.99,
        stock=22,
    )

    uc = ProductUseCases(db_session)

    with pytest.raises(HTTPException):
        uc.add_product(product=product, category_slug='invalid')


def test_update_product_uc(db_session, product_on_db):
    product = Product(
        name="Produto Atualizado",
        slug="produto-atualizado",
        price=22.99,
        stock=22,
    )

    uc = ProductUseCases(db_session)
    uc.update_product(id=product_on_db.id, product=product)

    product_updated_on_db = db_session.query(ProductModel).filter_by(id=product_on_db.id).first()

    assert product_updated_on_db is not None
    assert product_updated_on_db.name == product.name
    assert product_updated_on_db.slug == product.slug
    assert product_updated_on_db.price == product.price
    assert product_updated_on_db.stock == product.stock


def test_update_product_uc_invalid_id(db_session):
    product = Product(
        name="Produto Atualizado",
        slug="produto-atualizado",
        price=22.99,
        stock=22,
    )

    uc = ProductUseCases(db_session)

    with pytest.raises(HTTPException):
        uc.update_product(id=1, product=product)


def test_delete_product_uc(db_session, product_on_db):
    uc = ProductUseCases(db_session=db_session)
    uc.delete_product(id=product_on_db.id)

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 0


def test_delete_product_uc_non_exist(db_session):
    uc = ProductUseCases(db_session=db_session)

    with pytest.raises(HTTPException):
        uc.delete_product(id=1)


def test_list_products_uc(db_session, products_on_db):
    uc = ProductUseCases(db_session=db_session)

    products = uc.list_products()

    for product in products_on_db:
        db_session.refresh(product)

    assert len(products) == 4
    assert type(products[0]) == ProductOutput
    assert products[0].id == products_on_db[0].id
    assert products[0].name == products_on_db[0].name
    assert products[0].slug == products_on_db[0].slug
    assert products[0].price == products_on_db[0].price
    assert products[0].stock == products_on_db[0].stock
    assert products[0].category.name == products_on_db[0].category.name


def test_list_products_uc_with_search(db_session, products_on_db):
    uc = ProductUseCases(db_session=db_session)

    products = uc.list_products(search="um")

    for product in products_on_db:
        db_session.refresh(product)

    assert len(products) == 1
    assert type(products[0]) == ProductOutput
    assert products[0].id == products_on_db[0].id
    assert products[0].name == products_on_db[0].name
    assert products[0].slug == products_on_db[0].slug
    assert products[0].price == products_on_db[0].price
    assert products[0].stock == products_on_db[0].stock
    assert products[0].category.name == products_on_db[0].category.name
