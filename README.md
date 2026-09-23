# 🗳️  Self Auditing Ballot System – Secure Online Voting Platform

## 📖 Overview
The **Ballot System** is a secure web-based online voting application that enables authenticated users to cast votes digitally while ensuring **transparency, data integrity, and real-time result processing**.

This project was developed as a **team-based academic project** to demonstrate practical knowledge of **web development, database management, and secure authentication mechanisms**.
---

## 🚀 Key Features

*   **Secure Authentication**: Role-based access control for Admins, Election Commissioners, and Voters.
*   **Election Management**: Create and manage multiple elections with customizable parameters (start/end time, candidates, positions).
*   **Voter Dashboard**: Easy-to-use interface for casting votes securely.
*   **Real-time Results**: Live tracking of vote counts and election statistics.
*   **Audit Trails**: Comprehensive logs of all election activities to ensure transparency.
*   **Responsive Design**: Accessible on desktop and mobile devices.

## 🛠 Tech Stack

*   **Backend**: Python (Django Framework)
*   **Frontend**: HTML5, CSS3, JavaScript
*   **Database**: PostgreSQL / SQLite (for development)
*   **API**: Django REST Framework
*   **Authentication**: JWT / Session-based authentication

## 📦 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/alokaher31/Ballot-System.git
    cd Ballot-System
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```

6.  **Access the application:**
    Open your browser and navigate to `http://127.0.0.1:8000/`.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## 📄 License

This project is licensed under the MIT License.
