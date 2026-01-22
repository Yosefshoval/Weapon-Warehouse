from fastapi import FastAPI, UploadFile, HTTPException
import db
import os

# MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD', 'password')
# MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
# MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'weapons-warehouse')






DB_Connector = db.DBConnector(
    # host=MYSQL_HOST, 
    # port=MYSQL_PORT, 
    # user=MYSQL_USER, 
    password=MYSQL_ROOT_PASSWORD, 
    database=MYSQL_DATABASE
    )



app = FastAPI()

@app.get('/health')
def health_check():
    return {"message": "server is healthy!"}


@app.post('/upload')
def upload_csv(file: UploadFile):
    try:
        if file.filename.split('.')[-1] != 'csv':
            raise HTTPException(status_code=422, detail='Invalid file type')
        (file.file)
        inserted = ...
        return {"status": "success", "inserted_records": inserted}
    except:
        ...
    