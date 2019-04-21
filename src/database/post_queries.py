from typing import Dict

from database.models import Post


async def add_post(conn, data: Dict[str, str]):
    stmt = Post.insert().values(category_id=data['category_id'],
                                title=data['title'],
                                text=data['text'],
                                main_img=data['main_img'],
                                created_at=data['created_at'],
                                last_updated=data['last_updated'])
    await conn.execute(stmt)


async def get_all(conn):
    result = await conn.execute(Post.select())
    return await result.fetchall()
