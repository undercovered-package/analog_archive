import typing as tp
from abc import ABC, abstractmethod

from pydantic import BaseModel  # pylint: disable=E0611

T = tp.TypeVar('T', bound='UCResponse', covariant=True)


class UCRequest(BaseModel):
    pass


class UCResponse(BaseModel):
    errors: list["BaseUCError"] = []
    value: tp.Any = None

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def build_from_exception(cls: type[T], exception: "BaseUCError") -> T:
        instance = cls()
        instance.errors.extend([exception])
        return instance

    @property
    def first_error(self) -> tp.Optional["BaseUCError"]:
        if self:
            return None
        return self.errors[0]

    def add_error(self, error: "BaseUCError") -> None:
        self.errors.append(error)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def __nonzero__(self) -> bool:
        return not self.has_errors()

    __bool__ = __nonzero__


class UC(ABC):
    """Base UseCase class"""

    @abstractmethod
    async def execute(self, request: UCRequest, *args: tp.Any, **kwargs: tp.Any) -> UCResponse:
        raise NotImplementedError()


class BaseUCError(Exception):
    error_code = -1
    message = "Server error"

    def __init__(self, message: tp.Optional[str] = None, error_code: tp.Optional[int] = None):
        if message is not None:
            self.message = message
        if error_code is not None:
            self.error_code = error_code

        super().__init__(self.message)
