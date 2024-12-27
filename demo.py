import mysql.connector
db = mysql.connector.connect(
        user='root',
        host='localhost',
        password='Tejadeep@1755',
        port=3306,
        database='charity'
    )
print(db)