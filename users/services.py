import stripe
from django.conf import settings

# Подтягиваю из settings.py секретный ключ для сервиса Stripe
stripe.api_key = settings.SECRET_KEY_FOR_STRIPE


def create_stripe_product(paid_product):
    """Создание продукта по объекту модели (Course или Lesson) в платежной системе Stripe.

    :param paid_product: Это экземпляр модели (например, Course или Lesson), а Stripe_API ожидает:
        1) строку (str), чаще всего это название продукта (name), поэтому указываю "paid_product.title".
        2) или словарь (dict), если передаем product_data.
    :return: Для дальнейшего процесса формирования оплаты в return хватит одного product.id, если не нужны другие
    данные из ответа Stripe. Но, если нужно будет хранить в БД что-то ещё (например, product.url, product.name и т.д.),
    то нужно возвращать весь объект.
    """
    # Не обязательно, но лучшие практики рекомендуют делать проверку атрибутов на их наличие (микробезопасность):
    # Чтобы код был защищённым от случайных вызовов, можно добавить проверку, что объект действительно имеет .title:
    if not hasattr(paid_product, "title"):
        raise ValueError(
            "Объект должен иметь атрибут 'title' для создания продукта в Stripe"
        )

    try:
        product = stripe.Product.create(name=paid_product.title)
        return product.id
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании продукта в Stripe: {e.user_message}")


def create_stripe_price(product_id, payment_amount):
    """Создание цены продукта в платежной системе Stripe.
    Достаточно в функцию передать только product_id и payment_amount.

    :param product_id: ID продукта из Stripe (строка).
    :param payment_amount: Цена продукта, которую потом нужно перевести в копейки обязательно.
    :return: Для дальнейшего процесса формирования оплаты в return хватит одного price.id. Возвращаем объект
    только тогда, если нам нужно хранить какие-то другие поля (например, currency, unit_amount и т.д.).
    """
    try:
        price = stripe.Price.create(
            currency="RUB",
            unit_amount=int(payment_amount * 100),
            # В create_price() можно использовать ***product_data={"id": product_id}*** вместо
            # ***product=product_id***, если нам нужно одновременно создать нового продукта прям сразу тут в цене
            # без create_product_course(). Но, если продукт уже создан, то нужно использовать ***product=product_id***
            # вместо product_data.
            product=product_id,
        )
        return price.id
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании цены в Stripe: {e.user_message}")


def create_stripe_session(price_id):
    """Создание сессии для получения ссылки на оплату продукта.
    Достаточно в функцию передать только price_id, а остальное можно захардкодить (quantity=1 и т.д.) и потом изменить,
    когда появится у Пользователя возможность выбора количества оплачиваемых продуктов.

    :param price_id: ID цены из Stripe (строка).
    :return session.url, session.id: Для дальнейшего процесса формирования оплаты в return хватит session.id
    и session.url.
    1) session.url - нужно отдать клиенту;
    2) session.id - нужно сохранить в модель для последующей проверки статуса (Session.retrieve).
    """
    try:
        session = stripe.checkout.Session.create(
            # Только в продакшене (на хостинге с SSL/HTTPS) можно будет указать https://....
            success_url="http://127.0.0.1:8000/",
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
        )
        return session.id, session.url
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании сессии в Stripe: {e.user_message}")


def get_stripe_payment_status(session_id):
    """Получение статуса оплаты по session_id из Stripe.

    :param session_id: ID сессии оплаты в Stripe.
    :return: Строка со статусом оплаты (например, 'paid', 'unpaid' и т.д.).
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при проверке статуса в Stripe: {e.user_message}")
