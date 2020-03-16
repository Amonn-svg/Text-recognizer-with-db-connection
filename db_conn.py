from configparser import ConfigParser
import psycopg2


def connection_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for i in params:
            db[i[0]] = i[1]
    else:
        raise Exception("Invalid ini file: section {0} not found".format(section))
    return db


def tables_create():
    commands = (
        """ CREATE TABLE datastore (
                Tema VARCHAR(50) NOT NULL,
                Parola VARCHAR(20) NOT NULL,
                Frequenza FLOAT,
                PRIMARY KEY (Tema, Parola)
            );
        """,
        )
    conn = None
    try:
        params = connection_config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        for c in commands:
            cur.execute(c)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def upsert_data(theme, word, frequency):

    sqlupdate = """INSERT INTO datastore
                    VALUES (%s, %s, %f)
                    ON CONFLICT(Tema,Parola)
                    DO UPDATE SET Frequenza = %f;
            """
    conn = None
    try:
        params = connection_config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sqlupdate, (theme, word, frequency))
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def delete_data(frequency):
    sql = """DELETE FROM datastore WHERE dataupdate.frequenza > %f """
    conn = None
    try:
        params = connection_config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql, (frequency,))
        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
