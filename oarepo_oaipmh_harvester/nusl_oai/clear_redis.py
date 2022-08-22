from redis import StrictRedis


def clear_recis_db(db=0):
    cache = StrictRedis(db=db)
    CHUNK_SIZE = 5000

    cursor = '0'
    while cursor != 0:
        cursor, keys = cache.scan(cursor=cursor, match='*', count=CHUNK_SIZE)
        if keys:
            cache.delete(*keys)


if __name__ == '__main__':
    clear_recis_db(0)
    clear_recis_db(1)
