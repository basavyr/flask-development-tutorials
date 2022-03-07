from pydoc import replace
from flask import Flask, render_template
import platform
import socket
import sqlite3
from contextlib import closing


app = Flask(__name__)


DB_FILE = 'openstack_topology.db'


def clean_states(raw_states):
    clean_states = []
    # print('in clean_states')
    for state in raw_states:
        # print(state, state[0][0])
        if(state[0][0] == 'u'):
            clean_states.append('up')
        else:
            clean_states.append('down')
    # print(clean_states)
    return clean_states


def get_db_content(db_file):
    db_connection = sqlite3.connect(db_file)

    # parse the state column which has extra characters
    with closing(db_connection):
        db_cursor = db_connection.cursor()
        raw_states = db_cursor.execute('SELECT state FROM HOSTS').fetchall()
        parsed_states = [(x,) for x in clean_states(raw_states)]

        for idx in range(len(raw_states)):
            sql_message = f'UPDATE HOSTS SET state=? WHERE id_cloud={idx+1}'
            db_cursor.execute(sql_message, parsed_states[idx])

        db_connection.commit()
        # fetch the entire database and save it as a list
        full_db_data = db_cursor.execute('SELECT * FROM HOSTS').fetchall()

    return full_db_data


@app.route("/")
def show_index():
    db_content = get_db_content(DB_FILE)
    return render_template('index.html',
                           sys_info=str(platform.uname()),
                           app=f'{app}',
                           db_content=db_content)


def main():
    local_ip_addr = socket.gethostbyname(socket.gethostname())
    port = 5051
    app.run(debug=True, host=local_ip_addr, port=port)


if __name__ == "__main__":
    main()
