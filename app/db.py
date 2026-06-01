from sqlalchemy import create_engine, text
import config

_engine = create_engine(config.DB_URI, echo=True)


class _ResultWrapper:
    def __init__(self, rows):
        self._rows = rows

    def fetchall(self):
        return self._rows

    def fetchone(self):
        return self._rows[0] if self._rows else None

    def __iter__(self):
        return iter(self._rows)


class _EngineWrapper:
    def execute(self, query, params=None):
        with _engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return _ResultWrapper(result.fetchall())


db = _EngineWrapper()
