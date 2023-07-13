import mysql.connector

def create_tables(db):
    """
    Создаем таблицы для базы данных
    """
    assert db.is_connected(), "База данных не подключена!"

    try:
        with db.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
                            id_user INT NOT NULL AUTO_INCREMENT,
                            user_name CHAR(50) NOT NULL,
                            PRIMARY KEY (id_user));""")

            cur.execute("""CREATE TABLE IF NOT EXISTS models (
                            id_model INT NOT NULL AUTO_INCREMENT,
                            system_name CHAR(12) NOT NULL,
                            PRIMARY KEY(id_model));""")

            cur.execute("""CREATE TABLE IF NOT EXISTS requests (
                            id_req INT NOT NULL AUTO_INCREMENT,
                            id_user INT NOT NULL,
                            id_item INT NOT NULL,
                            id_model INT NOT NULL,
                            date DATETIME NOT NULL,
                            PRIMARY KEY(id_req));""")

            cur.execute("""CREATE TABLE IF NOT EXISTS reviews (
                            id_rev INT NOT NULL AUTO_INCREMENT,
                            id_req INT NOT NULL,
                            rating INT NOT NULL,
                            PRIMARY KEY(id_rev));""")

            cur.execute("""INSERT IGNORE INTO models (id_model, system_name)
                            VALUES (1, 'TF-IDF'), (2, 'BERT');""")
    except Exception as e:
        print(e)
    
    db.commit()