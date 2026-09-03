import pymysql
from datetime import datetime

# ============================================================
# HOSPITAL MANAGEMENT SYSTEM
# ============================================================

MYSQL_PASSWORD = "YOUR_MYSQL_PASSWORD"


# ================= DATABASE CONNECTION =================

def connect_db():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password=MYSQL_PASSWORD,
        database="hospital_db",
        cursorclass=pymysql.cursors.DictCursor,
        ssl_disabled=True
    )


# ================= DATABASE SETUP =================

def setup_database():
    conn = connect_db()

    try:
        with conn.cursor() as cursor:

            # Login table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    role VARCHAR(30) DEFAULT 'Admin'
                )
            """)

            # Billing table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bills (
                    bill_id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT NOT NULL,
                    consultation_fee DECIMAL(10,2) DEFAULT 0,
                    medicine_charge DECIMAL(10,2) DEFAULT 0,
                    other_charge DECIMAL(10,2) DEFAULT 0,
                    total_amount DECIMAL(10,2) DEFAULT 0,
                    bill_date DATE NOT NULL,
                    FOREIGN KEY (patient_id)
                    REFERENCES patients(patient_id)
                    ON DELETE CASCADE
                )
            """)

            # Appointment reason column
            cursor.execute(
                "SHOW COLUMNS FROM appointments LIKE 'reason'"
            )

            if not cursor.fetchone():
                cursor.execute("""
                    ALTER TABLE appointments
                    ADD COLUMN reason VARCHAR(200)
                """)

            # Default admin account
            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                ("admin",)
            )

            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO users
                    (username, password, role)
                    VALUES (%s, %s, %s)
                """, ("admin", "admin123", "Admin"))

        conn.commit()

    finally:
        conn.close()


# ================= LOGIN =================

def login():

    print("\n" + "=" * 50)
    print("              ADMIN LOGIN")
    print("=" * 50)

    for attempt in range(3):

        username = input("Username: ")
        password = input("Password: ")

        conn = connect_db()

        try:
            with conn.cursor() as cursor:

                cursor.execute("""
                    SELECT * FROM users
                    WHERE username = %s AND password = %s
                """, (username, password))

                user = cursor.fetchone()

        finally:
            conn.close()

        if user:
            print("\nLogin successful!")
            print("Welcome,", user["username"])
            return True

        print("Invalid username or password.")

    print("\nToo many failed attempts.")
    return False


# ================= DASHBOARD =================

def dashboard():

    print("\n" + "=" * 50)
    print("                 DASHBOARD")
    print("=" * 50)

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute(
                "SELECT COUNT(*) AS total FROM patients"
            )
            patients = cursor.fetchone()["total"]

            cursor.execute(
                "SELECT COUNT(*) AS total FROM doctors"
            )
            doctors = cursor.fetchone()["total"]

            cursor.execute(
                "SELECT COUNT(*) AS total FROM appointments"
            )
            appointments = cursor.fetchone()["total"]

            cursor.execute(
                "SELECT COUNT(*) AS total FROM bills"
            )
            bills = cursor.fetchone()["total"]

            cursor.execute("""
                SELECT COALESCE(SUM(total_amount), 0) AS total
                FROM bills
            """)

            revenue = cursor.fetchone()["total"]

        print("Total Patients     :", patients)
        print("Total Doctors      :", doctors)
        print("Total Appointments :", appointments)
        print("Total Bills        :", bills)
        print("Total Billing      :", revenue)

    finally:
        conn.close()


# ============================================================
# PATIENT MANAGEMENT
# ============================================================

def add_patient():

    print("\n--- Add Patient ---")

    name = input("Enter patient name: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender: ")
    phone = input("Enter phone: ")
    address = input("Enter address: ")
    disease = input("Enter disease: ")

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO patients
                (name, age, gender, phone, address, disease)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                name,
                age,
                gender,
                phone,
                address,
                disease
            ))

        conn.commit()

        print("\nPatient added successfully!")

    finally:
        conn.close()


def view_patients():

    print("\n--- Patient List ---")

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute(
                "SELECT * FROM patients ORDER BY patient_id"
            )

            patients = cursor.fetchall()

        if not patients:
            print("No patients found.")
            return

        for patient in patients:

            print("-" * 45)

            print("ID:", patient["patient_id"])
            print("Name:", patient["name"])
            print("Age:", patient["age"])
            print("Gender:", patient["gender"])
            print("Phone:", patient["phone"])
            print("Address:", patient["address"])
            print("Disease:", patient["disease"])

    finally:
        conn.close()


def search_patient():

    print("\n--- Search Patient ---")

    patient_id = input("Enter patient ID: ")

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT * FROM patients
                WHERE patient_id = %s
            """, (patient_id,))

            patient = cursor.fetchone()

        if patient:

            print("\nPatient Found!")

            print("ID:", patient["patient_id"])
            print("Name:", patient["name"])
            print("Age:", patient["age"])
            print("Gender:", patient["gender"])
            print("Phone:", patient["phone"])
            print("Address:", patient["address"])
            print("Disease:", patient["disease"])

        else:
            print("Patient not found.")

    finally:
        conn.close()


