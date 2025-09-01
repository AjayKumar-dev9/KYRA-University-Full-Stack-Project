# KYRA-University-Full-Stack-Project

# Kyra University

Kyra University is a **full-stack web application** that helps manage student and faculty operations.  
It is built with **Django (backend)** and **HTML, CSS, JavaScript (frontend)**, and uses **MySQL** as the database.  

---

## Key Features
- **User Authentication**: Registration and login  
- **Email & OTP Verification**: Secure password reset system  
- **Student Management**: Add and manage student details  
- **Faculty Management**: Add and manage faculty details  
- **Database Integration**: MySQL for storing all data  
- **Responsive Frontend**: Built with HTML, CSS, JavaScript, and Bootstrap  

---

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript, Bootstrap  
- **Backend:** Django, Django REST Framework  
- **Database:** MySQL  
- **Authentication:** Email + OTP verification  

---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/KYRA-University-Full-Stack-Project.git
   cd KYRA-University-Full-Stack-Project

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # Mac/Linux


3. **Install dependencies**
   ```bash
   pip install -r requirements.txt


4. **Configure the database**
 - Update settings.py with your MySQL username, password, and database name.

5. **Run migrations**

 - python manage.py migrate


6. **Start the development server**

 - python manage.py runserver


7. **Open the application**
 - Go to http://127.0.0.1:8000
   in your browser.

8. **Environment Variables**

- 1.Create a .env file in the project root
- 2.Add the following values:

 - SECRET_KEY=your_secret_key
 - EMAIL_HOST=smtp.yourmail.com
 - EMAIL_PORT=587
 - EMAIL_HOST_USER=your_email@example.com
 - EMAIL_HOST_PASSWORD=your_password
 - DATABASE_NAME=kyra_db
 - DATABASE_USER=root
 - DATABASE_PASSWORD=yourpassword

9. **Future Plans**

 - React.js Frontend for better UI

 - JWT Authentication for secure API access

 - Deployment on AWS/Docker for scalability

10. **Author**

Developed by **Ajay Kumar**
