"""
This module defines data models and enums related to orders and provides validation
using Pydantic for input and output data, as well as ORM mappings using SQLModel.
"""

from enum import Enum
from pydantic import BaseModel, Field
from sqlmodel import (
    SQLModel,
    Field as sqlField,
    Index
)

class OrderStatus(Enum):
    """
    Enum representing the status of an order.
    """
    PENDING = "pending"
    EXECUTED = "executed"
    CANCELED = "canceled"


class OrdersInput(BaseModel):
    """
    Model representing the input structure for placing a new order.

    Attributes:
        stocks (str): Currency pair symbol (e.g., "EURUSD").
        quantity (float): Quantity of the currency pair to be traded.
    """

    stocks: str = Field(
        ...,
        description='Currency pair symbol (e.g. "EURUSD")',
    )
    quantity: float = Field(
        ...,
        description='Quantity of the currency pair to be traded',
        ge=0
    )


class OrdersOutput(OrdersInput):
    """
    Model representing the output structure for an order, extending from OrdersInput.

    Attributes:
        id (int): Unique identifier for the order.
        status (str): Status of the order.
    """

    id: int = Field(
        ...,
        description='Unique identifier for the order',
    )
    status: OrderStatus = Field(..., description='Status of the order')


class Order(SQLModel, table=True):
    """
    Database model representing a trading order.

    Attributes:
        id (int, optional): Unique identifier for the order.
        stocks (str): Currency pair symbol (e.g., "EURUSD").
        quantity (float): Quantity of the currency pair to be traded.
        status (OrderStatus): Status of the order.
    """

    id: int = sqlField(default=None, primary_key=True)
    stocks: str = sqlField(..., description="Currency pair symbol (e.g., 'EURUSD')")
    quantity: float = sqlField(..., description="Quantity of the currency pair to be traded", ge=0)
    status: OrderStatus = sqlField(default=OrderStatus.PENDING,
                                   sa_column_kwargs={"server_default": OrderStatus.PENDING.name},
                                   description="Status of the order")
    __table_args__ = (
        Index("idx_status", "status"),
    )
