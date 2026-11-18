# Product Management System

A full-stack web application built using **React.js, FastAPI, and PostgreSQL** to manage products through a user-friendly interface and RESTful APIs.

## Project Overview

The Product Management System provides a centralized platform to manage product information. It combines a React frontend with a Python FastAPI backend and PostgreSQL database.

## Technologies Used

| Frontend | Backend | Database & Tools |
|---|---|---|
| React.js | Python | PostgreSQL |
| JavaScript | FastAPI | SQLAlchemy |
| HTML5 | Pydantic | Docker |
| CSS3 | REST APIs | Git & GitHub |
| Fetch API | Uvicorn | |

## Features

- Product management through a web interface
- Create, read, update, and delete products
- Product search and filtering
- Pagination
- REST API integration
- Backend data validation
- PostgreSQL database integration
- User authentication and security components

## Project Architecture

```text
product-management-system/
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── Dockerfile
│   └── README.md
│
├── backend/
│   ├── config/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── utils/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
└── README.md
```

## Application Workflow

1. Users interact with the React frontend.
2. The frontend sends HTTP requests using the Fetch API.
3. FastAPI receives and processes the API requests.
4. SQLAlchemy handles database operations.
5. PostgreSQL stores product and application data.
6. The backend returns responses to the frontend.

## Getting Started

### Prerequisites

- Python
- Node.js and npm
- PostgreSQL
- Git
- Docker (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/Strategy-200/product-management-system.git
cd product-management-system
```

### 2. Start the Backend

```bash
cd backend

python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your PostgreSQL database and the environment variables required by the backend.

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Backend API:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

### 3. Start the Frontend

Open another terminal:

```bash
cd frontend

npm install
npm run dev
```

Open the frontend URL displayed in your terminal.

## Docker Support

Both frontend and backend contain Dockerfiles.

Build and run each service using the Docker configuration provided in its respective folder. Configure the database connection and frontend API URL appropriately for your environment.

## Future Enhancements

- Advanced product analytics
- Role-based access control
- Improved dashboard and reporting
- Automated testing
- Cloud deployment

## Author

**Srinivas T R**

GitHub: [Strategy-200](https://github.com/Strategy-200)

## Project Repository

[Product Management System – GitHub](https://github.com/Strategy-200/product-management-system)

---

⭐ If you find this project useful, consider giving it a star!
