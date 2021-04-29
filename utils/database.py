import sqlite3


def initialize(name):
    conn = sqlite3.connect(name)
    conn.execute('''CREATE TABLE posts
            (post_id INT PRIMARY KEY    NOT NULL,
            user_id INT,
            text           TEXT    NOT NULL,
            time        TEXT,
            image            TEXT,
            url        TEXT             NOT NULL,
            source_name         TEXT    NOT NULL,
            source_identifier           TEXT);''')

    conn.close()


def check_if_exists(name, id):
    with sqlite3.connect(name) as c:
        r = c.execute(
            "SELECT * FROM posts WHERE post_id = ?", (id,))
        return r.fetchone()

# post_id,  text, url, source_name, time=None, image=None, user_id=None, source_identifier=None


def store(name, data):
    with sqlite3.connect(name) as c:

        images = ",".join(data["images"])
        r = c.execute(
            "INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (data["post_id"], data["user_id"], data["text"], data["time"], images, data["post_url"], data["source_name"], data["source_identifier"]))
