import aiosqlite
import logging
import time


class SQLiteDatabase:

    def __init__(self, conn):
        self._conn = conn
        # set aiosqlite logging level to critical, otherwise it spams stdio
        # with IntegrityError warnings
        log = logging.getLogger('aiosqlite')
        log.setLevel(logging.CRITICAL)

    @classmethod
    async def connect(cls, path='firehose.db'):
        conn = await aiosqlite.connect(path)
        await conn.execute('''
            create table if not exists Item (
                id text not null unique,
                title text not null,
                url text not null,
                body text not null,
                thumb text not null,
                category text not null,
                published text not null,
                processed real not null,
                source_name text not null,
                source_url text not null
            );
        ''')
        await conn.execute('''
            create index if not exists idxProcessed on Item (processed)
        ''')
        await conn.execute('''
            create index if not exists idxCategory on Item (category)
        ''')
        await conn.commit()
        return SQLiteDatabase(conn)

    async def close(self):
        await self._conn.close()

    async def insert(self, x):
        values = (
            x['id'],
            x['title'],
            x['url'],
            x.get('body', ''),
            x.get('thumb', ''),
            x.get('category', ''),
            x['published'].split(' ')[0],
            time.time(),
            x['source_name'],
            x['source_url'],
        )
        try:
            await self._conn.execute('''
            insert into Item (
                id,
                title,
                url,
                body,
                thumb,
                category,
                published,
                processed,
                source_name,
                source_url
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)
            await self._conn.commit()
        except aiosqlite.IntegrityError:
            return False
        return True
