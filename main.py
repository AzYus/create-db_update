import psycopg2


def delete_db(conn):
    cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)


def create_db(conn):
    cur.execute('CREATE TABLE IF NOT EXISTS client ('
                'id SERIAL PRIMARY KEY, '
                'name VARCHAR (40) NOT NULL ,'
                'surname VARCHAR (40) NOT NULL,'
                'email VARCHAR (40) NOT NULL,'
                'phone VARCHAR(40));')
    cur.execute('CREATE TABLE IF NOT EXISTS phone('
                'id SERIAL PRIMARY KEY,'
                'customer_id integer references client(id),'
                'phone_number VARCHAR(220));')


def add_client(conn, first_name, last_name, email, phones):
    cur.execute("""
                   INSERT INTO client(name, surname, email) VALUES(%s, %s, %s) 
                   RETURNING id, name, surname, email;
        """, (first_name, last_name, email))
    print(cur.fetchall())

    cur.execute("""
                    INSERT INTO phone(customer_id,phone_number) VALUES(%s,%s)
                    RETURNING id, customer_id, phone_number;""", (1, phones))
    print(cur.fetchall())


def add_phone(conn, client_id, phone):
    cur.execute("""
        INSERT INTO phone(phone_number, customer_id) VALUES(%s, %s);
        """, (phone, client_id))
    cur.execute("""
              SELECT * FROM phone;
              """)
    print(cur.fetchall())


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
               UPDATE client SET name=%s WHERE id=%s;
               """, (first_name, client_id))
    cur.execute("""
               UPDATE client SET surname=%s WHERE id=%s;
               """, (last_name, client_id))
    cur.execute(f"""
               UPDATE client SET email=%s WHERE id=%s;
               """, (email, client_id))
    cur.execute("""
               SELECT * FROM client;
               """)
    print(cur.fetchall())
    cur.execute("""
               UPDATE phone SET phone_number=%s WHERE id=%s;
               """, (phone, client_id))
    cur.execute("""
               SELECT * FROM phone;
               """)
    print(cur.fetchall())


def delete_phone(conn, phone):
    cur.execute("""
        DELETE FROM phone WHERE phone_number=%s;
        """, (phone,))
    cur.execute("""
        SELECT * FROM phone;
        """)
    print(cur.fetchall())


def delete_client(conn, client_id):
    cur.execute("""
        DELETE FROM phone WHERE customer_id=%s;
        """, (client_id,))
    cur.execute("""
        SELECT * FROM phone;
        """)
    print(cur.fetchall())
    cur.execute("""
        DELETE FROM client WHERE id=%s;
        """, (client_id,))
    cur.execute("""
        SELECT * FROM client;
        """)
    print(cur.fetchall())


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
            SELECT id FROM client WHERE name=%s and surname=%s and email=%s;
            """, (first_name, last_name, email,))
    print(cur.fetchone())
    cur.execute("""
            SELECT customer_id FROM phone WHERE phone_number=%s;
                    """, (phone,))
    print(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="personal_data", user="postgres", password="Yupi28@") as conn:
        with conn.cursor() as cur:
            delete_db(conn)
            create_db(conn)
            add_client(conn, 'Az', 'Yu', 'azyu@gmail.com', '+7-999-999-99-99')
            add_phone(conn, 1, '+72382365517')
            change_client(conn, 1, 'Za', 'Yu', 'zayu@mail.ru', '+79999999')
            delete_phone(conn, '+78888888888')
            # delete_client(conn, 1)
            find_client(conn, 'Za', 'Yu', 'zayu@mail.ru', '+79999999')
    conn.close()