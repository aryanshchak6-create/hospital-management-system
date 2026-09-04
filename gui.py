
import tkinter as tk
from tkinter import messagebox
import pymysql
from datetime import datetime


# ================= DATABASE CONNECTION =================

MYSQL_PASSWORD = "YOUR_MYSQL_PASSWORD"


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


# ================= LOGIN =================

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "admin123":
        messagebox.showinfo(
            "Login Successful",
            "Welcome to Hospital Management System!"
        )

        login_window.destroy()
        open_dashboard()

    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password"
        )


# ================= PATIENT MANAGEMENT =================

def add_patient():
    win = tk.Toplevel()
    win.title("Add Patient")
    win.geometry("400x400")

    tk.Label(win, text="Patient Name").pack(pady=5)
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Age").pack(pady=5)
    age_entry = tk.Entry(win)
    age_entry.pack()

    tk.Label(win, text="Gender").pack(pady=5)
    gender_entry = tk.Entry(win)
    gender_entry.pack()

    tk.Label(win, text="Phone").pack(pady=5)
    phone_entry = tk.Entry(win)
    phone_entry.pack()

    tk.Label(win, text="Address").pack(pady=5)
    address_entry = tk.Entry(win)
    address_entry.pack()

    def save_patient():
        try:
            conn = connect_db()
            cursor = conn.cursor()

            query = """
                INSERT INTO patients
                (name, age, gender, phone, address)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    name_entry.get(),
                    age_entry.get(),
                    gender_entry.get(),
                    phone_entry.get(),
                    address_entry.get()
                )
            )

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Patient added successfully!"
            )

            win.destroy()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        win,
        text="Add Patient",
        command=save_patient,
        width=20
    ).pack(pady=20)


def view_patients():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM patients ORDER BY patient_id"
        )

        patients = cursor.fetchall()

        cursor.close()
        conn.close()

        if not patients:
            messagebox.showinfo(
                "Patients",
                "No patients found."
            )
            return

        text = ""

        for p in patients:
            text += (
                f"ID: {p['patient_id']}\n"
                f"Name: {p['name']}\n"
                f"Age: {p['age']}\n"
                f"Gender: {p['gender']}\n"
                f"Phone: {p['phone']}\n"
                f"Address: {p['address']}\n"
                f"{'-' * 40}\n"
            )

        messagebox.showinfo("Patient List", text)

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def search_patient():
    win = tk.Toplevel()
    win.title("Search Patient")
    win.geometry("350x200")

    tk.Label(
        win,
        text="Enter Patient ID"
    ).pack(pady=10)

    id_entry = tk.Entry(win)
    id_entry.pack()

    def search():
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM patients WHERE patient_id = %s",
                (id_entry.get(),)
            )

            patient = cursor.fetchone()

            cursor.close()
            conn.close()

            if patient:
                messagebox.showinfo(
                    "Patient Found",
                    f"Patient ID: {patient['patient_id']}\n"
                    f"Name: {patient['name']}\n"
                    f"Age: {patient['age']}\n"
                    f"Gender: {patient['gender']}\n"
                    f"Phone: {patient['phone']}\n"
                    f"Address: {patient['address']}"
                )
            else:
                messagebox.showwarning(
                    "Not Found",
                    "Patient not found."
                )

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        win,
        text="Search",
        command=search,
        width=15
    ).pack(pady=20)


def delete_patient():
    win = tk.Toplevel()
    win.title("Delete Patient")
    win.geometry("350x200")

    tk.Label(
        win,
        text="Enter Patient ID"
    ).pack(pady=10)

    id_entry = tk.Entry(win)
    id_entry.pack()

    def delete():
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM patients WHERE patient_id = %s",
                (id_entry.get(),)
            )

            patient = cursor.fetchone()

            if not patient:
                messagebox.showwarning(
                    "Not Found",
                    "Patient not found."
                )
                cursor.close()
                conn.close()
                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this patient?"
            )

            if confirm:
                cursor.execute(
                    "DELETE FROM patients WHERE patient_id = %s",
                    (id_entry.get(),)
                )

                conn.commit()

                messagebox.showinfo(
                    "Deleted",
                    "Patient deleted successfully!"
                )

                win.destroy()

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        win,
        text="Delete",
        command=delete,
        width=15
    ).pack(pady=20)


def open_patient_management():
    win = tk.Toplevel()
    win.title("Patient Management")
    win.geometry("400x400")

    tk.Label(
        win,
        text="Patient Management",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Button(
        win,
        text="Add Patient",
        command=add_patient,
        width=25
    ).pack(pady=10)

    tk.Button(
        win,
        text="View Patients",
        command=view_patients,
        width=25
    ).pack(pady=10)

    tk.Button(
        win,
        text="Search Patient",
        command=search_patient,
        width=25
    ).pack(pady=10)

    tk.Button(
        win,
        text="Delete Patient",
        command=delete_patient,
        width=25
    ).pack(pady=10)


# ================= DOCTOR MANAGEMENT =================

def add_doctor():
    win = tk.Toplevel()
    win.title("Add Doctor")
    win.geometry("400x400")

    tk.Label(win, text="Doctor Name").pack(pady=5)
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Specialization").pack(pady=5)
    specialization_entry = tk.Entry(win)
    specialization_entry.pack()

    tk.Label(win, text="Phone").pack(pady=5)
    phone_entry = tk.Entry(win)
    phone_entry.pack()

    tk.Label(win, text="Department").pack(pady=5)
    department_entry = tk.Entry(win)
    department_entry.pack()

    def save_doctor():
        try:
            conn = connect_db()
            cursor = conn.cursor()

            query = """
                INSERT INTO doctors
                (name, specialization, phone, department)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    name_entry.get(),
                    specialization_entry.get(),
                    phone_entry.get(),
                    department_entry.get()
                )
            )

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Doctor added successfully!"
            )

            win.destroy()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        win,
        text="Add Doctor",
        command=save_doctor,
        width=20
    ).pack(pady=20)


