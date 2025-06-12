import mysql.connector

def connect_to_mysql():
    conn = mysql.connector.connect(
        host="localhost", user="user", password="password", database="futurama", port=3306
    )
    cursor = conn.cursor()
    return conn,cursor

def reset_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS characters")
    cursor.execute("""
                    CREATE TABLE characters (
                    id INT PRIMARY KEY,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    image_url TEXT
                    )
                    """)
    
    cursor.execute("DROP TABLE IF EXISTS episodes")
    cursor.execute("""
                    CREATE TABLE episodes (
                    id INT PRIMARY KEY,
                    number VARCHAR(50),
                    title VARCHAR(255),
                    writer VARCHAR(255),
                    original_date VARCHAR(100)
                    )
                    """)
    
def insert_characters(character_data,conn,cursor):
    for character in character_data:
        cursor.execute("INSERT INTO characters(id,first_name,last_name,image_url) VALUES (%s, %s, %s, %s)",
                       (
                           character["id"],
                           character["name"]["first"],
                           character["name"]["last"],
                           character["images"]["main"],
                       ),
        )

    conn.commit()

    print("Saved to Mysql")

def store_characters_in_mysql(character_data):
    conn, cursor = connect_to_mysql()

    reset_table(cursor)

    insert_characters(character_data, conn, cursor)

    cursor.close()
    conn.close()
    print("Closed mysql connection")

def insert_episodes(episode_data, conn, cursor):
    for episode in episode_data:
        cursor.execute("INSERT INTO episodes(id, number, title, writer, original_date) VALUES (%s, %s, %s, %s, %s)",
                       (
                           episode["id"],
                           episode["number"],
                           episode["title"],
                           episode["writers"],
                           episode["originalAirDate"],
                       ),
        )

    conn.commit()
    print(f"Saved {len(episode_data)} episodes to MySQL")

def store_episodes_in_mysql(episode_data):
    conn, cursor = connect_to_mysql()
    insert_episodes(episode_data, conn, cursor)
    cursor.close()
    conn.close()
    print("Closed MySQL connection")