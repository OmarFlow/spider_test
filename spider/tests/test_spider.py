import pytest

from spider.models import Product


@pytest.mark.django_db
def test_organizations(api_client, city_hood_factory,
                       category_factory, enterprise_network_factory,
                       enterprise_factory, product_factory,
                       product_price_factory):
    hood = city_hood_factory()

    category_meal = category_factory(title="продукты")
    category_drinks = category_factory(title="напитки")

    network = enterprise_network_factory(title="x5")

    enterprise_auchan = enterprise_factory(
        title="ашан", network=network, hoods=(hood,))
    enterprise_kb = enterprise_factory(
        title="красное_белое", network=network, hoods=(hood,))

    fanta = product_factory(title="фанта", category=category_drinks,
                            network=network, enterprises=(enterprise_kb,))
    product_price_factory(price=40, enterprise=enterprise_kb, product=fanta)

    pineapple = product_factory(title="pineapple", category=category_meal,
                                network=network, enterprises=(enterprise_auchan,))
    product_price_factory(
        price=1000, enterprise=enterprise_kb, product=pineapple)

    # проверяем фильтр минимальной цены
    res = api_client.get(
        f"/api/enterprises/{hood.id}/organizations/", {"min": True}, format="json").json()
    assert len(res) == 1
    assert res[0]["title"] == enterprise_kb.title

    # проверяем фильтр максимальной цены
    res = api_client.get(
        f"/api/enterprises/{hood.id}/organizations/", {"max": True}, format="json").json()
    assert len(res) == 1
    assert res[0]["title"] == enterprise_auchan.title

    # проверяем фильтр категории
    res = api_client.get(f"/api/enterprises/{hood.id}/organizations/", {
        "category": category_meal.id}, format="json").json()
    assert len(res) == 1
    assert res[0]["title"] == enterprise_auchan.title

    # проверяем фильтр текста(с русскими словами не точный поиск не работает,
    # видимо нужно настаривать бд, потому что пробежавшись по доке джанги не увидел чего-то подобного,
    # но может и не заметил)
    res = api_client.get(f"/api/enterprises/{hood.id}/organizations/", {
        "product_title": "pineapples"}, format="json").json()
    assert len(res) == 1
    assert res[0]["title"] == enterprise_auchan.title


@pytest.mark.django_db
def test_last_price_change(api_client, city_hood_factory,
                           category_factory, enterprise_network_factory,
                           enterprise_factory, product_factory,
                           product_price_factory):
    hood = city_hood_factory()
    category_drinks = category_factory(title="напитки")
    network = enterprise_network_factory(title="x5")
    enterprise_kb = enterprise_factory(
        title="красное_белое", network=network, hoods=(hood,))

    fanta = product_factory(title="фанта", category=category_drinks,
                            network=network, enterprises=(enterprise_kb,))
    product_price_factory(price=40, enterprise=enterprise_kb, product=fanta)

    res = api_client.get(f"/api/products/{fanta.id}/").json()
    assert res["price"] == 40
    assert res["price"] == fanta.last_price

    # создаём новую цену для фанты
    product_price_factory(price=30, enterprise=enterprise_kb, product=fanta)

    # проверяем, что цена изменилась
    res = api_client.get(f"/api/products/{fanta.id}/").json()
    assert res["price"] == 30
    assert res["price"] == fanta.last_price


@pytest.mark.django_db
def test_create_product(api_client, city_hood_factory,
                        category_factory, enterprise_network_factory,
                        enterprise_factory):
    hood = city_hood_factory()
    category_drinks = category_factory(title="напитки")
    network = enterprise_network_factory(title="x5")
    enterprise_kb = enterprise_factory(
        title="красное_белое", network=network, hoods=(hood,))

    # проверяем, что продукт создался и с верными данными
    res = api_client.post("/api/products/",
                          {"title": "fanta_created", "category": category_drinks.id,
                           "network": network.id, "enterprises": enterprise_kb.id,
                           "price": 40},
                          format="json")
    assert res.status_code == 201
    fanta = Product.objects.get(title="fanta_created")
    assert fanta.category == category_drinks
    assert fanta.enterprises.first() == enterprise_kb
    assert fanta.last_price == 40
