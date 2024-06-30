"""
This module provides functions and utilities for handling orders in an asynchronous
context using SQLModel and FastAPI. 
"""

import os
import asyncio
import random
from typing import AsyncGenerator, Optional
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from trading_api.classes.orders_classes import OrderStatus, Order

# Define the path to the SQLite database
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sqlite_path = os.path.join(project_root, "trading_api", "internal", "database.db")

DATABASE_URL = f"sqlite+aiosqlite:///{sqlite_path}"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an async session for database operations.
    """
    async with AsyncSessionLocal() as session:
        yield session

async def init_db() -> None:
    """
    Initialize the database and create all tables.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def insert_order(order: Order, session: AsyncSession) -> Order:
    """
    Insert a new order into the database.

    :param order: The order to be inserted
    :param session: The AsyncSession instance
    :return: The inserted order with updated fields
    """
    db_order = Order.model_validate(order)
    session.add(db_order)
    await session.commit()
    await session.refresh(db_order)
    return db_order

async def update_order_status(order_id: int,
                              new_status: OrderStatus,
                              session: AsyncSession) -> Order:
    """
    Update the status of an order.

    :param order_id: ID of the order to update
    :param new_status: The new status to set for the order
    :param session: The AsyncSession instance
    :return: The updated order
    """
    order = await fetch_order_by_id(order_id, session)
    if order:
        if order.status == OrderStatus.CANCELED:
            raise HTTPException(status_code=409, detail="Cannot set status once canceled.")
        order.status = new_status
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order

async def update_order_status_randomly(order_id: int, session: AsyncSession) -> Order:
    """
    Update the order status randomly to either executed or canceled after a short delay.

    :param order_id: ID of the order to update
    :param session: The AsyncSession instance
    :return: The updated order
    """
    await asyncio.sleep(random.uniform(0.1, 1.0))

    random_status = random.choice([OrderStatus.EXECUTED, OrderStatus.CANCELED])
    order = await update_order_status(order_id=order_id,
                                      new_status=random_status,
                                      session=session)
    return order

async def get_query_fetch_orders(status: Optional[OrderStatus]) -> select:
    """
    Generate a query to fetch orders, optionally filtered by status.

    :param status: The status to filter orders by
    :return: The generated query
    """
    query = select(Order)
    if status:
        query = query.where(Order.status == status)
    return query

async def fetch_order_by_id(order_id: str, session: AsyncSession) -> Order:
    """
    Fetch an order by its ID.

    :param order_id: The ID of the order to fetch
    :param session: The AsyncSession instance
    :return: The fetched order
    """
    order = await session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

async def delete_order_by_id(order_id: str, session: AsyncSession) -> None:
    """
    Delete an order by its ID.

    :param order_id: The ID of the order to delete
    :param session: The AsyncSession instance
    """

    order = await fetch_order_by_id(order_id, session)

    await session.delete(order)
    await session.commit()