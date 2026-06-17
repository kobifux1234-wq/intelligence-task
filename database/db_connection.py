import mysql.connector
class DB_connection:
    def get_connection(self):
        return mysql.connector.connect(
            host= "localhost",
            user="root",
            password= 1234,
            database= "intelligence_db"
            )
    def create_database(self):
        conn = mysql.connector.connect(
            host= "localhost",
            user="root",
            password= "1234"
            )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS intelligence_db")
        conn.commit()
        cursor.close()
        conn.close()
        
    def create_table(self):
        conn = mysql.connector.connect(
            host= "localhost",
            user="root",
            password= "1234",
            database = "intelligence_db"
            )
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
            difficulty INT NOT NULL,
            importance INT NOT NULL,
            status VARCHAR(50) DEFAULT "NEW",
            risk_level VARCHAR (100),
            assigned_agent_id INT DEFAULT NULL
        )""")
        conn.commit()
        cursor.close()
        conn.close()