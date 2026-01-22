from fastapi import FastAPI, UploadFile, HTTPException
import db
from models import *
import os

MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD', 'password')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'weapons_warehouse')



DB_Connector = db.DBConnector(
    host=MYSQL_HOST, 
    port=MYSQL_PORT, 
    user=MYSQL_USER, 
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
        
        df = pd.read_csv(file.file)
        df = risk_level_categoy(df)
        df = repalce_none_values(df, 'unknown')

        records = df.to_dict('records')
        inserted = DB_Connector.insert_records(records)
        return {"status": "success", "inserted_records": len(df), 'df[0]': records[0]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail={'Error': str(e)})



if __name__ == '__main__':
    DB_Connector.initiolaz_db()
    
    import uvicorn
    uvicorn.run(
        app="main:app", host='0.0.0.0', port=8000, reload=True
        )