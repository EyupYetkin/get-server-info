import psycopg2, configparser

def connect_to_database():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    try:
        dbname = config['database']['dbname']
        user = config['database']['user']
        password = config['database']['password']
        conn = psycopg2.connect(dbname=dbname, user=user, password=password)
        return conn
    
    except psycopg2.Error as e:
        print(f"Database ile bağlanti kurulamadi: {str(e)}")
        return None

def perform_database_operation(conn, query, data=None):
    try:            
        cursor = conn.cursor()
        cursor.execute(query,data)
        cursor.close()
        conn.commit()
        return None
    except psycopg2.Error as e:
        print(f"Database islemi gerceklestirilemedi: {str(e)}")
        return None

def clean_db(conn, hosts):
    try:
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM cpu WHERE ip NOT IN %s", (tuple(hosts),))

        cursor.execute("DELETE FROM memory WHERE ip NOT IN %s", (tuple(hosts),))

        cursor.execute("DELETE FROM users WHERE ip NOT IN %s", (tuple(hosts),))
        conn.commit()
        cursor.close()
    except psycopg2.Error as e :
        print(f"Database temizleme islemi yapilamadi: {str(e)}")



def close_database_connection(conn):
    try:
        conn.close()
    except psycopg2.Error as e:
        print(f"Database kapatilamadi: {str(e)}")
