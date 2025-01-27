from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lenta.client import LentaClient
from lenta.models import City, Store, BaseSku
from tgbot.callbacks.profile import city_cb, store_cb, add_sku_cb
from tgbot.services.repository import Repo


async def get_city_by_name(city_name: str, lenta_client: LentaClient) -> Optional[City]:
    """
    Получение города по названию
    :param city_name:
    :param lenta_client:
    :return:
    """

    all_cities = await lenta_client.get_cities()

    for city in all_cities:
        if city.name == city_name:
            return city
    return None


async def get_inline_keyboard_for_cities(lenta_client: LentaClient) -> InlineKeyboardMarkup:
    """
    Получение инлайн клавиатуры для списка городов
    :return:
    """
    all_cities = await lenta_client.get_cities()
    all_cities = sorted(all_cities, key=lambda c: c.name)

    return InlineKeyboardMarkup(row_width=2).add(
        *[InlineKeyboardButton(city.name, callback_data=city_cb.new(city_id=city.id)) for city in all_cities]
    )


async def get_inline_keyboard_for_city_stores(lenta_client: LentaClient, city_id: str) -> InlineKeyboardMarkup:
    """
    Получение инлайн клавиатуры для списка магазинов
    :param lenta_client:
    :param city_id:
    :return:
    """
    city_stores = await lenta_client.get_city_stores(city_id)
    city_stores = sorted(city_stores, key=lambda s: s.name)

    return InlineKeyboardMarkup(row_width=2).add(
        *[InlineKeyboardButton(store.name, callback_data=store_cb.new(store_id=store.id)) for store in city_stores]
    )


async def get_store_for_user(lenta_client: LentaClient, repo: Repo, user_id: int) -> Optional[Store]:
    """
    Получение магазинов пользователя
    :param repo:
    :param user_id:
    :param lenta_client:
    :return:
    """

    store_id = await repo.get_user_store_id(user_id)
    return await lenta_client.get_store(store_id) if store_id else None


async def save_store_for_user(repo: Repo, user_id: int, store_id: int) -> None:
    await repo.set_store_to_user(store_id, user_id)


def get_add_sku_keyboard(sku_id: str) -> InlineKeyboardMarkup:
    """Получение клавиатуры для добавление товара"""
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Добавить товар", callback_data=add_sku_cb.new(sku_id))
    )


async def get_user_skus(user_id: int, repo: Repo, lenta_client: LentaClient) -> list[BaseSku]:
    """Получение информации о товарах пользователя"""
    sku_ids = await repo.get_user_sku_ids(user_id)
    store_id = await repo.get_user_store_id(user_id)
    return await lenta_client.get_store_skus_by_ids(store_id, sku_ids) if sku_ids else []


async def get_user_sku(user_id: int, sku_code: str, repo: Repo, lenta_client: LentaClient) -> BaseSku:
    store_id = await repo.get_user_store_id(user_id)
    return await lenta_client.get_sku(store_id, sku_code)


async def search_skus_in_user_store(user_id: int, sku_name: str,
                                    repo: Repo, lenta_client: LentaClient) -> list[BaseSku]:
    """Получение товаров по совпадению в названии"""
    store_id = await repo.get_user_store_id(user_id)
    return await lenta_client.search_skus_in_store(store_id, sku_name)
