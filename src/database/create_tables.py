import mysql.connector

def create_tables(db):
    """
    Создаем таблицы для базы данных
    """
    assert db.is_connected(), "База данных не подключена!"

    try:
        with db.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
                            user_id INT NOT NULL AUTO_INCREMENT,
                            tm_hash_id CHAR(64) NOT NULL,
                            PRIMARY KEY (user_id))""")

            cur.execute("""CREATE TABLE IF NOT EXISTS models (
                            model_id INT NOT NULL AUTO_INCREMENT,
                            system_name VARCHAR(16) NOT NULL,
                            PRIMARY KEY(model_id))""")

            cur.execute("""CREATE TABLE IF NOT EXISTS requests (
                            request_id INT NOT NULL AUTO_INCREMENT,
                            user_id INT NOT NULL,
                            item_first_id INT NOT NULL,
                            item_second_id INT NOT NULL,
                            item_third_id INT NOT NULL,
                            model_id INT NOT NULL,
                            date DATETIME NOT NULL,
                            PRIMARY KEY(request_id))""")

            cur.execute("""CREATE TABLE IF NOT EXISTS reviews (
                            review_id INT NOT NULL AUTO_INCREMENT,
                            request_id INT NOT NULL,
                            rating INT NOT NULL,
                            PRIMARY KEY(review_id))""")

            cur.execute("""INSERT IGNORE INTO models (model_id, system_name)
                            VALUES (1, 'TF-IDF'), (2, 'BERT')""")
    except Exception as e:
        print(e)
    
    db.commit()