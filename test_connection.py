import pymysql

print("1. Python started")

try:
    print("2. Connecting...")

    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="aryansh7078@#",
        database="hospital_db",
        connect_timeout=10
    )

    print("3. Connected!")
    print("4. Connection successful")

    conn.close()
    print("5. Connection closed")

except Exception as e:
    print("ERROR:", type(e).__name__)
    print("DETAIL:", e)