def delete_patient():

    print("\n--- Delete Patient ---")

    patient_id = input("Enter patient ID: ")

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                DELETE FROM patients
                WHERE patient_id = %s
            """, (patient_id,))

            deleted = cursor.rowcount

        conn.commit()

        if deleted:
            print("Patient deleted successfully!")
        else:
            print("Patient not found.")

    finally:
        conn.close()


# ================= PATIENT MENU =================

def patient_menu():

    while True:

        print("\n" + "=" * 45)
        print("          PATIENT MANAGEMENT")
        print("=" * 45)

        print("1. Add Patient")
        print("2. View Patients")
        print("3. Search Patient")
        print("4. Delete Patient")
        print("5. Back to Main Menu")

        print("=" * 45)

        choice = input("Enter your choice: ")

        if choice == "1":
            add_patient()

        elif choice == "2":
            view_patients()

        elif choice == "3":
            search_patient()

        elif choice == "4":
            delete_patient()

        elif choice == "5":
            break

        else:
            print("Invalid choice!")


# ============================================================
# DOCTOR MANAGEMENT
# ============================================================

def add_doctor():

    print("\n--- Add Doctor ---")

    name = input("Enter doctor name: ")
    specialization = input("Enter specialization: ")
    phone = input("Enter phone: ")

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO doctors
                (name, specialization, phone)
                VALUES (%s, %s, %s)
            """, (
                name,
                specialization,
                phone
            ))

        conn.commit()

        print("\nDoctor added successfully!")

    finally:
        conn.close()


def view_doctors():

    print("\n--- Doctor List ---")

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute(
                "SELECT * FROM doctors ORDER BY doctor_id"
            )

            doctors = cursor.fetchall()

        if not doctors:
            print("No doctors found.")
            return

        for doctor in doctors:

            print("-" * 45)

            print("ID:", doctor["doctor_id"])
            print("Name:", doctor["name"])
            print("Specialization:", doctor["specialization"])
            print("Phone:", doctor["phone"])

    finally:
        conn.close()


def search_doctor():

    print("\n--- Search Doctor ---")

    doctor_id = input("Enter doctor ID: ")

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT * FROM doctors
                WHERE doctor_id = %s
            """, (doctor_id,))

            doctor = cursor.fetchone()

        if doctor:

            print("\nDoctor Found!")

            print("ID:", doctor["doctor_id"])
            print("Name:", doctor["name"])
            print("Specialization:", doctor["specialization"])
            print("Phone:", doctor["phone"])

        else:
            print("Doctor not found.")

    finally:
        conn.close()


def delete_doctor():

    print("\n--- Delete Doctor ---")

    doctor_id = input("Enter doctor ID: ")

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                DELETE FROM doctors
                WHERE doctor_id = %s
            """, (doctor_id,))

            deleted = cursor.rowcount

        conn.commit()

        if deleted:
            print("Doctor deleted successfully!")
        else:
            print("Doctor not found.")

    finally:
        conn.close()


# ================= DOCTOR MENU =================

def doctor_menu():

    while True:

        print("\n" + "=" * 45)
        print("           DOCTOR MANAGEMENT")
        print("=" * 45)

        print("1. Add Doctor")
        print("2. View Doctors")
        print("3. Search Doctor")
        print("4. Delete Doctor")
        print("5. Back to Main Menu")

        print("=" * 45)

        choice = input("Enter your choice: ")

        if choice == "1":
            add_doctor()

        elif choice == "2":
            view_doctors()

        elif choice == "3":
            search_doctor()

        elif choice == "4":
            delete_doctor()

        elif choice == "5":
            break

        else:
            print("Invalid choice!")


# ============================================================
# APPOINTMENT MANAGEMENT
# ============================================================