def view_doctors():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM doctors ORDER BY doctor_id"
        )

        doctors = cursor.fetchall()

        cursor.close()
        conn.close()

        if not doctors:
            messagebox.showinfo(
                "Doctors",
                "No doctors found."
            )
            return

        text = ""

        for d in doctors:
            text += (
                f"ID: {d['doctor_id']}\n"
                f"Name: {d['name']}\n"
                f"Specialization: {d['specialization']}\n"
                f"Phone: {d['phone']}\n"
                f"Department: {d['department']}\n"
                f"{'-' * 40}\n"
            )

        messagebox.showinfo("Doctor List", text)

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def search_doctor():
    win = tk.Toplevel()
    win.title("Search Doctor")
    win.geometry("350x200")

    tk.Label(
        win,
        text="Enter Doctor ID"
    ).pack(pady=10)

    id_entry = tk.Entry(win)
    id_entry.pack()

    def search():
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM doctors WHERE doctor_id = %s",
                (id_entry.get(),)
            )

            doctor = cursor.fetchone()

            cursor.close()
            conn.close()

            if doctor:
                messagebox.showinfo(
                    "Doctor Found",
                    f"Doctor ID: {doctor['doctor_id']}\n"
                    f"Name: {doctor['name']}\n"
                    f"Specialization: {doctor['specialization']}\n"
                    f"Phone: {doctor['phone']}\n"
                    f"Department: {doctor['department']}"
                )
            else:
                messagebox.showwarning(
                    "Not Found",
                    "Doctor not found."
                )

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        win,
        text="Search",
        command=search,
        width=15
    ).pack(pady=20)


def delete_doctor():
    win = tk.Toplevel()
    win.title("Delete Doctor")
    win.geometry("350x200")

    tk.Label(
        win,
        text="Enter Doctor ID"
    ).pack(pady=10)

    id_entry = tk.Entry(win)
    id_entry.pack()

    def delete():
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM doctors WHERE doctor_id = %s",
                (id_entry.get(),)
            )

            doctor = cursor.fetchone()

            if not doctor:
                messagebox.showwarning(
                    "Not Found",
                    "Doctor not found."
                )
                cursor.close()
                conn.close()
                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this doctor?"
            )

            if confirm:
                cursor.execute(
                    "DELETE FROM doctors WHERE doctor_id = %s",
                    (id_entry.get(),)
                )

                conn.commit()

                messagebox.showinfo(
                    "Deleted",
                    "Doctor deleted successfully!"
                )

                win.destroy()

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        win,
        text="Delete",
        command=delete,
        width=15
    ).pack(pady=20)


