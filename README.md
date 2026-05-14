# 🩸 Blood Bank Management System

A desktop application built with **Python (Tkinter)** as the frontend and **MySQL** as the backend database to manage blood donors, inventory, requests, and donation records efficiently.

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Screenshots](#screenshots)
- [Modules](#modules)
- [Author](#author)

---

## About

The Blood Bank Management System is a mini project developed as part of the **Database Management Systems** course. It replaces manual paper-based blood bank record keeping with a fast, reliable, and easy-to-use computerized system. The system provides a secure admin login and dedicated modules for managing every aspect of blood bank operations.

---

## Features

- 🔐 Secure admin login with MySQL authentication
- 👤 Add, view, and delete donor records
- ✅ Automatic donor eligibility check (age must be ≥ 18)
- 🩸 Real-time blood inventory tracking per blood group
- ⚠️ Low stock alert when units fall below 5
- 🏥 Blood request management for patients and hospitals
- 📋 Complete donation history log
- 🔍 Search donors by blood group for emergencies
- 📅 Expiry date tracking for stored blood units

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Python 3.14, Tkinter |
| Backend | MySQL 8.0 |
| Connector | mysql-connector-python 9.7.0 |
| IDE | Python IDLE |
| DB GUI | MySQL Workbench 8.0 |

---

## Project Structure

```
BloodBank/
│
├── main.py              # Entry point — Login screen
├── db_connect.py        # MySQL database connection
├── dashboard.py         # Main dashboard with navigation
├── donors.py            # Donor management module
├── inventory.py         # Blood inventory module
├── recipients.py        # Blood request module
├── donations.py         # Donation log module
└── reports.py           # Reports and search module
```

---

## Database Schema

The system uses a MySQL database named `BloodBankDB` with 5 tables:

```sql
Donors          — donor personal details and eligibility
BloodInventory  — blood units per group with expiry dates
Recipients      — blood requests from patients/hospitals
DonationLog     — complete history of all donations
Admin           — administrator login credentials
```

**Key Relationship:**
```
DonationLog.donor_id  →  Donors.donor_id  (FOREIGN KEY)
```

---

## Installation

### Prerequisites
- Python 3.x — [python.org](https://python.org)
- MySQL 8.0 — [mysql.com](https://dev.mysql.com/downloads/installer/)
- MySQL Workbench (comes with MySQL installer)

### Step 1 — Clone the repository
```bash
git clone https://github.com/yourusername/blood-bank-management-system.git
cd blood-bank-management-system
```

### Step 2 — Install required Python library
```bash
pip install mysql-connector-python
```

### Step 3 — Set up the database
Open MySQL Workbench and run the following SQL:

```sql
CREATE DATABASE BloodBankDB;
USE BloodBankDB;

CREATE TABLE Donors (
    donor_id     INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    age          INT NOT NULL,
    gender       ENUM('Male', 'Female', 'Other'),
    blood_group  ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    phone        VARCHAR(15) UNIQUE NOT NULL,
    email        VARCHAR(100),
    address      TEXT,
    last_donated DATE,
    is_eligible  BOOLEAN DEFAULT TRUE
);

CREATE TABLE BloodInventory (
    inventory_id  INT AUTO_INCREMENT PRIMARY KEY,
    blood_group   ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    units         INT DEFAULT 0,
    last_updated  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    expiry_date   DATE
);

CREATE TABLE Recipients (
    recipient_id   INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    age            INT,
    gender         ENUM('Male', 'Female', 'Other'),
    blood_group    ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    phone          VARCHAR(15),
    units_needed   INT NOT NULL,
    hospital_name  VARCHAR(150),
    request_date   DATE DEFAULT (CURRENT_DATE),
    status         ENUM('Pending','Fulfilled','Rejected') DEFAULT 'Pending'
);

CREATE TABLE DonationLog (
    log_id       INT AUTO_INCREMENT PRIMARY KEY,
    donor_id     INT,
    blood_group  VARCHAR(5),
    units        INT DEFAULT 1,
    donated_on   DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (donor_id) REFERENCES Donors(donor_id)
);

CREATE TABLE Admin (
    admin_id   INT AUTO_INCREMENT PRIMARY KEY,
    username   VARCHAR(50) UNIQUE NOT NULL,
    password   VARCHAR(100) NOT NULL
);

INSERT INTO Admin (username, password) VALUES ('admin', 'admin123');
```

### Step 4 — Configure database connection
Open `db_connect.py` and update your MySQL credentials:

```python
def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_mysql_password",  # ← change this
        database="BloodBankDB"
    )
    return conn
```

---

## How to Run

```bash
python main.py
```

**Default login credentials:**
```
Username: admin
Password: admin123
```

---

## Screenshots

| Screen | Description |
|---|---|
| Login Screen | Secure admin login with red-themed GUI |
| Dashboard | Main navigation with 5 module buttons |
| Manage Donors | Add/view/delete donors with eligibility check |
| Blood Inventory | Real-time stock with low stock highlighting |
| Blood Requests | Patient request management with status tracking |
| Donation Log | Complete donation history sorted by latest |
| Reports & Search | Search donors by blood group, expiry alerts |

> Add your screenshots to a `/screenshots` folder and link them here.

---

## Modules

| Module | File | Description |
|---|---|---|
| Login | `main.py` | Admin authentication via MySQL |
| Dashboard | `dashboard.py` | Navigation hub for all modules |
| Donors | `donors.py` | CRUD operations for donor records |
| Inventory | `inventory.py` | Blood stock tracking and alerts |
| Requests | `recipients.py` | Blood request registration |
| Donations | `donations.py` | Donation history log |
| Reports | `reports.py` | Search and expiry alerts |

---

## Author

**[Roshan Begum]**
- GitHub: [@roshanbegum](https://github.com/yourusername)
- Email: youremail@example.com

---

## License

This project is for educational purposes only as part of a DBMS mini project.

---

> ⭐ If you found this project helpful, consider giving it a star on GitHub!
