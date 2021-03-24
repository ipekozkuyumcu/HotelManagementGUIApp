import sqlite3


def create_database():
    conn = sqlite3.connect("hotel.db")
    conn.commit()
    conn.close()
    create_missing_table()


def create_missing_table():
    conn = sqlite3.connect("hotel.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tblUser (
            username TEXT PRIMARY KEY,
            name TEXT,
            surname TEXT,
            pNo INTEGER,
            password TEXT
        );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tblReservation (
            reservationID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            country TEXT,
            city TEXT,
            numberOfPeople INTEGER,
            numberOfRoom INTEGER,
            view TEXT,
            breakfast TEXT,
            ac TEXT,
            rs TEXT,
            reservationDate TEXT,
            visitStartDate TEXT,
            visitFinishDate TEXT
        );
        """)
    conn.commit()
    conn.close()