def open_doctor_management():
    win = tk.Toplevel()
    win.title("Doctor Management")
    win.geometry("400x400")

    tk.Label(
        win,
        text="Doctor Management",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Button(
        win,
        text="Add Doctor",
        command=add_doctor,
        width=25
    ).pack(pady=10)

    tk.Button(
        win,
        text="View Doctors",
        command=view_doctors,
        width=25
    ).pack(pady=10)

    tk.Button(
        win,
        text="Search Doctor",
        command=search_doctor,
        width=25
    ).pack(pady=10)

    tk.Button(
        win,
        text="Delete Doctor",
        command=delete_doctor,
        width=25
    ).pack(pady=10)


# ================= APPOINTMENT MANAGEMENT =================

def add_appointment():
    win = tk.Toplevel()
    win.title("Add Appointment")
    win.geometry("450x450")

    tk.Label(win, text="Patient ID").pack(pady=5)
    patient_entry = tk.Entry(win)
    patient_entry.pack()

    tk.Label(win, text="Doctor ID").pack(pady=5)
    doctor_entry = tk.Entry(win)
    doctor_entry.pack()

    tk.Label(
        win,
        text="Date (YYYY-MM-DD)"
    ).pack(pady=5)

    date_entry = tk.Entry(win)
    date_entry.pack()

    tk.Label(
        win,
        text="Time (HH:MM)"
    ).pack(pady=5)

    time_entry = tk.Entry(win)
    time_entry.pack()

    tk.Label(win, text="Reason").pack(pady=5)
    reason_entry = tk.Entry(win)
    reason_entry.pack()

    def save_appointment():
        patient_id = patient_entry.get()
        doctor_id = doctor_entry.get()
        date = date_entry.get()
        time = time_entry.get()
        reason = reason_entry.get()

        try:
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror(
                "Invalid Date/Time",
                "Use Date: YYYY-MM-DD\nTime: HH:MM"
            )
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT patient_id FROM patients WHERE patient_id = %s",
                (patient_id,)
            )

            if not cursor.fetchone():
                messagebox.showerror(
                    "Error",
                    "Patient does not exist."
                )
                cursor.close()
                conn.close()
                return

            cursor.execute(
                "SELECT doctor_id FROM doctors WHERE doctor_id = %s",
                (doctor_id,)
            )

            if not cursor.fetchone():
                messagebox.showerror(
                    "Error",
                    "Doctor does not exist."
                )
                cursor.close()
                conn.close()
                return

            query = """
                INSERT INTO appointments
                (patient_id, doctor_id, appointment_date,
                 appointment_time, reason)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    patient_id,
                    doctor_id,
                    date,
                    time,
                    reason
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Appointment added successfully!"
            )

            win.destroy()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        win,
        text="Add Appointment",
        command=save_appointment,
        width=20
    ).pack(pady=20)


def view_appointments():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
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
        """

        cursor.execute(query)
        appointments = cursor.fetchall()

        cursor.close()
        conn.close()

        if not appointments:
            messagebox.showinfo(
                "Appointments",
                "No appointments found."
            )
            return

        text = ""

        for a in appointments:
            text += (
                f"Appointment ID: {a['appointment_id']}\n"
                f"Patient: {a['patient_name']}\n"
                f"Doctor: {a['doctor_name']}\n"
                f"Date: {a['appointment_date']}\n"
                f"Time: {a['appointment_time']}\n"
                f"Reason: {a['reason']}\n"
                f"{'-' * 40}\n"
            )

        messagebox.showinfo(
            "Appointment List",
            text
        )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def search_appointment():
    win = tk.Toplevel()
    win.title("Search Appointment")
    win.geometry("350x200")

    tk.Label(
        win,
        text="Enter Appointment ID"
    ).pack(pady=10)

    id_entry = tk.Entry(win)
    id_entry.pack()

    def search():
        try:
            conn = connect_db()
            cursor = conn.cursor()

            query = """
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
            """

            cursor.execute(
                query,
                (id_entry.get(),)
            )

            appointment = cursor.fetchone()

            cursor.close()
            conn.close()

            if appointment:
                messagebox.showinfo(
                    "Appointment Found",
                    f"Appointment ID: {appointment['appointment_id']}\n"
                    f"Patient: {appointment['patient_name']}\n"
                    f"Doctor: {appointment['doctor_name']}\n"
                    f"Date: {appointment['appointment_date']}\n"
                    f"Time: {appointment['appointment_time']}\n"
                    f"Reason: {appointment['reason']}"
                )

            else:
                messagebox.showwarning(
                    "Not Found",
                    "Appointment not found."
                )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        win,
        text="Search",
        command=search,
        width=15
    ).pack(pady=20)


