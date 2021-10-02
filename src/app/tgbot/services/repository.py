from typing import Optional

import asyncpg


class Repo:

    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def add_user(self, user_id) -> None:
        """Сохранение пользователя"""
        await self.conn.execute(
            "INSERT INTO users (id) VALUES ($1) ON CONFLICT DO NOTHING",
            user_id,
        )
        return

    async def set_store_to_user(self, store_id: int, user_id: int):
        """Добавление магазина пользователю"""
        await self.conn.execute(
            "DELETE FROM user_store WHERE user_id=$1",
            user_id
        )
        await self.conn.execute(
            "INSERT INTO user_store (user_id, store_id) VALUES ($1, $2) ON CONFLICT DO NOTHING",
            user_id, store_id
        )

    async def get_user_store_id(self, user_id: int) -> Optional[str]:
        """Получение магазинов пользователя"""
        row = await self.conn.fetchrow(
            "SELECT user_id, store_id FROM user_store WHERE user_id=$1",
            user_id
        )
        return None if not row else row["store_id"]

    async def add_sku_to_user(self, user_id: int, sku_id: str) -> None:
        """
        Добавление товара к пользователю
        """
        await self.conn.execute("INSERT INTO user_skus (user_id, sku_id) VALUES ($1, $2) ON CONFLICT DO NOTHING",
                                user_id, sku_id)

    async def get_user_sku_ids(self, user_id: int) -> list[int]:
        """Получение идентификаторов товаров"""
        rows = await self.conn.fetch(
            "SELECT sku_id FROM user_skus WHERE user_id=$1",
            user_id
        )

        return [row["sku_id"] for row in rows]
