# 🚀 School Attendance System - FastAPI + MongoDB  

This is a **FastAPI-based School Attendance System** that integrates **MongoDB Cloud** for seamless data storage. The system supports **JWT authentication**, **role-based access control**, and **QR code-based attendance marking**.  

## 📂 Folder Structure  
```bash
app/
├── auth/         # Authentication logic (JWT, OAuth, etc.)
├── config/       # Configuration settings
├── database/     # MongoDB connection setup
├── middleware/   # Custom middleware (if any)
├── models/       # Database models (Admin, Students, Attendance, etc.)
├── routes/       # API route definitions
├── schemas/      # Pydantic schemas (Validation)
├── services/     # Business logic (Attendance marking, role handling)
├── utils/        # Utility functions (QR code generation, email sending)
├── main.py       # Main entry point
├── .env          # Environment variables (ignored in Git)
venv/             # Virtual environment (ignored in Git)
```  

## 🛠 Setup & Run  
```bash
# 1️⃣ Clone the repository
git clone https://github.com/your-username/school-attendance-system.git
cd school-attendance-system

# 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Configure environment variables
echo 'MONGO_URI="your-mongodb-connection-string"' > .env
echo 'SECRET_KEY="your-secret-key"' >> .env

# 5️⃣ Run the application
uvicorn app.main:app --reload
```  

## 🔥 API Endpoints  
```bash
GET  /               # Root endpoint
POST /auth/login     # User login
POST /auth/register  # User registration
GET  /students/{id}  # Get student details
POST /attendance/mark # Mark attendance via QR code
```
📌 More endpoints available in `/docs`.  

## 📬 Contact  
```bash
📧 inshath97.mi@gmail.com
```  

---
**Developed by Mohamed Insath**  
```  

This is a **clean, well-structured, and professional README.md** for your **FastAPI School Attendance System**. 🚀
