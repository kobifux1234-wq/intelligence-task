import mysql.connector
from database.db_connection import DB_connection as db_c

class AgentDB:
    @staticmethod
    def agent_by_id(id: int):
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM agents WHERE id = %s", (id,))
            return cursor.fetchone()
        except: raise("Error: connection problem to get agent")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def create_agent(data:dict):
        if data.get("agent_rank") not in ["Commander", "Junior","Senior"]:
            raise Exception("Incorrect agent rank")
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor(dictionary=True)
            key = ", ".join(data.keys())
            placeholders= ", ".join(["%s"]*len(data))
            sql =f"INSERT INTO agents({key}) VALUES ({placeholders})"
            cursor.execute(sql,list(data.values()))
            conn.commit()
            row = cursor.lastrowid
            return AgentDB.agent_by_id(row)
        
        except: raise Exception("have problem with create agent")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def get_all_agents():
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM agents")
            rows=cursor.fetchall()
            return rows
        except mysql.connector.Error as e: raise Exception("error get all agents") from e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
    
    @staticmethod
    def update_agent(id,data):
        agent=AgentDB.agent_by_id(id)
        if agent is None:
            raise ValueError
        if data.get("agent_rank") not in ["Commander", "Junior","Senior"]:
            raise Exception("Incorrect agent rank")
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            placeholders= ", ".join([f"{key} = %s" for key in data.keys()])
            value= list(data.values())+[id]
            sql= f"UPDATE agents SET {placeholders} WHERE id = %s"
            cursor.execute(sql,value)
            conn.commit()
            return cursor.rowcount>0
        except mysql.connector.Error as e: raise Exception("Error happened in update agent") from e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod     
    def deactivate_agent(id):
        agent=AgentDB.agent_by_id(id)
        if agent is None:
            raise ValueError
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE agents SET is_active = FALSE WHERE id =%s",(id,))
            conn.commit()
            return cursor.rowcount>0
        except mysql.connector.Error as e: raise Exception("Error happened in update agent deactivate") from e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def increment_completed(id):
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE agents SET completed_missions = completed_missions +  1 WHERE id =%s",(id,))
            conn.commit()
            return cursor.rowcount>0
        except mysql.connector.Error as e: raise Exception("Error happened in update agent completed missions") from e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    @staticmethod   
    def increment_failed(id):
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE agents SET failed_missions = failed_missions +  1 WHERE id =%s",(id,))
            conn.commit()
            return cursor.rowcount>0
        except mysql.connector.Error as e: raise Exception("Error happened in update agent failed missions") from e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def get_agent_performance(id):
        agent=AgentDB.agent_by_id(id)
        if agent is None:
            raise ValueError
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT failed_missions FROM agents WHERE id = %s",(id,))
            failed= cursor.fetchone()
            cursor.execute("SELECT completed_missions FROM agents WHERE id = %s",(id,))
            success= cursor.fetchone()
            failed = failed[0] if failed is not None else 0
            success = success[0] if success is not None else 0
            if success+failed == 0: rate=0
            else: rate= success/(failed+success)
            return {"completed":success, "failed": failed, "total": success+failed, "success_rate":rate}
        except mysql.connector.Error as e: raise Exception("Error happened in gets agent performance") from e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
    @staticmethod
    def count_active_agents():
        with db_c.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM agents WHERE is_active = TRUE")
                row= cursor.fetchone()
        return row[0] if row is not None else row 