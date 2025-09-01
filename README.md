# KYRA-University-Full-Stack-Project

🎓 Kyra University

Kyra University is a full-stack web application that helps manage student and faculty operations.
It is built with Django (backend) and HTML, CSS, JavaScript (frontend), and uses MySQL as the database.


✨ Key Features

🔐 User registration & login

✉️ Email & OTP verification for password reset

👩‍🎓 Student and faculty management

🗄 MySQL database integration

🌐 Responsive frontend with HTML, CSS, JavaScript, Bootstrap


🛠 Tech Stack

Frontend: HTML, CSS, JavaScript, Bootstrap

Backend: Django, Django REST Framework

Database: MySQL

Authentication: Email + OTP verification



⚙️ Setup Instructions

Clone the repository

git clone https://github.com/your-username/KYRA-University-Full-Stack-Project.git
cd KYRA-University-Full-Stack-Project


Create & activate virtual environment

python -m venv venv
venv\Scripts\activate   # Windows  
source venv/bin/activate  # Mac/Linux


Install dependencies

pip install -r requirements.txt


Configure database
Update settings.py with your MySQL username, password, and database name.

Run migrations

python manage.py migrate


Start the server

python manage.py runserver


Now open 👉 http://127.0.0.1:8000



📬 Environment Variables

Create a .env file with your own values:

SECRET_KEY=your_secret_key
EMAIL_HOST=smtp.yourmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_password
DATABASE_NAME=kyra_db
DATABASE_USER=root
DATABASE_PASSWORD=yourpassword



🚀 Future Plans

React.js frontend

JWT authentication

Deployment on AWS / Docker



👨‍💻 Author

Developed by Ajay Kumar