def patient_exists(patient_id):

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT * FROM patients
                WHERE patient_id = %s
            """, (patient_id,))

            return cursor.fetchone()

    finally:
        conn.close()


def doctor_exists(doctor_id):

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT * FROM doctors
                WHERE doctor_id = %s
            """, (doctor_id,))

            return cursor.fetchone()

    finally:
        conn.close()


def add_appointment():

    print("\n--- Add Appointment ---")

    print("\nAvailable Patients:")
    view_patients()

    patient_id = input("\nEnter patient ID: ")

    if not patient_exists(patient_id):

        print("Patient ID does not exist.")
        print("Appointment not added.")
        return

    print("\nAvailable Doctors:")
    view_doctors()

    doctor_id = input("\nEnter doctor ID: ")

    if not doctor_exists(doctor_id):

        print("Doctor ID does not exist.")
        print("Appointment not added.")
        return

    appointment_date = input(
        "Enter appointment date (YYYY-MM-DD): "
    )

    appointment_time = input(
        "Enter appointment time (HH:MM): "
    )

    reason = input("Enter reason: ")

    try:

        datetime.strptime(
            appointment_date + " " + appointment_time,
            "%Y-%m-%d %H:%M"
        )

    except ValueError:

        print("Invalid date or time format.")
        return

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO appointments
                (
                    patient_id,
                    doctor_id,
                    appointment_date,
                    appointment_time,
                    reason
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                reason
            ))

        conn.commit()

        print("\nAppointment added successfully!")

    except Exception as e:

        conn.rollback()

        print("\nAppointment could not be added.")
        print("Error:", e)

    finally:
        conn.close()


def view_appointments():

    print("\n--- Appointment List ---")

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    a.appointment_id,
                    p.name AS patient_name,
                    d.name AS doctor_name,
                    a.appointment_date,
                    a.appointment_time,
                    a.reason
                FROM appointments a
                JOIN patients p
                ON a.patient_id = p.patient_id
                JOIN doctors d
                ON a.doctor_id = d.doctor_id
                ORDER BY a.appointment_id
            """)

            appointments = cursor.fetchall()

        if not appointments:

            print("No appointments found.")
            return

        for appointment in appointments:

            print("-" * 50)

            print(
                "Appointment ID:",
                appointment["appointment_id"]
            )

            print(
                "Patient:",
                appointment["patient_name"]
            )

            print(
                "Doctor:",
                appointment["doctor_name"]
            )

            print(
                "Date:",
                appointment["appointment_date"]
            )

            print(
                "Time:",
                appointment["appointment_time"]
            )

            print(
                "Reason:",
                appointment["reason"]
            )

    finally:
        conn.close()


def search_appointment():

    print("\n--- Search Appointment ---")

    appointment_id = input(
        "Enter appointment ID: "
    )

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    a.appointment_id,
                    p.name AS patient_name,
                    d.name AS doctor_name,
                    a.appointment_date,
                    a.appointment_time,
                    a.reason
                FROM appointments a
                JOIN patients p
                ON a.patient_id = p.patient_id
                JOIN doctors d
                ON a.doctor_id = d.doctor_id
                WHERE a.appointment_id = %s
            """, (appointment_id,))

            appointment = cursor.fetchone()

        if appointment:

            print("\nAppointment Found!")

            print(
                "Appointment ID:",
                appointment["appointment_id"]
            )

            print(
                "Patient:",
                appointment["patient_name"]
            )

            print(
                "Doctor:",
                appointment["doctor_name"]
            )

            print(
                "Date:",
                appointment["appointment_date"]
            )

            print(
                "Time:",
                appointment["appointment_time"]
            )

            print(
                "Reason:",
                appointment["reason"]
            )

        else:

            print("Appointment not found.")

    finally:
        conn.close()


