import psycopg2
import configparser

# Read config file
config = configparser.ConfigParser()
config.read('config.ini')

# connect to database
conn = psycopg2.connect(
    host=config['DATABASE']['host'],
    database=config['DATABASE']['database'],
    user=config['DATABASE']['user'],
    password=config['DATABASE']['password']
)

def create_db(conn): # drop before create if exists and create new with first_name, last_name, email, phones
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS clients')
    cur.execute('CREATE TABLE clients (id serial PRIMARY KEY, first_name varchar(255), last_name varchar(255), email varchar(255), phones varchar(255))')
    conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    cur = conn.cursor()
    cur.execute('INSERT INTO clients (first_name, last_name, email, phones) VALUES (%s, %s, %s, %s)', (first_name, last_name, email, phones))
    conn.commit()

def add_phone(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute('SELECT phones FROM clients WHERE id = %s', (client_id,))
    phones = cur.fetchone()[0]
    if phones:
        phones += ',' + phone
    else:
        phones = phone
    cur.execute('UPDATE clients SET phones = %s WHERE id = %s', (phones, client_id))
    conn.commit()

def update_client(conn, client_id, first_name, last_name, email, phones=None):
    cur = conn.cursor()
    cur.execute('UPDATE clients SET first_name = %s, last_name = %s, email = %s, phones = %s WHERE id = %s', (first_name, last_name, email, phones, client_id))
    conn.commit()

def delete_client(conn, client_id):
    cur = conn.cursor()
    cur.execute('DELETE FROM clients WHERE id = %s', (client_id,))
    conn.commit()

def delete_phone(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute('SELECT phones FROM clients WHERE id = %s', (client_id,))
    phones = cur.fetchone()[0]
    phones = phones.split(',')
    phones.remove(phone)
    phones = ','.join(phones)
    cur.execute('UPDATE clients SET phones = %s WHERE id = %s', (phones, client_id))
    conn.commit()

def get_client(conn, client_id):
    cur = conn.cursor()
    cur.execute('SELECT * FROM clients WHERE id = %s', (client_id,))
    return cur.fetchone()

def get_clients(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM clients')
    return cur.fetchall()