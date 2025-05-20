import abc

from src.domain.repositories.stock_repository import SyncStockRepository

class UnitOfWork(abc.ABC):

    @abc.abstractmethod
    def _initialize_session(self):  # pragma: no cover
        raise NotImplementedError

    @abc.abstractmethod
    def _initialize_repositories(self):  # pragma: no cover
        raise NotImplementedError


class SyncUnitOfWork(UnitOfWork):
    stock_repo: SyncStockRepository = None

    def __enter__(self):
        self._initialize_session()
        self._initialize_repositories()
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        self._rollback()
        self._close_session()

    @abc.abstractmethod
    def commit(self):  # pragma: no cover
        raise NotImplementedError

    @abc.abstractmethod
    def close_connection(self):  # pragma: no cover
        raise NotImplementedError

    @abc.abstractmethod
    def _rollback(self):  # pragma: no cover
        raise NotImplementedError

    @abc.abstractmethod
    def _close_session(self):  # pragma: no cover
        raise NotImplementedError


# This is not completely working, prefer Sync UOW

# class AsyncUnitOfWork(UnitOfWork):  # pragma: no cover
#     stock_repo: AsyncStockRepository = None

#     async def __aenter__(self):
#         self._initialize_session()
#         self._initialize_repositories()
#         return self

#     async def __aexit__(self, exn_type, exn_value, traceback):
#         await self._rollback()
#         await self._close_session()

#     @abc.abstractmethod
#     async def commit(self):  # pragma: no cover
#         raise NotImplementedError

#     @abc.abstractmethod
#     async def close_connection(self):  # pragma: no cover
#         raise NotImplementedError

#     @abc.abstractmethod
#     async def _rollback(self):  # pragma: no cover
#         raise NotImplementedError

#     @abc.abstractmethod
#     async def _close_session(self):  # pragma: no cover
#         raise NotImplementedError
