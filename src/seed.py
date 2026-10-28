from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src import crud, models


def seed(db: Session) -> None:
    if db.query(models.Account).count() > 0:
        print("[seed] БД уже заполнена, пропускаем")
        return

    print("[seed] Заполняем БД тестовыми данными...")

    t_news = crud.create_tag(db, "Новости", "Научные достижения и отчёты")
    t_humor = crud.create_tag(db, "Юмор", "Мемы и неформальный контент")
    t_ann = crud.create_tag(db, "Анонсы", "Мероприятия, дедлайны, приглашения")

    admin_acc = crud.create_account(db, "admin@sno.ru", "sno_admin", "hashed_pw_admin")
    admin = crud.create_admin(
        db, account_id=admin_acc.id, name="Пресс-служба СНО",
        can_create_admins=True,
    )

    u1_acc = crud.create_account(db, "ivanov@stud.ru", "ivanov", "hashed_pw_1")
    u1 = crud.create_user(db, account_id=u1_acc.id, nickname="Иван Иванов")

    u2_acc = crud.create_account(db, "petrova@stud.ru", "petrova", "hashed_pw_2")
    u2 = crud.create_user(db, account_id=u2_acc.id, nickname="Анна Петрова")

    p1 = crud.create_post(
        db, title="СНО ИИКа заняло 1 место на конференции",
        body="Команда нашего СНО представила проект...",
        admin_id=admin.id, tag_id=t_news.id,
        summary="Отчёт о победе на межвузовской конференции",
    )
    crud.publish_post(db, p1.id)

    p2 = crud.create_post(
        db, title="Мемы про сессию: часть 2",
        body="Подборка лучших студенческих мемов...",
        admin_id=admin.id, tag_id=t_humor.id,
        summary="Юмористическая подборка",
    )
    crud.publish_post(db, p2.id)

    p3 = crud.create_post(
        db, title="Анонс: научный квиз 15 октября",
        body="Приглашаем всех на научный квиз...",
        admin_id=admin.id, tag_id=t_ann.id,
        summary="Приглашение к участию",
    )
    crud.publish_post(db, p3.id)

    p4 = crud.create_post(
        db, title="Анонс: набор в научный кружок",
        body="Открыт набор в кружок по машинному обучению...",
        admin_id=admin.id, tag_id=t_ann.id,
    )
    crud.publish_post(db, p4.id)

    crud.subscribe(db, u1.id, t_news.id)
    crud.subscribe(db, u1.id, t_ann.id)
    crud.subscribe(db, u2.id, t_humor.id)

    now = datetime.utcnow()
    crud.record_view(db, post_id=p1.id, user_id=u1.id, read_seconds=180)
    crud.record_view(db, post_id=p2.id, user_id=u2.id, read_seconds=60)
    crud.record_view(db, post_id=p1.id, user_id=u2.id, read_seconds=200)

    crud.add_to_library(db, u1.id, p1.id)
    crud.add_to_library(db, u1.id, p3.id)
    crud.add_to_library(db, u2.id, p2.id)

    db.commit()
    print("[seed] Готово")