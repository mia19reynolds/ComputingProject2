import mysql.connector as mysql

HOST = "igor.gold.ac.uk"
DATABASE = "avidl002_Project"
USER = "avidl002"
PASSWORD = "asdf"
PORT = 3307

db = mysql.connect(
    host=HOST, 
    database=DATABASE, 
    user=USER, 
    password=PASSWORD,
    port=PORT
)


print("Connected to:", db.get_server_info()) 

cursor = db.cursor()
cursor.execute("SELECT * FROM Users")
for x in cursor:
    print(x)