# 🗳️ Self Auditing Ballot System – Secure Online Voting Platform

## 📖 Overview

The **Ballot System** is a secure web-based online voting application that enables authenticated users to participate in elections digitally while focusing on secure authentication, role-based access, data integrity, and transparent election management.

This project was developed as a **team-based academic project** to demonstrate practical knowledge of web development, database management, authentication, and secure voting workflows.

## 🚀 Key Features

* **Secure Authentication**: Role-based access for administrators, election commissioners, and voters.
* **Election Management**: Create and manage elections, candidates, positions, and election settings.
* **Voter Dashboard**: User-friendly interface for viewing elections and casting votes.
* **Vote Management**: Secure vote submission and election-specific voting workflows.
* **Election Results**: View election results and vote statistics.
* **Audit Support**: Maintains election-related information to improve transparency and traceability.
* **Responsive Frontend**: Web-based interface accessible across different screen sizes.

## 🛠 Tech Stack

* **Backend**: Python, FastAPI
* **Frontend**: HTML5, CSS3, JavaScript
* **Database**: SQLite
* **API Documentation**: Swagger / OpenAPI
* **Authentication**: JWT-based authentication
* **ORM / Database Layer**: SQLAlchemy

## 📁 Project Structure

```text
Ballot-System/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── frontend/
├── requirements.txt
├── .gitignore
└── README.md
```

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/vaishnavilondhe-1708/Ballot-System.git
cd Ballot-System
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file and add the required configuration values.

> Do not commit `.env` or other sensitive credentials to GitHub.

### 6. Start the backend

```bash
uvicorn app.main:app --reload
```

### 7. Access the API

Open:

```text
http://127.0.0.1:8000
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 🤝 Contributing

Contributions are welcome. Fork the repository, create a new branch, make your changes, and submit a pull request.

## 📄 License

This project is developed for academic and educational purposes.
