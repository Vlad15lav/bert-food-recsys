import mysql.connector

def add_user(db, user_name):
    """
    Добавляем нового пользователя в базу данных
    """
    with db.cursor() as cur:
        cur.execute("SELECT id_user \
                        FROM users \
                        WHERE user_name = %s", (user_name, ))
        result_query = cur.fetchall()

        if len(result_query) == 0:
            cur.execute("INSERT INTO users (user_name) \
                            VALUES (%s)", (user_name, ))
    db.commit()


def get_id_user(db, user_name):
    """
    Узнать индекс пользователя в базе данных
    """
    with db.cursor() as cur:
        cur.execute("SELECT id_user \
                        FROM users \
                        WHERE user_name = %s", (user_name, ))
        user_id = cur.fetchall()[0][0]
    
    return user_id


def add_request(db, id_user, id_item, id_model):
    """
    Добавляем запрос рекомендации в базу данных
    """
    with db.cursor() as cur:
        cur.execute("INSERT INTO requests (id_user, id_item, id_model, date) \
                        VALUES (%s, %s, %s, CONVERT_TZ(NOW(),'+00:00','+3:00'))",
                        (id_user, id_item, id_model))
    
    db.commit()


def get_id_model(db, user_name):
    """
    Узнать текущею рекомендательную систему у пользователя
    """
    with db.cursor() as cur:
        cur.execute(f"SELECT r.id_model \
                        FROM requests AS r \
                        JOIN users AS u USING(id_user) \
                        WHERE u.user_name = '{user_name}' \
                            AND DATE(r.date) = (SELECT DATE(CONVERT_TZ(NOW(),'+00:00','+3:00')));")
        id_model = cur.fetchall()
    
    if len(id_model) == 0:
        return None
    
    return id_model[0][0]

def add_reviews(db, user_name, rating):
    """
    Добавляем отзыв пользователя о рекомендации (для A/B тестирования)
    """
    # Проверяем есть ли рекомендация, которую нужно оценить
    with db.cursor() as cur:
        cur.execute(f"SELECT MAX(r.id_req) \
                        FROM requests AS r \
                        JOIN users AS u USING(id_user) \
                        WHERE u.user_name = '{user_name}';")
        id_req = cur.fetchall()

    if len(id_req) == 0:
        return
    
    # Проверяем оставлял ли уже пользователь отзыв на рекомендацию
    with db.cursor() as cur:
        cur.execute(f"SELECT id_rev \
                        FROM reviews \
                        WHERE id_req = {id_req[0][0]};")
        id_rev = cur.fetchall()
    
    if len(id_rev) > 0:
        return 

    # Добавляем отзыв пользователя
    with db.cursor() as cur:
        cur.execute("INSERT INTO reviews (id_req, rating) \
                        VALUES (%s, %s)",
                        (id_req[0][0], rating))
    
    db.commit()
