import psycopg2
import pandas as pd
import psycopg2.extras as extras
import pandas as pd
import time

class data_loader():
    
    def __init__(self):
        
        self.create_connection()
        self.read_csv_data()
        self.load_data()
        
        

    def create_connection(self):
        host = "localhost"
        db_name = "test"
        user = "postgres"
        password = "1234"
        port= "5432"

        try:
            self.connection_test_db = psycopg2.connect(host=host,port=port,database=db_name,user=user,password=password)
            self.test_db_cursor = self.connection_test_db.cursor()
            print("connection successful")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)


    def read_csv_data(self):
        self.df = pd.read_csv('fake_data.csv')


    def load_data(self):
        try:
            t1 = time.perf_counter()
            tuples = [tuple(x) for x in self.df.to_numpy()]
            cols = ','.join(list(self.df.columns))
            query = "INSERT INTO %s(%s) VALUES %%s" % ('public.test_table', cols)
            extras.execute_values(self.test_db_cursor , query, tuples)
            self.connection_test_db.commit()
            print("data inserted successfully!")
            t2 = time.perf_counter()
            print(t2-t1)
        except (Exception, psycopg2.Error) as error:
                print("Error while deleting data:", error)
        pass

    def close_connection(self):
        self.connection_test_db.close()
        pass

instance = data_loader()
