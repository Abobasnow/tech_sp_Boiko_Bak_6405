from src.db import Base, SessionLocal, engine
from src import crud, models
from src.seed import seed
from sqlalchemy import text, select


def line(title: str) -> None:
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



    with SessionLocal() as db:
        seed(db)

        line("Все теги")
        for t in crud.list_tags(db):
            print(f"  #{t.id} {t.name} — {t.description}")

        line("Опубликованные статьи")
        for p in crud.list_published_posts(db):
            author = p.admin.name if p.admin else (p.author.nickname if p.author else "—")
            tag = p.tag.name if p.tag else "—"
            views = crud.count_views(db, p.id)
            print(f"  #{p.id} [{tag}] {p.title!r} | автор: {author} | просмотров: {views}")

        line("Статьи с тегом 'Анонсы'")
        ann = crud.get_tag_by_name(db, "Анонсы")
        for p in crud.list_posts_by_tag(db, ann.id):
            print(f"  #{p.id} {p.title}")

        line("Поиск по подстроке 'квиз'")
        for p in crud.search_posts(db, "квиз"):
            print(f"  #{p.id} {p.title}")

        line("Подписки Ивана")
        u1 = db.query(models.User).filter_by(nickname="Иван Иванов").first()
        for sub in crud.list_user_subscriptions(db, u1.id):
            print(f"  → {sub.tag.name}")

        line("Подписчики тега 'Анонсы'")
        for user in crud.list_tag_subscribers(db, ann.id):
            print(f"  → {user.nickname}")

        line("Библиотека Ивана")
        for p in crud.list_user_library(db, u1.id):
            print(f"  #{p.id} {p.title}")

        line("Снятие с публикации p3")
        crud.unpublish_post(db, 3)
        db.commit()
        print(f"  После снятия опубликовано: "
              f"{len(crud.list_published_posts(db))} статей")

        line("Создание и удаление тега")
        t = crud.create_tag(db, "Тестовый", "Временный тег")
        print(f"  Создан: {t}")



        db.commit()

    print("\nГотово.\n")




if __name__ == "__main__":
    main()