def delete_appointment():

    print("\n--- Delete Appointment ---")

    appointment_id = input(
        "Enter appointment ID: "
    )

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                DELETE FROM appointments
                WHERE appointment_id = %s
            """, (appointment_id,))

            deleted = cursor.rowcount

        conn.commit()

        if deleted:

            print(
                "Appointment deleted successfully!"
            )

        else:

            print("Appointment not found.")

    finally:
        conn.close()


# ================= APPOINTMENT MENU =================

def appointment_menu():

    while True:

        print("\n" + "=" * 45)
        print("        APPOINTMENT MANAGEMENT")
        print("=" * 45)

        print("1. Add Appointment")
        print("2. View Appointments")
        print("3. Search Appointment")
        print("4. Delete Appointment")
        print("5. Back to Main Menu")

        print("=" * 45)

        choice = input("Enter your choice: ")

        if choice == "1":
            add_appointment()

        elif choice == "2":
            view_appointments()

        elif choice == "3":
            search_appointment()

        elif choice == "4":
            delete_appointment()

        elif choice == "5":
            break

        else:
            print("Invalid choice!")


# ============================================================
# BILLING MANAGEMENT
# ============================================================

def create_bill():

    print("\n--- Create Bill ---")

    print("\nAvailable Patients:")
    view_patients()

    patient_id = input(
        "\nEnter patient ID: "
    )

    if not patient_exists(patient_id):

        print("Patient ID does not exist.")
        return

    consultation = float(
        input("Enter consultation fee: ")
    )

    medicine = float(
        input("Enter medicine charge: ")
    )

    other = float(
        input("Enter other charges: ")
    )

    total = consultation + medicine + other

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO bills
                (
                    patient_id,
                    consultation_fee,
                    medicine_charge,
                    other_charge,
                    total_amount,
                    bill_date
                )
                VALUES
                (%s, %s, %s, %s, %s, CURDATE())
            """, (
                patient_id,
                consultation,
                medicine,
                other,
                total
            ))

        conn.commit()

        print("\nBill created successfully!")
        print("Total Amount:", total)

    finally:
        conn.close()


def view_bills():

    print("\n--- Bill List ---")

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    b.bill_id,
                    p.name AS patient_name,
                    b.consultation_fee,
                    b.medicine_charge,
                    b.other_charge,
                    b.total_amount,
                    b.bill_date
                FROM bills b
                JOIN patients p
                ON b.patient_id = p.patient_id
                ORDER BY b.bill_id
            """)

            bills = cursor.fetchall()

        if not bills:

            print("No bills found.")
            return

        for bill in bills:

            print("-" * 50)

            print("Bill ID:", bill["bill_id"])
            print("Patient:", bill["patient_name"])
            print("Consultation:", bill["consultation_fee"])
            print("Medicine:", bill["medicine_charge"])
            print("Other Charges:", bill["other_charge"])
            print("Total:", bill["total_amount"])
            print("Date:", bill["bill_date"])

    finally:
        conn.close()


def delete_bill():

    print("\n--- Delete Bill ---")

    bill_id = input(
        "Enter bill ID: "
    )

    conn = connect_db()

    try:

        with conn.cursor() as cursor:

            cursor.execute("""
                DELETE FROM bills
                WHERE bill_id = %s
            """, (bill_id,))

            deleted = cursor.rowcount

        conn.commit()

        if deleted:

            print("Bill deleted successfully!")

        else:

            print("Bill not found.")

    finally:
        conn.close()


# ================= BILLING MENU =================

def billing_menu():

    while True:

        print("\n" + "=" * 45)
        print("             BILLING MANAGEMENT")
        print("=" * 45)

        print("1. Create Bill")
        print("2. View Bills")
        print("3. Delete Bill")
        print("4. Back to Main Menu")

        print("=" * 45)

        choice = input("Enter your choice: ")

        if choice == "1":
            create_bill()

        elif choice == "2":
            view_bills()

        elif choice == "3":
            delete_bill()

        elif choice == "4":
            break

        else:
            print("Invalid choice!")


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():

    while True:

        print("\n" + "=" * 55)
        print("           HOSPITAL MANAGEMENT SYSTEM")
        print("=" * 55)

        print("1. Dashboard")
        print("2. Patient Management")
        print("3. Doctor Management")
        print("4. Appointment Management")
        print("5. Billing Management")
        print("6. Logout")

        print("=" * 55)

        choice = input("Enter your choice: ")

        if choice == "1":

            dashboard()

        elif choice == "2":

            patient_menu()

        elif choice == "3":

            doctor_menu()

        elif choice == "4":

            appointment_menu()

        elif choice == "5":

            billing_menu()

        elif choice == "6":

            print("\nLogged out successfully!")
            break

        else:

            print("Invalid choice!")


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    try:

        setup_database()

        if login():

            main_menu()

        else:

            print(
                "\nHospital Management System closed."
            )

    except pymysql.err.OperationalError as e:

        print("\nDatabase connection error!")
        print("Check MySQL server and password.")
        print("Error:", e)

    except Exception as e:

        print("\nUnexpected error:")
        print(e)