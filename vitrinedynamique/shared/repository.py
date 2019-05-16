from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, List, Any

T = TypeVar('T')
From = TypeVar('From')
To = TypeVar('To')


class Mapper(Generic[From, To], metaclass=ABCMeta):
    @abstractmethod
    def map(self, from_obj: From) -> To:
        pass


class Specification(metaclass=ABCMeta):
    pass


class ByAgenceIdSpecification(Specification):
    def __init__(self, agence_id: str, filters: dict={}):
        self.agence_id = agence_id
        self.filters = filters


class ByAnnonceIdSpecification(Specification):
    def __init__(self, annonce_id):
        self.annonce_id = annonce_id


class AllSpecification(Specification):
    pass


class Repository(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def get(self, id: str) -> T:
        pass

    @abstractmethod
    def list(self, spec: Specification) -> List[T]:
        pass


class DatabaseRepository(Repository[T], metaclass=ABCMeta):
    @abstractmethod
    def save(self, item: T):
        pass

    @abstractmethod
    def save_all(self, items: List[T]):
        pass