# 💼 Salary Management System

A simple GUI-based Salary Management System built using **Python**, **Tkinter**, and **MySQL**, allowing HR to manage employees' salary records and enabling employees to securely view their salary details using an access code.

## 🧰 Features

### HR Dashboard
- View all employee records in a tabular format.
- View total **Gross Salary** and **Annual Salary** of the company.
- Add new employees with an automatically generated **Access Code**.
- Delete existing employees.
- Update employee salaries with fields like **allowances**, **deductions**, **PF%**, and track **salary history**.
- Search employee records.
- Download employee details as a **PDF report** with company totals.
- Logout functionality to switch back to login screen.

### Employee Dashboard
- Secure login using **Employee ID** and **Access Code**.
- View basic, gross, net, and annual salary details.
- Option to **download PDF** of their salary details.

---
## 🖼️ Screenshots


### 🧑‍💼 HR Dashboard
![image](https://github.com/user-attachments/assets/db0daf36-43e7-4727-8807-0831588edc68)


### 📄 Add Employee
![image](https://github.com/user-attachments/assets/47e55bd0-0c7b-4b91-a3d6-4fe6eeeeff5b)


### 📥 Download PDF Prompt
![image](https://github.com/user-attachments/assets/7b24b29e-e409-4bb3-a852-1c410ca18e97)


### 🗂️ Employee Dashboard
![image](https://github.com/user-attachments/assets/4ad06292-6e7a-4e01-a871-b28bc407a6b7)




---
## 🖥️ Technologies Used

- **Frontend**: Tkinter (Python GUI)
- **Backend**: MySQL
- **PDF Generation**: `reportlab`
- **Python Libraries**:
  - `mysql.connector`
  - `tkinter`
  - `reportlab`
  - `random`, `string`, `datetime`

---

## 🗃️ Database Structure

### Database: `salary_db`

#### Table: `employees`
| Column         | Type         |
|----------------|--------------|
| emp_id         | VARCHAR(10)  |
| access_code    | VARCHAR(10)  |
| name           | VARCHAR(50)  |
| position       | VARCHAR(50)  |
| basic_salary   | FLOAT        |
| allowances     | FLOAT        |
| deductions     | FLOAT        |
| pf_percentage  | FLOAT        |
| gross_salary   | FLOAT        |
| net_salary     | FLOAT        |
| annual_salary  | FLOAT        |

#### Table: `salary_history`
| Column        | Type         |
|---------------|--------------|
| id            | INT (PK)     |
| emp_id        | VARCHAR(10)  |
| old_salary    | FLOAT        |
| new_salary    | FLOAT        |
| reason        | TEXT         |
| pf            | FLOAT        |
| gross         | FLOAT        |
| net           | FLOAT        |
| annual        | FLOAT        |

---

## 🚀 How to Run

1. Make sure **MySQL** is installed and running.
2. Create the database and required tables using the schema above.
3. Install required Python libraries:

   ```bash
   pip install mysql-connector-python reportlab



