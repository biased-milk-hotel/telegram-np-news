import sqlite3


def initialize(name):
    with sqlite3.connect(name) as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE posts
            (post_id INT PRIMARY KEY    NOT NULL,
            user_id INT,
            text           TEXT    NOT NULL,
            time        TEXT,
            image            TEXT,
            url        TEXT             NOT NULL,
            source_name         TEXT    NOT NULL,
            source_identifier           TEXT);''')
        
        con.commit()



def check_if_exists(name, id):
    with sqlite3.connect(name) as con:
        cur = con.cursor()
        r = cur.execute(
            "SELECT * FROM posts WHERE post_id = ?", (id,))
        return r.fetchone()

# post_id,  text, url, source_name, time=None, image=None, user_id=None, source_identifier=None


def store(name, data):
    with sqlite3.connect(name) as con:
        cur = con.cursor()

        images = ",".join(data["images"])
        cur.execute(
            "INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (data["post_id"], data["user_id"], data["text"], data["time"], images, data["post_url"], data["source_name"], data["source_identifier"]))

        con.commit()