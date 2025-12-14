## TDD Kata: Sweet Shop Management System

### 🍬 Sweet Shop Management System

A full-stack Sweet Shop Management System built using Django (Backend) and React (Frontend).
The application supports role-based access where admins manage sweets and users can browse, search, and purchase sweets through a modern, real-world UI.

This project was developed with a focus on security, usability, clean architecture, and professional UI/UX.

## ✨ Features

### 👨‍💼 Admin Features

* Secure login using JWT authentication

* Add sweets with:

  Name

  Category

  Price

  Quantity

  Image upload (Optional)

* Edit sweets (with smooth auto-scroll to edit form)

* Delete sweets

* Admin-only protected APIs

* Separate Admin Dashboard


### 👤 User Features

* User registration & login

* Browse sweets in a real shop-style layout

* View sweet details (image, category, price, quantity)

* Search sweets by name, category, and price

* Purchase sweets with stock validation

* Clean and responsive UI with hero banner

### 🛠️ Tech Stack

#### Backend
* Python
* Django
* Django REST Framework
* JWT Authentication (SimpleJWT)
* SQLite (development)

#### Frontend

* React.js
* Axios
* Custom CSS (no UI frameworks)
* Responsive design

### 📂 Project Structure

```
Sweet-Shop/
│
├── backend/    # All the backend structure/code are here
│   ├── shop/   # Django App
│   ├── backend/   # Django Project
│   ├── manage.py
│   
│
├── frontend/   # All the frontend structure/codes are here
│   ├── src/  # Source folder which contain all files
│   ├── public/
│   ├── package.json
│   └── package-lock.json
│
└── README.md
└── requirements.txt
```

### 🚀 Installation & Setup (Beginner Friendly)  

**You can also watch the installation and setup video. The link is provided below.**
  Link: 


* Clone the Github Repo:

  ```
  git clone https://github.com/rishee10/Sweet-Shop-Management-System.git
  ```
* Move Inside the Sweet-Shop-Management-System folder

  ```
  cd Sweet-Shop-Management-System
  ```
  
* Open the Project in Any Code editer (Ex-> Vs code)

  With cmd you can open directly also

  ```
  code .
  ```

#### Setup the backend first

**Open a New Terminal for backend setup**

* Create Virtual Enviroment

  ```
  python -m venv venv
  ```

* Activate the virtual Enviroment

  ```
  venv\Scripts\activate
  ```

* Download the requirements

  ```
  pip install -r requirements.txt
  ```

* Move Inside the backend folder now

  ```
  cd backend
  ```

* Apply Migrations Command

  ```
  python manage.py makemigrations shop
  ```

* Apply Migrate Command

  ```
  python manage.py migrate
  ```

#### (IMP)🔐 Admin Creation

**Admins are created securely using Django’s shell**

* Open the shell
  ```
  python manage.py shell
  ```

* Run this (Copy paste it)

```
  User.objects.create_user(
     username="admin_user_name",  # Here the admin user name come
     password="admin_password",   # Here the admin password come
     is_staff=True 
  )
```

* Run the backend Server

  ```
  python manage.py runserver
  ```

#### Setup for frontend

**Open new terminal for frontend**

* Move Inside the Frontend Folder

  ```
  cd frontend
  ```

* Install the nmp

  ```
  npm install
  ```

* Run the frontend  server

  ```
  npm start
  ```

* Frontend runs at:

  ```
  http://localhost:3000/
  ```

#### Running Test cases

**Go backed to the backend terminal stop the backend server**

run  this command

```
python manage.py test
```



### 🤖 My AI Usage

**🔧 AI Tools Used**

* ChatGPT (OpenAI)

**🛠️ How I Used AI**

**I used ChatGPT as a development assistant and learning aid, not as a replacement for my own coding.**

Specifically, I used it to:

* Brainstorm REST API endpoint design
* Understand JWT authentication flows
* Review Django permission strategies (admin vs user)
* Debug React state management and form handling
* Improve UI/UX decisions (dashboard layout, hero banner, admin usability)
* Refine README documentation clarity

**All final implementations were written, tested, and integrated by me.**


### 🧠 Reflection: Impact of AI on My Workflow

**AI significantly improved my workflow by:**
* Reducing time spent on repetitive research
* Helping me identify edge cases earlier
* Improving code readability and structure
* Enhancing UI/UX quality
* Accelerating learning of unfamiliar concepts
  

**I treated AI like a senior developer mentor — validating ideas, learning faster, and making better technical decisions — while still fully understanding and owning the final code.**
  



  

