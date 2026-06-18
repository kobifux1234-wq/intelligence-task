from fastapi import APIRouter
from database.agent_db import AgentDB as ag_db
from database.mission_db import MissionDB as mi_db
router=APIRouter()

@router.get("/summary")
def total_summary():
    dict_summary={
"active_agents_count": 0,
"total_missions": 0,
"open_missions": 0,
"completed_missions": 0,
"failed_missions": 0,
"critical_missions": 0
}
    dict_summary["active_agents_count"]= ag_db.count_active_agents()
    dict_summary["total_missions"]= mi_db.count_all_missions()
    dict_summary["open_missions"]= mi_db.count_open_missions()
    dict_summary["completed_missions"]= mi_db.count_by_status("COMPLETE")
    dict_summary["failed_missions"]= mi_db.count_by_status("FAILED")
    dict_summary["critical_missions"]= mi_db.count_critical_missions()
    return dict_summary


    
@router.get("/missions-by-status")
def get_by_status():
    dict_status= dict()
    dict_status["new"] = mi_db.count_by_status("NEW") or 0
    dict_status["assigned"] = mi_db.count_by_status("ASSIGNED") or 0
    dict_status["in_progress"] = mi_db.count_by_status("IN_PROGRESS") or 0
    dict_status["completed"] = mi_db.count_by_status("COMPLETED") or 0
    dict_status["failed"] = mi_db.count_by_status("FAILED") or 0
    dict_status["canceled"] = mi_db.count_by_status("CANCELED") or 0
    return dict_status
    
    
@router.get("/top-agent")
def get_top_agent():
    return mi_db.get_top_agent()