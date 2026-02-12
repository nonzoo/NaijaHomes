# 🏠 NaijaHomes – Django Real Estate Platform

A modern real estate web application built with **Django 6**, allowing agents to list properties and customers to browse listings across Nigerian states.

---

## 🚀 Features

* 🔐 Custom Authentication (Agent & Customer roles)
* 🏢 Agent & Customer Dashboards
* 🏘 Property Listings
* 📸 Multiple Property Images
* 🌍 State-based Property Filtering (All Nigerian states supported)
* ⭐ Featured Properties
* 🌱 Smart Property Seeding Command
* 🖼 Separate image folders:

  * `seed_image/` → Main property images
  * `seed_image2/` → Extra property images
* 🎨 Tailwind CSS UI
* ⚙ Django Admin Panel

---

## 🛠 Tech Stack

* Python 3.12+
* Django 6.0
* SQLite (default database)
* Tailwind CSS
* HTML5
* JavaScript

---

## 📁 Project Structure

```
Real Estate/
│
├── Properties/
│   ├── management/
│   │   └── commands/
│   │       └── seed_properties.py
│   ├── models.py
│   ├── views.py
│   └── templates/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   └── forms.py
│
├── seed_image/      # Main property images
├── seed_image2/     # Extra property images
│
├── db.sqlite3
├── manage.py
└── README.md
```

---

## ⚙ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/naijahomes.git
cd naijahomes
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .env
```

Activate (Windows):

```bash
.env\Scripts\activate
```

Activate (Mac/Linux):

```bash
source .env/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have one yet:

```bash
pip freeze > requirements.txt
```

---

### 4️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

---

### 6️⃣ Run Development Server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

Admin Panel:

```
http://127.0.0.1:8000/admin
```

---

## 🌱 Seeding Demo Properties

To generate demo properties:

```bash
python manage.py seed_properties
```

This will:

* Create **20 properties**
* Distribute them across Agent users
* Assign properties to **10 Nigerian states**
* Use:

  * `seed_image/` → main property images
  * `seed_image2/` → extra property images

---

## 👤 User Roles

### 🧑‍💼 Agent

* Can create and manage properties
* Has `AgentProfile`
* Redirected to Agent Dashboard after login

### 👤 Customer

* Can browse properties
* Has `CustomerProfile`
* Redirected to Customer Dashboard after login

---

## 📌 Nigerian States Supported

Includes all Nigerian states such as:

* Lagos
* FCT Abuja
* Rivers
* Ogun
* Oyo
* Kaduna
* Enugu
* Anambra
* Delta
* Akwa Ibom
* and more...

---

## 🏗 Property Model Overview

```python
class Properties(models.Model):
    title
    price
    address
    state
    agent
    bedrooms
    bathrooms
    living_rooms
    Sqm
    property_type
    description
    image
    is_featured
```

---

## 🔐 Authentication System

* Single-page Sign In / Sign Up
* Group-based user roles
* Automatic dashboard redirection
* Django authentication backend

---

## 📂 Media Handling

* Main images stored in: `property_images/`
* Extra images stored in: `property_images/extra/`
* Uploaded via Django `MEDIA_ROOT`

---

## 🚧 Future Improvements

* 🔎 Advanced property filtering
* 💳 Payment integration
* ☁ Cloud storage for images
* 📧 Email verification
* 🌐 REST API version
* 📱 Mobile responsive enhancements

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Built with ❤️ using Django.
