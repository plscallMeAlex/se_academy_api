# Backend

please clone this project first before doing anything. This project make for experience in web development.

## To run an api

After cloning this project, follow these steps:

1. Create your virtual environment:

   ```bash
       python -m venv venv
   ```

2. Activate the virtual environment:

   - For Windows:

     ```bash
         venv\Scripts\activate
     ```

   - For Linux/macOS:

     ```bash
         source venv/bin/activate
     ```

3. Install all required dependencies:

   ```bash
       pip install -r requirements.txt
   ```

4. Run the API:

   - With FastAPI:

     ```bash
         fastapi run main.py
     ```

   - With Uvicorn server:

     ```bash
         uvicorn main:app --reload
     ```

## Alembic migration to creating database

If you want to creating the table using command:

```bash
    alembic revision --autogenerate -m "{message}"
    alembic upgrade head
```
