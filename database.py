import mysql.connector

# Replace the placeholders with your MySQL connection details
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='irs',
    port = '3306',
    # socket		='/opt/lampp/var/mysql/mysql.sock',
    unix_socket='/opt/lampp/var/mysql/mysql.sock'
)

def insert_member(firstname, lastname, username, address, gender, photo):
    cursor = db.cursor()
    sql = "INSERT INTO members (firstname, lastname, username, address, gender, photo) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (firstname, lastname, username, address, gender, photo)
    cursor.execute(sql, val)
    db.commit()

def get_member_by_username(username):
    cursor = db.cursor()
    sql = "SELECT * FROM members WHERE username = %s"
    cursor.execute(sql, (username,))
    return cursor.fetchone()

def face_matching_algorithm(photo1, photo2):
    # Implement your face recognition logic here
    # Compare the two photos and return True if they match, False otherwise
    return True  # Placeholder for demonstration purposes

if __name__ == '__main__':
    db.close()
