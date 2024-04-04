import sqlite3


connection = sqlite3.connect('rest_base.db', check_same_thread=False)
cursor = connection.cursor()


def insert_user(user_id, name):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute('select user_id from users where user_id = ?', (user_id,))
        user = cursor.fetchone()
        if user is None:
            cursor.execute('insert into users (user_id, name) values (?, ?)', (user_id, name, ))
        else:
            pass


def find_rest_id(name):
    with connection as conn:
        result = conn.cursor().execute('select restaurant_id from restaurants where name = ?',
                                       (name,)).fetchone()
        return result


def insert_order_to_orders_cache(id_booking, ex, date, user_id, number, rest_id):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute('insert into booking (order_id, execution, Date,client_id,'
                       'numberOfPersons,rest_id) values (?, ?, ?,?, ?, ?)',
                       (id_booking, ex, date, user_id, number, rest_id, ))


def get_description_by_name(name):
    with connection as conn:
        result = conn.cursor().execute('select description,address,image from restaurants where name = ?',
                                       (name,)).fetchone()
        return result
def get_description_map_by_name(name):
    with connection as conn:
        result = conn.cursor().execute('select description,address,map,image from restaurants where name = ?',
                                       (name,)).fetchone()
        return result

