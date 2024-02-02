import mysql.connector
import hashlib

def add_user(db, user_tm_id):
    """
    Добавляем нового пользователя в базу данных
    """
    tm_hash_id = hashlib.sha3_256(str(user_tm_id).encode()).hexdigest()

    with db.cursor() as cur:
        cur.execute("""SELECT user_id
                        FROM users
                        WHERE tm_hash_id = %s""", (tm_hash_id, ))
        user_id = cur.fetchall()

        # Если пользователя еще нет базе данных - добавляем его
        if len(user_id) == 0:
            cur.execute("""INSERT INTO users (tm_hash_id)
                            VALUES (%s)""", (tm_hash_id, ))
    db.commit()


def get_user_id(db, user_tm_id):
    """
    Узнать индекс пользователя в базе данных
    """
    tm_hash_id = hashlib.sha3_256(str(user_tm_id).encode()).hexdigest()

    with db.cursor() as cur:
        cur.execute("""SELECT user_id
                        FROM users
                        WHERE tm_hash_id = %s""", (tm_hash_id, ))
        user_id = cur.fetchall()

    # Если пользователя еще нет базе данных - добавляем его
    if len(user_id) == 0:
        with db.cursor() as cur:
            cur.execute("""INSERT INTO users (tm_hash_id)
                            VALUES (%s)""", (tm_hash_id, ))
            db.commit()

            cur.execute("""SELECT user_id
                            FROM users
                            WHERE tm_hash_id = %s""", (tm_hash_id, ))
            user_id = cur.fetchall()

    return user_id[0][0]


def add_request(db, user_id, items_id, model_id):
    """
    Добавляем запрос рекомендации в базу данных
    """
    with db.cursor() as cur:
        cur.execute("""INSERT INTO requests (user_id, item_first_id,
                                item_second_id, item_third_id, model_id, date)
                        VALUES (%s, %s, %s, %s, %s, CONVERT_TZ(NOW(),'+00:00','+3:00'))""",
                        (user_id, *items_id, model_id))

    db.commit()


def get_model_id(db, user_tm_id):
    """
    Узнать текущею рекомендательную систему у пользователя (для A/B тестирования)
    """
    tm_hash_id = hashlib.sha3_256(str(user_tm_id).encode()).hexdigest()

    with db.cursor() as cur:
        cur.execute("""SELECT r.model_id
                        FROM requests AS r
                        JOIN users AS u USING(user_id)
                        WHERE u.tm_hash_id = %s
                            AND DATE(r.date) = (SELECT DATE(CONVERT_TZ(NOW(),'+00:00','+3:00')))""",
                            (tm_hash_id, ))
        model_id = cur.fetchall()

    if len(model_id) == 0:
        return None

    return model_id[0][0]


def add_reviews(db, user_tm_id, rating):
    """
    Добавляем отзыв пользователя о рекомендации (для A/B тестирования)
    """
    # Проверяем есть ли рекомендация, которую нужно оценить
    tm_hash_id = hashlib.sha3_256(str(user_tm_id).encode()).hexdigest()

    with db.cursor() as cur:
        cur.execute("""SELECT MAX(r.request_id)
                        FROM requests AS r
                        JOIN users AS u USING(user_id)
                        WHERE u.tm_hash_id = %s""", (tm_hash_id, ))
        request_id = cur.fetchall()

    if len(request_id) == 0:
        return

    # Проверяем пользователь оставлял ли уже отзыв на рекомендацию
    with db.cursor() as cur:
        cur.execute("""SELECT review_id
                        FROM reviews
                        WHERE request_id = %s""", (request_id[0][0], ))
        review_id = cur.fetchall()

    if len(review_id) > 0:
        return

    # Добавляем отзыв пользователя
    with db.cursor() as cur:
        cur.execute("""INSERT INTO reviews (request_id, rating)
                        VALUES (%s, %s)""", (request_id[0][0], rating))

    db.commit()
