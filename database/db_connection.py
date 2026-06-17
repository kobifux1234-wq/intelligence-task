import mysql.connector
class DB_connection:
    def get_connection()-> mysql.connector.connect:
        return mysql.connector.connect(
            host= "localhost",
            user="root",
            password= "1234",
            database= "intelligence_db"
            )
    def create_database():
        conn= None
        cursor = None
        try:
            conn = mysql.connector.connect(
                host= "localhost",
                user="root",
                password= "1234"
                )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS intelligence_db")
            conn.commit()
        except:return ("Problem in connection and creating database")
        finally:
            
            cursor.close()
            conn.close()
        
    def create_table():
        conn= None
        cursor = None
        try:
            conn =DB_connection.get_connection()
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS agents(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                specialty VARCHAR(100) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                completed_missions INT DEFAULT 0,
                failed_missions INT DEFAULT 0,
                agent_rank ENUM("Commander","Senior","Junior")
                )""")
            
            cursor.execute("""CREATE TABLE IF NOT EXISTS missions(
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                location VARCHAR(100) NOT NULL,
                difficulty INT CHECK(difficulty BETWEEN 1 AND 10),
                importance INT CHECK(importance BETWEEN 1 AND 10),
                status VARCHAR(50) DEFAULT "NEW",
                risk_level VARCHAR (100),
                assigned_agent_id INT DEFAULT NULL
            )""")
            conn.commit()
            
        except: return ("Problem in connection and creating tables")
        finally: 
            cursor.close()
            conn.close()