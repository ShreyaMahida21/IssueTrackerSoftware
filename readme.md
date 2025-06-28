# 🐍 Issue Tracker — Python Flask + MongoDB

This is an **Issue Tracking System** built with **Python**, **Flask**, and **MongoDB**.  
It lets **Admins**, **Users**, and **Super Admins** register, login, create, assign, track, and resolve issues with ease.

---

## 🚀 **Features**

- ✅ User registration and login with roles: `Admin`, `User`, `Super Admin`
- ✅ Create, assign, track, and resolve issues
- ✅ Priority, type, status management
- ✅ Simple file upload & attachment (coming soon)
- ✅ Modern, responsive UI with Bootstrap

---

## ⚙️ **How to Run**

### 1️⃣ Clone this repository

```bash
git clone https://github.com/yourusername/issue-tracker.git
cd issue-tracker
2️⃣ Create a virtual environment
Windows:
python -m venv venv
venv\Scripts\activate
3️⃣ Install dependencies
bash

pip install -r requirements.txt
4️⃣ Set up your environment variables
Create a .env file in the root of your project with:

env

MONGO_URI=mongodb://localhost:27017/issuetrackerdb
SECRET_KEY=your_secret_key_here
✅ Replace your_secret_key_here with any random string for session security.
✅ Replace MONGO_URI if you’re using MongoDB Atlas instead of local.

5️⃣ Set up your MongoDB database
Start MongoDB (if local).

Use MongoDB Compass or DBeaver to connect.

Create a new database called: issuetrackerdb

Create these collections:

users

issues
6️⃣ Run the Flask app
python run.py