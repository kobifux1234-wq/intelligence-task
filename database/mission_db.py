from database.db_connection import DB_connection as db_c
from database.agent_db import AgentDB as a_db
import mysql.connector
class MissionDB:
    @staticmethod
    def get_mission_by_id(id: int):
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM missions WHERE id = %s", (id,))
            return cursor.fetchone()
        except mysql.connector.Error as e: raise Exception("Error: connection problem to get ") from e
        finally:    
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    @staticmethod
    def create_mission(data:dict):
        if not 0<data.get("difficulty")<11 or not 0<data.get("importance")<11:
            raise Exception("Incorrect difficulty or importance data")
        risk_level_num = data.get("difficulty")*2 + data.get("importance")
        data["risk_level"] = "LOW" if 0<=risk_level_num<=9 else "MEDIUM" if 10<=risk_level_num<=17 else "HIGH" if 18<=risk_level_num<=24 else "CRITICAL"
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor(dictionary=True)
            key = ", ".join(data.keys())
            placeholders= ", ".join(["%s"]*len(data))
            sql =f"INSERT INTO missions({key}) VALUES ({placeholders})"
            cursor.execute(sql,list(data.values()))
            conn.commit()
            row = cursor.lastrowid
            return MissionDB.get_mission_by_id(row)
        
        except mysql.connector.Error as e: raise Exception("have problem with create mission") from e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return row
    
    @staticmethod
    def get_all_missions():
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM missions")
            rows=cursor.fetchall()
        except mysql.connector.Error as e: raise Exception("error get all missions") from e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return rows

    @staticmethod
    def assign_mission(m_id, a_id):
        conn = None
        cursor = None
        try:
            conn = db_c.get_connection()
            cursor = conn.cursor() 
            cursor.execute("SELECT risk_level, status FROM missions WHERE id = %s", (m_id,))
            mission = cursor.fetchone()
            if not mission:
                return False 
            risk, status = mission
            
            if status != 'NEW':
                return False  
            cursor.execute("SELECT agent_rank, is_active FROM agents WHERE id = %s", (a_id,))
            agent = cursor.fetchone()
            if not agent:
                return False
            rank, is_active = agent
            
            if not is_active:
                return False
            if risk == 'CRITICAL' and rank != 'Commander':
                return False
            cursor.execute("SELECT COUNT(*) FROM missions WHERE assigned_agent_id = %s AND status IN ('ASSIGNED', 'IN_PROGRESS')",(a_id,))
            active_missions = cursor.fetchone()[0]
            
            if active_missions >= 3:
                return False
            cursor.execute("UPDATE missions SET assigned_agent_id = %s, status = 'ASSIGNED' WHERE id = %s AND status = 'NEW'",(a_id, m_id))
            conn.commit()
            
            return cursor.rowcount > 0
        
        except mysql.connector.Error as e: raise Exception("Error in assign mission") from e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    
    @staticmethod
    def update_mission_status(id, status):
        valid_statuses = ["IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED"]
        if status not in valid_statuses:
            raise Exception("Incorrect status value")
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT status, assigned_agent_id FROM missions WHERE id = %s", (id,))
            mission = cursor.fetchone()
            if not mission:
                return False
            current_status, a_id = mission
            
            if status == "IN_PROGRESS" and current_status != "ASSIGNED":
                raise ValueError("Only a mission with status ASSIGNED can be started")
            if status in ("COMPLETED", "FAILED") and current_status != "IN_PROGRESS":
                raise ValueError("Only a mission with status IN_PROGRESS can be finished")
            if status == "CANCELLED" and current_status not in ("NEW", "ASSIGNED"):
                raise ValueError("Only a mission with status NEW or ASSIGNED can be canceled")
 
            cursor.execute("UPDATE missions SET status = %s WHERE id = %s", (status,id))
            conn.commit()
            updated = cursor.rowcount >0
 
            if updated and status == "COMPLETED" and a_id is not None:
                a_db.increment_completed(a_id)
            if updated and status == "FAILED" and a_id is not None:
                a_db.increment_failed(a_id)
 
            return updated
        except mysql.connector.Error as e:
            raise Exception("Error happened in update mission status") from e
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
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM missions WHERE assigned_agent_id= %s AND status IN ('ASSIGNED','IN_PROGRESS')",(id,))
            return cursor.fetchall()
        except mysql.connector.Error as e:raise Exception("Error happened in open missions by agent") from e
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
        except mysql.connector.Error as e:raise Exception("Error happened in count all missions") from e
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
        except mysql.connector.Error as e:raise Exception("Error happened in count by status") from e
        finally: 
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def count_open_missions():
        return MissionDB.count_by_status("NEW")+MissionDB.count_by_status("ASSIGNED")+MissionDB.count_by_status("IN_PROGRESS")
    
    @staticmethod
    def count_critical_missions():
        
        conn= None
        cursor = None
        try:
            conn=db_c.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM missions WHERE risk_level = %s",("CRITICAL",))
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
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT assigned_agent_id, COUNT(*) as mission_count FROM missions WHERE status = 'COMPLETED'\
                        GROUP BY assigned_agent_id ORDER BY mission_count DESC LIMIT 1")
            top=cursor.fetchone()
            if top:
                return a_db.agent_by_id(top["assigned_agent_id"])
            else:
                return("agent not found")
        except mysql.connector.Error as e:raise Exception("Error happened in get_top_agent") from e
        finally: 
            if cursor:
                cursor.close()
            if conn:
                conn.close()