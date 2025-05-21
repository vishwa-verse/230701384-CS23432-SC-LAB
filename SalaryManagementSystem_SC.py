import tkinter as tk
from tkinter import font, messagebox, ttk
import mysql.connector
from mysql.connector import errorcode
import random
import string



from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
from tkinter import filedialog


from reportlab.lib.pagesizes import A4
from datetime import datetime

        
class SalaryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Salary Management System")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e2f")  

        self.custom_font = font.Font(family="Segoe UI", size=20, weight="bold")
        self.button_font = font.Font(family="Segoe UI", size=14)

        self.create_tables()  # Auto create required tables
        self.setup_login_page()

    def create_tables(self):
        try:
            db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Realme6pro",
                database="salary_db"
            )
            cursor = db.cursor()
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                emp_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                position VARCHAR(100),
                salary FLOAT
            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS salary_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                emp_id VARCHAR(20),
                old_salary FLOAT,
                new_salary FLOAT,
                change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reason VARCHAR(255),
                FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE CASCADE
            )''')

            
            '''
                ALTER TABLE employees ADD COLUMN access_code VARCHAR(10) UNIQUE;
                
                ALTER TABLE employees
                ADD COLUMN allowances DOUBLE DEFAULT 0,
                ADD COLUMN deductions DOUBLE DEFAULT 0,
                ADD COLUMN pf_percentage DOUBLE DEFAULT 12,
                ADD COLUMN gross_salary DOUBLE DEFAULT 0,
                ADD COLUMN net_salary DOUBLE DEFAULT 0,
                ADD COLUMN annual_salary DOUBLE DEFAULT 0;

                ALTER TABLE salary_history
                ADD COLUMN pf DOUBLE DEFAULT 0,
                ADD COLUMN gross DOUBLE DEFAULT 0,
                ADD COLUMN net DOUBLE DEFAULT 0,
                ADD COLUMN annual DOUBLE DEFAULT 0;
            '''

            db.commit()
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error creating tables: {str(e)}")

    def setup_login_page(self):
        self.clear_frame()

        self.login_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.login_frame.place(relx=0.5, rely=0.5, anchor='center')

        title = tk.Label(self.login_frame, text="Welcome to Salary Management System", 
                         font=self.custom_font, fg="#ffffff", bg="#1e1e2f")
        title.pack(pady=30)

        emp_btn = tk.Button(self.login_frame, text="Login as Employee", font=self.button_font,
                            bg="#0077b6", fg="white", activebackground="#023e8a",
                            padx=20, pady=10, width=20, command=self.open_employee_dashboard,
                            bd=0, relief="flat", cursor="hand2")
        emp_btn.pack(pady=15)

        hr_btn = tk.Button(self.login_frame, text="Login as HR", font=self.button_font,
                           bg="#d62828", fg="white", activebackground="#9d0208",
                           padx=20, pady=10, width=20, command=lambda: HRLogin(self.root, self),####
                           bd=0, relief="flat", cursor="hand2")
        hr_btn.pack(pady=15)

    def open_employee_dashboard(self, emp_id=None):
        self.clear_frame()
        if emp_id:
            EmployeeDashboard(self.root, emp_id)
        else:
            EmployeeLogin(self.root, self)

    

    

    def open_hr_dashboard(self):
        self.clear_frame()
        HRDashboard(self.root)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
# Employee Dashboard
class EmployeeLogin:
    def __init__(self, root, app):
        self.root = root
        self.app = app

        self.frame = tk.Frame(root, bg="grey")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.frame, text="Employee Login", font=("Segoe UI", 18, "bold"), fg="white", bg="#1e1e2f").pack(pady=20)

        self.emp_id = tk.Entry(self.frame, font=("Segoe UI", 12))
        self.emp_id.pack(pady=5)
        self.emp_id.insert(0, "Employee ID")

        self.emp_code = tk.Entry(self.frame, font=("Segoe UI", 12))
        self.emp_code.pack(pady=5)
        self.emp_code.insert(0, "Access Code")

        tk.Button(self.frame, text="Login", font=("Segoe UI", 12), bg="#00adb5", fg="white", command=self.login).pack(pady=10)
        tk.Button(self.frame, text="Back", font=("Segoe UI", 12), bg="#393e46", fg="white", command=self.back).pack(pady=5)

    def login(self):
        emp_id = self.emp_id.get()
        emp_code = self.emp_code.get()
        try:
            db = mysql.connector.connect(host="127.0.0.1", user="root", password="Realme6pro", database="salary_db")
            cursor = db.cursor()
            cursor.execute("SELECT emp_id FROM employees WHERE emp_id = %s AND access_code = %s", (emp_id, emp_code))
            result = cursor.fetchone()
            db.close()
            if result:
                self.frame.destroy()
                self.app.open_employee_dashboard(emp_id)
            else:
                messagebox.showerror("Login Failed", "Invalid ID or Code")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def back(self):
        self.frame.destroy()
        self.app.setup_login_page()

class EmployeeDashboard:
    def __init__(self, root, emp_id):
        self.root = root
        self.emp_id = emp_id

        self.frame = tk.Frame(root, bg="#222831")
        self.frame.pack(fill="both", expand=True)

        title = tk.Label(self.frame, text=f"Employee Dashboard - {emp_id}", font=("Segoe UI", 25, "bold"), fg="cyan", bg="black")
        title.pack(pady=10)

        self.info_label = tk.Label(self.frame, text="", font=("Segoe UI", 18), fg="white", bg="#222831")
        self.info_label.pack(pady=10)

        self.salary_history_tree = ttk.Treeview(self.frame, columns=("Old Salary", "New Salary", "Change Date", "Reason"), show='headings')
        for col in ("Old Salary", "New Salary", "Change Date", "Reason"):
            self.salary_history_tree.heading(col, text=col)
            self.salary_history_tree.column(col, width=150)
        self.salary_history_tree.pack(fill="both", expand=True, padx=20, pady=20)

        ##download#####
        tk.Button(self.frame, text="Generate Report(PDF)", font=("Segoe UI", 12), bg="cyan", fg="black", padx=20, pady=10, command=self.download_pdf).pack(pady=5)

        tk.Button(self.frame, text="Logout", font=("Segoe UI", 12), bg="#393e46", fg="white", padx=20, pady=10, command=self.logout).pack(pady=10)

        

        self.load_employee_info()
        self.load_salary_history()

    def connect_db(self):
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Realme6pro",
            database="salary_db"
        )

    def load_employee_info(self):
        try:
            db = self.connect_db()
            cursor = db.cursor()
            cursor.execute("""
            SELECT emp_id, name, position, basic_salary, allowances, deductions, 
                   pf_percentage, gross_salary, net_salary, annual_salary 
            FROM employees 
            WHERE emp_id = %s
            """, (self.emp_id,))
            result = cursor.fetchone()
            db.close()
            if result:
                (emp_id, name, position, basic_salary, allowances, deductions,
             pf_percentage, gross_salary, net_salary, annual_salary) = result

                info_text = (
                    f"{'Employee ID':<20}: {emp_id}   |    {'Name':<20}:  {name}   |   {'Position':<20}: {position}\n"
                    f"{'Basic Salary':<20}: ${basic_salary:,.2f}   |   {'Allowances':<20}: ${allowances:,.2f}   |   {'Deductions':<20}: ${deductions:,.2f}\n"
                    f"    | {'Provident Fund (%)':<20}:{pf_percentage:.2f}% |\n"
                    f"    | {'Gross Salary':<20}:     ${gross_salary:,.2f} |\n"
                    f"    | {'CURRENT Net Salary':<20}:${net_salary:,.2f} |\n"
                    f"    | {'Annual Salary':<20}:    ${annual_salary:,.2f} |\n\n"
                    f"{'='*40}\n"
                    f"   {'Salary Update History':^40}\n"
                    f"{'='*40}"
                )
                self.info_label.config(text=info_text,font=("Segoe UI", 16), justify="left")

                note_text = (
                    "  Gross Salary = Basic Pay + Allowances\n"
                    "  PF Amount = (Basic Pay × PF%) / 100\n"
                    "  Net Salary = Gross - Deductions - PF\n"
                    "  Annual Salary = Net × 12"
                )
                self.note_label = tk.Label(self.frame, text=note_text, font=("Segoe UI", 9), fg="gray", bg="#f0f0f0", justify="left", anchor="w")
                self.note_label.pack(anchor="w", padx=20, pady=(1, 10))

            else:
                self.info_label.config(text="Employee details not found.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def load_salary_history(self):
        
        for row in self.salary_history_tree.get_children():
            self.salary_history_tree.delete(row)

        try:
            db = self.connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT old_salary, new_salary, change_date, reason FROM salary_history WHERE emp_id = %s ORDER BY change_date DESC", (self.emp_id,))
            rows = cursor.fetchall()
            db.close()

            for row in rows:
                self.salary_history_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    


    def download_pdf(self):
        try:
            # Ask user where to save
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                                     filetypes=[("PDF files", "*.pdf")],
                                                     title="Save PDF as",
                                                     initialfile=f"{self.emp_id}_salary_report.pdf")
            if not file_path:
                return  # Cancelled

            # Create canvas
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter

            # Header
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 50, f"Salary Report for Employee ID: {self.emp_id}")
            c.setFont("Helvetica", 10)
            c.drawString(50, height - 65, f"Generated on: {current_time}")
            c.line(50, height - 70, width - 50, height - 70)

            y = height - 90

            # Info Text
            c.setFont("Helvetica", 10)
            for line in self.info_label.cget("text").split("\n"):
                c.drawString(50, y, line.strip())
                y -= 14
                if y < 100:
                    c.showPage()
                    y = height - 50

            y -= 20
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Salary History:")
            y -= 20

            # Table Header
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y, "Old Salary")
            c.drawString(150, y, "New Salary")
            c.drawString(270, y, "Change Date")
            c.drawString(400, y, "Reason")
            y -= 15
            c.setFont("Helvetica", 10)

            # Fetch and print salary history
            db = self.connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT old_salary, new_salary, change_date, reason FROM salary_history WHERE emp_id = %s ORDER BY change_date DESC", (self.emp_id,))
            rows = cursor.fetchall()
            db.close()

            for row in rows:
                old_salary, new_salary, change_date, reason = row
                c.drawString(50, y, f"${old_salary:,.2f}")
                c.drawString(150, y, f"${new_salary:,.2f}")
                c.drawString(270, y, str(change_date))
                c.drawString(400, y, reason[:30])  # truncate long reasons
                y -= 15
                if y < 100:
                    c.showPage()
                    y = height - 50

            c.save()
            messagebox.showinfo("Success", "PDF downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def logout(self):
        self.frame.destroy()
        app.setup_login_page()
        

class HRLogin:

    #predefined HRs
    
    HR_CREDENTIALS = {
        "384": "384",
        "386": "386",
        "382": "382",
        "355": "355"
    }

    def __init__(self, root, app):
        self.root = root
        self.app = app

        self.frame = tk.Frame(root, bg="green")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.frame, text="HR Login", font=("Segoe UI", 18, "bold"), fg="white", bg="#1e1e2f").pack(pady=20)

        self.username_entry = tk.Entry(self.frame, font=("Segoe UI", 12))
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, "Username")

        self.password_entry = tk.Entry(self.frame, font=("Segoe UI", 12), show="*")
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, "Password")

        tk.Button(self.frame, text="Login", font=("Segoe UI", 12), bg="#00adb5", fg="white", command=self.login).pack(pady=10)
        tk.Button(self.frame, text="Back", font=("Segoe UI", 12), bg="#393e46", fg="white", command=self.back).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in HRLogin.HR_CREDENTIALS and HRLogin.HR_CREDENTIALS[username] == password:
            messagebox.showinfo("Login Successful", f"Welcome {username.title()}!")
            self.frame.destroy()
            HRDashboard(self.root)  # Launch HR dashboard here
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def back(self):
        self.frame.destroy()
        self.app.setup_login_page()


# HR Dashboard 
class HRDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Dashboard")

        self.frame = tk.Frame(root, bg="#222831")
        self.frame.pack(fill='both', expand=True)

        title = tk.Label(self.frame, text="HR Dashboard", font=("Segoe UI", 25, "bold"), fg="cyan", bg="black")
        title.pack(pady=10)

        self.totals_label = tk.Label(self.frame, text="", font=("Segoe UI", 20), fg="white", bg="#222831")
        self.totals_label.pack(pady=(0, 10))

        


        content = tk.Frame(self.frame, bg="#222831")
        content.pack(fill="both", expand=True, padx=20, pady=10)

        ##download
        tk.Button(content, text="Generate Report(PDF)", command=self.download_pdf_report, padx=10, pady=10, bg="cyan").pack(pady=5)

        # Left side - Employee list
        self.tree = ttk.Treeview(content, columns=("EmployeeID", "Access code", "Name", "Position", "Basic Salary", "Gross Salary", "Net Salary", "Annual Salary"), show='headings')
        for col in ("EmployeeID", "Access code", "Name", "Position", "Basic Salary", "Gross Salary", "Net Salary", "Annual Salary"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(side="left", fill="both", expand=True)

        self.load_employees()

        # Right side - Buttons
        right_frame = tk.Frame(content, bg="#222831")
        right_frame.pack(side="right", fill="y", padx=10)

        btn_style = {"font": ("Segoe UI", 11), "bg": "#00adb5", "fg": "yellow", "padx": 10, "pady": 10,
                     "bd": 0, "relief": "flat", "cursor": "hand2", "width": 18}

        tk.Button(right_frame, text="Add Employee", command=self.add_employee_popup, **btn_style).pack(pady=5)
        tk.Button(right_frame, text="Delete Employee", command=self.delete_employee_popup, **btn_style).pack(pady=5)
        tk.Button(right_frame, text="Update Salary", command=self.update_salary_popup, **btn_style).pack(pady=5)
        #tk.Button(right_frame, text="Bulk Update", command=self.bulk_update_popup, **btn_style).pack(pady=5)
        tk.Button(right_frame, text="Search Employee", command=self.search_employee_popup, **btn_style).pack(pady=5)
        tk.Button(right_frame, text="Salary History", command=self.salary_history_popup, **btn_style).pack(pady=5)

        tk.Button(right_frame, text="Logout", command=self.go_back, bg="#393e46", fg="white", padx=10, pady=10,
                  bd=0, cursor="hand2", relief="flat", width=18).pack(pady=30)

    def connect_db(self):
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Realme6pro",
            database="salary_db"
        )

    def load_employees(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            db = self.connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT emp_id, access_code, name, position, basic_salary, gross_salary, net_salary, annual_salary FROM employees")
            gross_total = 0
            annual_total = 0

            for emp in cursor.fetchall():
                self.tree.insert("", "end", values=emp)
                gross_total += float(emp[5]) if emp[5] else 0  # gross_salary
                annual_total += float(emp[7]) if emp[7] else 0  # annual_salary

            self.totals_label.config(text=f"Total Gross Salary: ${gross_total:,.2f}    |    Total Annual Salary: ${annual_total:,.2f}")
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def generate_access_code(self, length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def add_employee_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Add Employee")
        win.geometry("500x400")
        win.configure(bg="#393e46")

        entries = {}
        for idx, field in enumerate(["Employee ID", "Name", "Position", "Basic Salary"]):
            tk.Label(win, text=field, font=("Segoe UI", 12), fg="white", bg="#393e46").pack(pady=(10, 0))
            entries[field] = tk.Entry(win, font=("Segoe UI", 12))
            entries[field].pack(pady=5)

        def submit():
            try:
                access_code = self.generate_access_code()
                db = self.connect_db()
                cursor = db.cursor()
                cursor.execute("INSERT INTO employees (emp_id, name, position, basic_salary, access_code) VALUES (%s, %s, %s, %s, %s)",
                               (entries["Employee ID"].get(), entries["Name"].get(), entries["Position"].get(), entries["Basic Salary"].get(), access_code))
                db.commit()
                db.close()
                messagebox.showinfo("Success", f"Employee Added!\nAccess Code: {access_code}")
                win.destroy()
                self.load_employees()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Submit", font=("Segoe UI", 12), bg="#00adb5", fg="white", command=submit).pack(pady=20)

    def delete_employee_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Delete Employee")
        win.geometry("400x200")
        win.configure(bg="#393e46")

        tk.Label(win, text="Employee ID to Delete", font=("Segoe UI", 12), fg="white", bg="#393e46").pack(pady=(20, 5))
        emp_id_entry = tk.Entry(win, font=("Segoe UI", 12))
        emp_id_entry.pack(pady=5)

        def delete():
            try:
                emp_id = emp_id_entry.get()
                db = self.connect_db()
                cursor = db.cursor()

                cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
                if cursor.rowcount == 0:
                    raise ValueError(f"No employee found with ID {emp_id}")

                db.commit()
                db.close()
                messagebox.showinfo("Deleted", "Employee Deleted Successfully!")
                win.destroy()
                self.load_employees()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Delete", font=("Segoe UI", 12), bg="#d62828", fg="white", command=delete).pack(pady=20)

    def update_salary_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Update Salary")
        win.geometry("500x500")
        win.configure(bg="#393e46")

        fields = ["Employee ID", "Basic Salary", "Allowances", "Deductions", "PF %", "Reason"]
        entries = {}
        for field in fields:
            tk.Label(win, text=field, font=("Segoe UI", 12), fg="white", bg="#393e46").pack(pady=(10, 0))
            entries[field] = tk.Entry(win, font=("Segoe UI", 12))
            entries[field].pack(pady=5)

        def update():
            try:
                emp_id = entries["Employee ID"].get()
                basic = float(entries["Basic Salary"].get())
                allowances = float(entries["Allowances"].get())
                deductions = float(entries["Deductions"].get())
                pf = float(entries["PF %"].get())
                reason = entries["Reason"].get()

                gross = basic + allowances
                pf_amount = (basic * pf) / 100
                net = gross - deductions - pf_amount
                annual = net * 12

                db = self.connect_db()
                cursor = db.cursor()

                cursor.execute("SELECT net_salary FROM employees WHERE emp_id = %s", (emp_id,))
                result = cursor.fetchone()
                if not result:
                    messagebox.showerror("Error", "Employee ID not found.")
                    return
                old_salary = result[0]

                cursor.execute("UPDATE employees SET basic_salary = %s, allowances = %s, deductions = %s, pf_percentage = %s, gross_salary = %s, net_salary = %s, annual_salary = %s WHERE emp_id = %s",
                               (basic, allowances, deductions, pf, gross, net, annual, emp_id))
                #both new_salary and net are same
                cursor.execute("INSERT INTO salary_history (emp_id, old_salary, new_salary, reason, pf, gross, net, annual) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                               (emp_id, old_salary, net, reason, pf_amount, gross, net, annual))

                db.commit()
                db.close()
                messagebox.showinfo("Updated", "Salary Updated Successfully!")
                win.destroy()
                self.load_employees()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Update", font=("Segoe UI", 12), bg="#2196F3", fg="white", command=update).pack(pady=20)
    '''
    def bulk_update_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Bulk Salary Update")
        win.geometry("500x400")
        win.configure(bg="#393e46")

        tk.Label(win, text="Percentage Increase in Gross Salary", font=("Segoe UI", 12), fg="white", bg="#393e46").pack(pady=(30, 10))
        percent_entry = tk.Entry(win, font=("Segoe UI", 12))
        percent_entry.pack(pady=5)

        tk.Label(win, text="Reason for Update", font=("Segoe UI", 12), fg="white", bg="#393e46").pack(pady=(20, 10))
        reason_entry = tk.Entry(win, font=("Segoe UI", 12))
        reason_entry.pack(pady=5)

        def apply_bulk():
            try:
                percent = float(percent_entry.get())
                reason = reason_entry.get()
                db = self.connect_db()
                cursor = db.cursor()
                
                
                
                cursor.execute("SELECT emp_id, basic_salary FROM employees")
                for emp_id, salary in cursor.fetchall():
                    new_salary = salary + (salary * percent / 100)
                    cursor.execute("UPDATE employees SET basic_salary = %s WHERE emp_id = %s", (new_salary, emp_id))
                    
                    cursor.execute("SELECT deductions FROM employees WHERE emp_id = %s", (emp_id,))
                    deductions = cursor.fetchone()[0]

                    net = new_salary - deductions
                    cursor.execute("UPDATE employees SET net_salary = %s WHERE emp_id = %s", (net, emp_id))

                    
                    ####change net and annual
                    
                    cursor.execute("INSERT INTO salary_history (emp_id, old_salary, new_salary, reason) VALUES (%s, %s, %s, %s)",
                                   (emp_id, salary, new_salary, reason))
                db.commit()
                db.close()
                messagebox.showinfo("Success", "Bulk Salary Update Applied!")
                win.destroy()
                self.load_employees()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Apply Update", font=("Segoe UI", 12), bg="#00adb5", fg="white", command=apply_bulk).pack(pady=30)
    '''

    def search_employee_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Search Employee")
        win.geometry("400x250")
        win.configure(bg="#393e46")

        tk.Label(win, text="Enter Employee ID", font=("Segoe UI", 12), fg="white", bg="#393e46").pack(pady=10)
        entry = tk.Entry(win, font=("Segoe UI", 12))
        entry.pack(pady=5)

        result_label = tk.Label(win, font=("Segoe UI", 20), fg="white", bg="#393e46")
        result_label.pack(pady=20)

        def search():
            emp_id = entry.get()
            try:
                db = self.connect_db()
                cursor = db.cursor()
                cursor.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
                data = cursor.fetchone()
                db.close()
                if data:
                    result_label.config(text=f"ID: {data[0]} | Name: {data[1]} | Position: {data[2]} | Net Monthly Salary: ${data[9]} | Annaul Salary(CTC) : ${data[10]}")
                else:
                    result_label.config(text="Employee not found")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Search", font=("Segoe UI", 12), bg="#00adb5", fg="white", command=search).pack(pady=10)

    

    def salary_history_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Salary History")
        win.geometry("700x400")
        win.configure(bg="#393e46")

        tree = ttk.Treeview(win, columns=("ID", "Old(Monthly Net)", "New(Monthly Net)", "Date", "Reason"), show='headings')
        for col in ("ID", "Old(Monthly Net)", "New(Monthly Net)", "Date", "Reason"):
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill="both", expand=True)

        try:
            db = self.connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT emp_id, old_salary, new_salary, change_date, reason FROM salary_history ORDER BY change_date DESC")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def download_pdf_report(self):
        try:
            # Ask user for location and file name
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Report As",
                initialfile=f"HR_Report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
            )

            if not file_path:
                return  # User cancelled

            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4

            # Title and timestamp
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "HR Employee Salary Report")
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 70, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Totals
            totals = self.totals_label.cget("text")
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, height - 100, "Summary:")
            c.setFont("Helvetica", 11)
            c.drawString(70, height - 120, totals)

            # Table headers
            y = height - 160
            headers = ("Emp ID", "Access Code", "Name", "Position", "Basic", "Gross", "Net", "Annual")
            col_widths = [60, 90, 90, 80, 60, 60, 60, 70]
            x = 50

            c.setFont("Helvetica-Bold", 10)
            for i, header in enumerate(headers):
                c.drawString(x, y, header)
                x += col_widths[i]

            # Table data
            y -= 20
            c.setFont("Helvetica", 9)
            for row_id in self.tree.get_children():
                x = 50
                values = self.tree.item(row_id)['values']
                for i, value in enumerate(values):
                    c.drawString(x, y, str(value))
                    x += col_widths[i]
                y -= 15
                if y < 50:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 9)

            c.save()
            messagebox.showinfo("PDF Generated", f"Report saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_back(self):
        self.frame.destroy()
        app.setup_login_page()
        


if __name__ == "__main__":
    
    root = tk.Tk()
    global app
    app = SalaryManagementApp(root)
    root.mainloop()

