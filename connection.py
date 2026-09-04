import mysql.connector

print("1. Program started")
print("2. Trying MySQL connection...")

try:
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="aryansh7078@#",
        database="hospital_db"
    )

    print("3. MySQL Database Connected Successfully!")

    con.close()
    print("4. Connection closed")

except Exception as e:
    print("ERROR:", e)  