def delete_appointment():
    win = tk.Toplevel()
    win.title("Delete Appointment")
    win.geometry("350x200")

    tk.Label(
        win,
        text="Enter Appointment ID"
    ).pack(pady=10)

    id_entry = tk.Entry(win)
    id_entry.pack()

    def delete():
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT appointment_id FROM appointments "
                "WHERE appointment_id = %s",
                (id_entry.get(),)
            )

            appointment = cursor.fetchone()

            if not appointment:
                messagebox.showwarning(
                    "Not Found",
                    "Appointment not found."
                )
                cursor.close()
                conn.close()
                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this appointment?"
            )

            if confirm:
                cursor.execute(
                    "DELETE FROM appointments WHERE appointment_id = %s",
                    (id_entry.get(),)
                )

                conn.commit()

                messagebox.showinfo(
                    "Deleted",
                    "Appointment deleted successfully!"
                )

                win.destroy()

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        win,
        text="Delete",
        command=delete,
        width=15
    ).pack(pady=20)


def open_appointment_management():
    win = tk.Toplevel()
    win.title("Appointment Management")
    win.geometry("400x400")

    tk.Label(
        win,
        text="Appointment Management",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Button(
        win,
        text="Add Appointment",
        command=add_appointment,
        width=25
    ).pack(pady=10)

    tk.Button(
        win,
        text="View Appointments",
        command=view_appointments,
        width=25
    ).pack(pady=10)

    tk.Button(
        win,
        text="Search Appointment",
        command=search_appointment,
        width=25
    ).pack(pady=10)

    tk.Button(
        win,
        text="Delete Appointment",
        command=delete_appointment,
        width=25
    ).pack(pady=10)


# ================= BILLING MANAGEMENT =================

def open_billing_management():
    win = tk.Toplevel()
    win.title("Billing Management")
    win.geometry("450x500")

    tk.Label(
        win,
        text="Billing Management",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(win, text="Patient ID").pack(pady=5)
    patient_entry = tk.Entry(win)
    patient_entry.pack()

    tk.Label(
        win,
        text="Consultation Fee"
    ).pack(pady=5)

    consultation_entry = tk.Entry(win)
    consultation_entry.pack()

    tk.Label(
        win,
        text="Medicine Charge"
    ).pack(pady=5)

    medicine_entry = tk.Entry(win)
    medicine_entry.pack()

    tk.Label(
        win,
        text="Other Charge"
    ).pack(pady=5)

    other_entry = tk.Entry(win)
    other_entry.pack()

    def create_bill():
        try:
            patient_id = patient_entry.get()

            consultation = float(
                consultation_entry.get() or 0
            )

            medicine = float(
                medicine_entry.get() or 0
            )

            other = float(
                other_entry.get() or 0
            )

            total = consultation + medicine + other

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Charges must be numbers."
            )
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT patient_id FROM patients WHERE patient_id = %s",
                (patient_id,)
            )

            if not cursor.fetchone():
                messagebox.showerror(
                    "Error",
                    "Patient does not exist."
                )
                cursor.close()
                conn.close()
                return

            query = """
                INSERT INTO bills
                (
                    patient_id,
                    consultation_fee,
                    medicine_charge,
                    other_charge,
                    total_amount,
                    bill_date
                )
                VALUES (%s, %s, %s, %s, %s, CURDATE())
            """

            cursor.execute(
                query,
                (
                    patient_id,
                    consultation,
                    medicine,
                    other,
                    total
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Bill Created",
                f"Bill created successfully!\n\n"
                f"Total Amount: ₹{total:.2f}"
            )

            win.destroy()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def view_bills():
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    bill_id,
                    patient_id,
                    consultation_fee,
                    medicine_charge,
                    other_charge,
                    total_amount,
                    bill_date
                FROM bills
                ORDER BY bill_id
                """
            )

            bills = cursor.fetchall()

            cursor.close()
            conn.close()

            if not bills:
                messagebox.showinfo(
                    "Bills",
                    "No bills found."
                )
                return

            text = ""

            for b in bills:
                text += (
                    f"Bill ID: {b['bill_id']}\n"
                    f"Patient ID: {b['patient_id']}\n"
                    f"Consultation: ₹{float(b['consultation_fee']):.2f}\n"
                    f"Medicine: ₹{float(b['medicine_charge']):.2f}\n"
                    f"Other Charges: ₹{float(b['other_charge']):.2f}\n"
                    f"Total: ₹{float(b['total_amount']):.2f}\n"
                    f"Date: {b['bill_date']}\n"
                    f"{'-' * 40}\n"
                )

            messagebox.showinfo(
                "Bill List",
                text
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def delete_bill():
        delete_win = tk.Toplevel()
        delete_win.title("Delete Bill")
        delete_win.geometry("350x200")

        tk.Label(
            delete_win,
            text="Enter Bill ID"
        ).pack(pady=10)

        bill_id_entry = tk.Entry(delete_win)
        bill_id_entry.pack()

        def delete():
            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT bill_id FROM bills WHERE bill_id = %s",
                    (bill_id_entry.get(),)
                )

                bill = cursor.fetchone()

                if not bill:
                    messagebox.showwarning(
                        "Not Found",
                        "Bill not found."
                    )
                    cursor.close()
                    conn.close()
                    return

                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    "Are you sure you want to delete this bill?"
                )

                if confirm:
                    cursor.execute(
                        "DELETE FROM bills WHERE bill_id = %s",
                        (bill_id_entry.get(),)
                    )

                    conn.commit()

                    messagebox.showinfo(
                        "Deleted",
                        "Bill deleted successfully!"
                    )

                    delete_win.destroy()

                cursor.close()
                conn.close()

            except Exception as e:
                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

        tk.Button(
            delete_win,
            text="Delete Bill",
            command=delete,
            width=15
        ).pack(pady=20)

    tk.Button(
        win,
        text="Create Bill",
        command=create_bill,
        width=25
    ).pack(pady=15)

    tk.Button(
        win,
        text="View Bills",
        command=view_bills,
        width=25
    ).pack(pady=10)

    tk.Button(
        win,
        text="Delete Bill",
        command=delete_bill,
        width=25
    ).pack(pady=10)


# ================= DASHBOARD =================

def open_dashboard():
    dashboard = tk.Tk()
    dashboard.title("Hospital Management System")
    dashboard.geometry("500x550")

    tk.Label(
        dashboard,
        text="Hospital Management System",
        font=("Arial", 20, "bold")
    ).pack(pady=30)

    buttons = [
        "Dashboard",
        "Patient Management",
        "Doctor Management",
        "Appointment Management",
        "Billing Management",
        "Logout"
    ]

    for text in buttons:

        button = tk.Button(
            dashboard,
            text=text,
            width=30,
            height=2
        )

        if text == "Dashboard":
            button.config(
                command=lambda: messagebox.showinfo(
                    "Dashboard",
                    "Welcome to Hospital Management System!"
                )
            )

        elif text == "Patient Management":
            button.config(
                command=open_patient_management
            )

        elif text == "Doctor Management":
            button.config(
                command=open_doctor_management
            )

        elif text == "Appointment Management":
            button.config(
                command=open_appointment_management
            )

        elif text == "Billing Management":
            button.config(
                command=open_billing_management
            )

        elif text == "Logout":
            button.config(
                command=dashboard.destroy
            )

        button.pack(pady=8)

    dashboard.mainloop()


# ================= LOGIN WINDOW =================

login_window = tk.Tk()
login_window.title("Hospital Management Login")
login_window.geometry("400x300")

tk.Label(
    login_window,
    text="Hospital Management System",
    font=("Arial", 18, "bold")
).pack(pady=25)

tk.Label(
    login_window,
    text="Username"
).pack()

username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

tk.Label(
    login_window,
    text="Password"
).pack()

password_entry = tk.Entry(
    login_window,
    show="*"
)
password_entry.pack(pady=5)

tk.Button(
    login_window,
    text="Login",
    command=login,
    width=20
).pack(pady=20)

login_window.mainloop()

