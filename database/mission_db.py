import mysql.connector
class DB_connection:
    def get_connection(self):
        return mysql.connector.connect(
            host= "localhost",
            user="root",
            password= 1234,
            database= "intelligence-mysql"
            )
    def create_database(self):
        conn = mysql.connector.connect(
            host= "localhost",
            user="root",
            password= "1234"
            )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS intelligence-mysql")
        conn.commit()
        cursor.close()
        conn.close()
        
    def create_table(self):
        conn = mysql.connector.connect(
            host= "localhost",
            user="root",
            password= "1234",
            database = "intelligence-mysql"
            )
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS agents(
            id INT AUTO_INCREMENT PRIMARY KEY
            name VARCHAR(50) NOT NULL,
            specialty VARCHAR(100) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            completed_missions INT DEFAULT 0,
            failed_missions INT DEFAULT 0,
            agent_rank VARCHAR(50) ENUM("Commander","Senior","Junior")
            )""")
        conn.commit()
        cursor.close()
        conn.close()