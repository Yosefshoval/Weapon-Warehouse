import mysql.connector


class DBConnector:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                # password=self.password,
                # database=self.database
            )
        return self.connection
    


    def initiolaz_db(self):
        cnx = self.get_connection()

        create_table_query = """CREATE TABLE IF NOT EXISTS weapons (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    weapon_id VARCHAR(255),
                                    weapon_name VARCHAR(255),
                                    weapon_type VARCHAR(255),
                                    range_km INT,
                                    weight_kg FLOAT,
                                    manufacturer VARCHAR(255),
                                    origin_country VARCHAR(255),
                                    storage_location VARCHAR(255),
                                    year_estimated INT,
                                    level_risk VARCHAR(255)
                                );"""
        
        with cnx.cursor(dictionary=True) as cursor:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.database};')
            cursor.execute(f'USE {self.database};')
            cursor.execute(create_table_query)
            cnx.commit()
        


    def insert_records(self, records: list[dict]):
        cnx = self.get_connection()
        insert_query = """INSERT INTO weapons (
                        weapon_id, weapon_name, weapon_type, 
                        range_km, weight_kg, manufacturer, 
                        origin_country, storage_location, 
                        year_estimated, level_risk) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        
        values = [tuple(record.values()) for record in records]

        with cnx.cursor(dictionary=True) as cursor:
            print('records[0]', records[0]) #!

            cursor.execute(f'USE {self.database};')
            cursor.execute('SELECT COUNT(*) FROM weapons;')
            
            length_before = cursor.fetchone()['COUNT(*)']
            print('length_before', length_before) #!

            if len(records) > 1:
                r = cursor.executemany(insert_query, values)
                print('many inserted') #!
            
            elif len(records) == 1:
                cursor.execute(insert_query, values)
                print('one inserted') #!
            
            else:
                raise ValueError('No records to insert')
            
            cursor.execute('SELECT COUNT(*) FROM weapons;')
            length_after = cursor.fetchone()['COUNT(*)']
            
            cnx.commit()
            inserted = length_after - length_before
            
            result = {"status": "success", "inserted_records": inserted, "all records": length_after}
            print(result) #!
            return result
        



