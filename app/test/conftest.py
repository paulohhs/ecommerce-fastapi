import pytest
from passlib.context import CryptContext
from app.db.connection import Session
from app.db.models import Category as CategoryModel
from app.db.models import Product as ProductModel
from app.db.models import User as UserModel


crypt_context = CryptContext(schemes=['sha256_crypt'])


@pytest.fixture()
def db_session():
    try:
        session = Session()
        
        yield session
    finally:
        session.close()


@pytest.fixture()
def category_on_db(db_session):
    category = CategoryModel(name="Categoria Teste", slug="categoria-teste")

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    yield category

    db_session.delete(category)
    db_session.commit()


@pytest.fixture()
def categories_on_db(db_session):
    categories = [
        CategoryModel(name="Categoria Teste Um", slug="categoria-teste-um"),
        CategoryModel(name="Categoria Teste Dois", slug="categoria-teste-dois"),
        CategoryModel(name="Categoria Teste Tres", slug="categoria-teste-tres"),
        CategoryModel(name="Categoria Teste Quatro", slug="categoria-teste-quatro"),
    ]

    for category in categories:
        db_session.add(category)
    db_session.commit()

    for category in categories:
        db_session.refresh(category)

    yield categories

    for category in categories:
        db_session.delete(category)
    db_session.commit()


@pytest.fixture()
def product_on_db(db_session):
    category = CategoryModel(name="Categoria Teste", slug="categoria-teste")
    db_session.add(category)
    db_session.commit()

    product = ProductModel(
        name="Produto Teste", 
        slug="produto-teste",
        price=99.99,
        stock=20,
        category_id=category.id
    )

    db_session.add(product)
    db_session.commit()

    yield product

    db_session.delete(product)
    db_session.delete(category)
    db_session.commit()


@pytest.fixture()
def products_on_db(db_session):
    category = CategoryModel(name="Categoria Teste", slug="categoria-teste")
    db_session.add(category)
    db_session.commit()

    products = [
        ProductModel(name="Produto Teste Um", slug="produto-teste-um", price=9.99, stock=10, category_id=category.id),
        ProductModel(name="Produto Teste Dois", slug="produto-teste-dois", price=12.99, stock=12, category_id=category.id),
        ProductModel(name="Produto Teste Tres", slug="produto-teste-tres", price=15.99, stock=15, category_id=category.id),
        ProductModel(name="Produto Teste Quatro", slug="produto-teste-quatro", price=19.99, stock=18, category_id=category.id),
    ]

    for product in products:
        db_session.add(product)
    db_session.commit()

    for product in products:
        db_session.add(product)
    db_session.commit()

    for product in products:
        db_session.refresh(product)

    yield products

    for product in products:
        db_session.delete(product)

    db_session.delete(category)
    db_session.commit()


@pytest.fixture()
def user_on_db(db_session):
    user = UserModel(username="UsuarioTeste", password=crypt_context.hash("pass#"))
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    yield user

    db_session.delete(user)
    db_session.commit()
