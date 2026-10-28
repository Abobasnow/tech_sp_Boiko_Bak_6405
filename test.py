import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

url = os.environ["DATABASE_URL"].replace("postgresql+psycopg2://", "postgresql://")

conn = psycopg2.connect(url)

cur = conn.cursor()

SQL = """
    SELECT tag.name, COUNT(post.id) AS posts_count
    FROM tag
    JOIN subscription ON subscription.tag_id = tag.id
    JOIN post ON post.tag_id = tag.id
    WHERE subscription.user_id = %s
    GROUP BY tag.name
    ORDER BY COUNT(post.id) DESC
"""
cur.execute(SQL, (1,))

for row in cur.fetchall():
    name = row[0]
    posts_count = row[1]
    print(f"{name}: {posts_count}")

cur.close()
conn.close()

# stmt = (
#         select(models.Tag.name, func.count(models.Post.id).label("posts_count"))
#         .join(models.Subscription, models.Subscription.tag_id == models.Tag.id)
#         .join(models.Post, models.Post.tag_id == models.Tag.id)
#         .where(models.Subscription.user_id == 1)
#         .group_by(models.Tag.name)
#         .order_by(func.count(models.Post.id).desc())
#     )
#
# with engine.connect() as conn:
#     for row in conn.execute(stmt):
#         print(f"{row.name}: {row.posts_count}")
#
# from src.db import Base, SessionLocal, engine
# from src import crud, models
# from src.seed import seed
# from sqlalchemy import text, select, func
#
# from sqlalchemy import text
# from src.db import engine
#
# raw_sql = """
#     SELECT tag.name, COUNT(post.id) AS posts_count
#     FROM tag
#
#     JOIN subscription ON subscription.tag_id = tag.id
#     JOIN post ON post.tag_id = tag.id
#     WHERE subscription.user_id = :user_id
#
#     GROUP BY tag.name
#     ORDER BY COUNT(post.id) DESC
# """
#
# with engine.connect() as conn:
#     result = conn.execute(text(raw_sql), {"user_id": 1})
#     rows = result.fetchall()
#     for row in rows:
#         print(f"Тег: {row.name} Постов: {row.posts_count}")
#
#
with SessionLocal() as db:


    srtm = select(models.Tag.name, func.count(models.Post.id).label("posts_count"))\
    .join(models.Subscription, models.Subscription.tag_id == models.Tag.id) \
    .join(models.Post, models.Post.tag_id == models.Tag.id)\
    .where(models.Subscription.user_id == 1)\
    .group_by(models.Tag.name)\
    .order_by(func.count(models.Post.id).desc())
    for row in db.execute(srtm).all():
        print(f"{row.name}:{row.posts_count}")

    ivan = db.get(models.User, 1)
    results = []
    for sub in ivan.subscriptions:
        tag = sub.tag
        results.append((tag.name, len(tag.posts)))
    results.sort(key=lambda x: x[1], reverse=True)
    for name, cnt in results:
        print(f"{name}: {cnt}")

# # stmt = (
# #         select(models.Tag.name, func.count(models.Post.id).label("posts_count"))
# #         .join(models.Subscription, models.Subscription.tag_id == models.Tag.id)
# #         .join(models.Post, models.Post.tag_id == models.Tag.id)
# #         .where(models.Subscription.user_id == 1)
# #         .group_by(models.Tag.name)
# #         .order_by(func.count(models.Post.id).desc())
# #     )
# #
# # with engine.connect() as conn:
# #     for row in conn.execute(stmt):
# #         print(f"{row.name}: {row.posts_count}")