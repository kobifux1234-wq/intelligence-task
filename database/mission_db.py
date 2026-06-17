from database.db_connection import DB_connection as db_c
class MissionDB:
    @staticmethod
    def mission_by_id(id: int):
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM missions WHERE id = %s", (id,))
            return cursor.fetchone()
        except: raise Exception("Error: connection problem to get ")
        finally:    
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    @staticmethod
    def create_mission(data:dict):
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            key = ", ".join(data.keys())
            placeholders= ", ".join(["%s"]*len(data))
            sql =f"INSERT INTO missions({key}) VALUES ({placeholders})"
            cursor.execute(sql,list(data.values()))
            conn.commit()
            row = cursor.lastrowid
            return MissionDB.mission_by_id(row)
        
        except: raise Exception("have problem with create mission")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return row
    
    def get_all_missions():
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM missions")
            rows=cursor.fetchall()
        except: raise Exception("error get all missions")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return rows

    @staticmethod
    def assign_mission(m_id,a_id):
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE missions SET assigned_agent_id = %s WHERE id= %s",(a_id,m_id))
            conn.commit()
            return cursor.rowcount>0
        except: raise Exception("Error happened in update assign mission")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def update_mission_status(id, status):
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE missions SET status = %s WHERE id = %s", (status,id))
            conn.commit()
            return cursor.rowcount >0
        except: raise Exception("Error happened in update mission status")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            
    @staticmethod
    def get_open_missions_by_agent(id:int):
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM missions WHERE assigned_agent_id= %s",(id,))
            return cursor.fetchall()
        except:raise Exception("Error happened in open missions by agent")
        finally: 
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def count_all_missions():
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM missions")
            return cursor.fetchone()[0]
        except:raise Exception("Error happened in count all missions")
        finally: 
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def count_by_status(status:str):
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM missions WHERE status = %s",(status,))
            return cursor.fetchone()[0]
        except:raise Exception("Error happened in count by status")
        finally: 
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def count_open_missions():
        return MissionDB.count_by_status("NEW")
    
    @staticmethod
    def count_critical_missions():
        
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM missions WHERE risk_level = %s",("Critical",))
            return cursor.fetchone()[0]
        except:raise Exception("Error happened in count by status")
        finally: 
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    @staticmethod
    def get_top_agent():
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT assigned_agent_id, COUNT(*) as mission_count FROM missions WHERE status = 'Completed'\
                        GROUP BY assigned_agent_id ORDER BY mission_count DESC LIMIT 1")
            
            return cursor.fetchone()
        except:raise Exception("Error happened in get_top_agent")
        finally: 
            if cursor:
                cursor.close()
            if conn:
                conn.close()