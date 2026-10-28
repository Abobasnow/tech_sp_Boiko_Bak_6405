from src.db import Base, engine
from src import models  # noqa: F401 — важно, чтобы модели зарегистрировались

Base.metadata.create_all(engine)
print("Таблицы созданы.")