"""
This module defines API endpoints for handling orders in an asynchronous context
using SQLModel and FastAPI.
"""

import random
import asyncio
from typing import Any, Optional
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_pagination import Page
from trading_api.internal.data_base import (
    get_session,
    init_db,
    delete_order_by_id,
    update_order_status_randomly,
    insert_order,
    get_query_fetch_orders,
    fetch_order_by_id
)
from trading_api.classes.orders_classes import (
    OrdersInput,
    OrdersOutput,
    OrderStatus
)

router = APIRouter()

@router.on_event("startup")
async def on_startup() -> None:
    """
    Initialize the database on startup.
    """
    await init_db()

@router.post("/orders",
    tags=["Default"],
    summary="Place a new order",
    response_model=OrdersOutput,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid input"},
        status.HTTP_201_CREATED: {"description": "Order Created"},
    }
)
async def place_new_order(order: OrdersInput,
                          session: AsyncSession = Depends(get_session)) -> Any:
    """
    Place a new order.

    :param order: The order input data
    :param session: The AsyncSession instance
    :return: The created order
    """
    await asyncio.sleep(random.uniform(0.1, 1.0))

    db_order = await insert_order(order, session)

    asyncio.create_task(update_order_status_randomly(db_order.id, session))
    return db_order

@router.get("/orders",
    tags=["Default"],
    summary="Retrieve all orders",
    response_model=Page[OrdersOutput],
    responses={
        status.HTTP_200_OK: {"description": "A list of orders"},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid input"},
    } 
)
async def get_orders(status: Optional[OrderStatus] = None,
                     session: AsyncSession = Depends(get_session)) -> Any:
    """
    Retrieve all orders, optionally filtered by status.

    :param status: The status to filter orders by
    :param session: The AsyncSession instance
    :return: A paginated list of orders
    """
    await asyncio.sleep(random.uniform(0.1, 1.0))

    query = await get_query_fetch_orders(status)

    return await paginate(session, query)

@router.get("/orders/{orderId}",
    tags=["Default"],
    summary="Retrieve a specific order",
    response_model=OrdersOutput,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Order not found"},
        status.HTTP_200_OK: {"description": "Order found"}
    }
)
async def get_specific_order(orderId: str,
                             session: AsyncSession = Depends(get_session)) -> Any:
    """
    Retrieve a specific order by ID.

    :param orderId: The ID of the order to retrieve
    :param session: The AsyncSession instance
    :return: The retrieved order
    """
    await asyncio.sleep(random.uniform(0.1, 1.0))

    order = await fetch_order_by_id(orderId, session)

    return order

@router.delete("/orders/{orderId}",
    tags=["Default"],
    summary="Cancel an order",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Order not found"},
        status.HTTP_204_NO_CONTENT: {"description": "Order canceled"}
    }
)
async def cancel_order(orderId: str,
                       session: AsyncSession = Depends(get_session)) -> None:
    """
    Cancel an order by ID.

    :param orderId: The ID of the order to cancel
    :param session: The AsyncSession instance
    :return: None
    """
    await delete_order_by_id(order_id=orderId,
                              session=session)

    return None
