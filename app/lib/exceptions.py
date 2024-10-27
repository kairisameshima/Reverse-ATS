from typing import Type, Union
from uuid import UUID

from flask_sqlalchemy.model import Model

from db.base import BaseTable


class RecordNotFoundError(Exception):
    def __init__(
        self,
        entity_id: Union[int, str, UUID],
        model: Union[Type[Model], Type[BaseTable]],
    ):
        self.id = entity_id
        self.model = model

    def __str__(self):
        return f"Record (uuid={self.id}) of type {self.model.__name__} not found."
