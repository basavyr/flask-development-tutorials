import sqlite3


def get_user_vms(db_file):
    connection = sqlite3.connect(db_file)

    cursor = connection.cursor()

    data = cursor.execute('''SELECT id_cloud, host FROM HOSTS''').fetchall()

    connection.close()

    return data
