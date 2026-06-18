from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from typing import Literal
from database.mission_db import MissionDB as miss_db
from database.agent_db import AgentDB as ag_db
import logging

router=APIRouter()
logger = logging.getLogger(__name__)

class CreateMission(BaseModel):
    title:str
    description:str
    location:str
    difficulty:Literal[1,2,3,4,5,6,7,8,9,10]
    importance:Literal[1,2,3,4,5,6,7,8,9,10]
    

@router.get("")
def get_all_missions():
    logger.info("GET /missions called")
    try:
        mission = miss_db.get_all_missions()
        logger.info("GET all missions successfully")
        return mission
    except Exception as ecs:
        logger.warning(f"message: {ecs}", exc_info=True)
        raise HTTPException(status_code=500,detail=f"{ecs}")

@router.get("/{id}")
def get_get_mission_by_id(id:int):
    
    logger.info(f"GET /mission by id:{id} called")
    try:
        mission= miss_db.get_mission_by_id(id)
        if mission:
            logger.info(f"GET /mission by id:{id} success")
            return mission
        else:
            logger.error(f"GET /mission by id:{id} failed")
            raise HTTPException(status_code= 404,detail="Id not found")
    except Exception as ecs:
        logger.warning(f"message: {ecs}", exc_info=True)
        raise HTTPException(status_code=500,detail=f"{ecs}")
    
@router.post("")
def create_mission(new_mission:CreateMission):
    try:
        logger.info("POST /mission called")
        mission=miss_db.create_mission(new_mission.model_dump())
        if mission:
            logger.info("POST /mission success")
            return {"message": "mission created!"}
        else:
            logger.error("POST /mission failed")
            return{"message": "Created Failed, check the rules"}
    except Exception as ecs:
        logger.warning(f"message: {ecs}", exc_info=True)
        raise HTTPException(status_code=500,detail=f"{ecs}")

@router.put("/{id}/assign/{agent_id}")
def assign_mission_to_agent(id: int,agent_id: int):
    logger.info(f"POST /{id}/assign/{agent_id} called")
    if miss_db.get_mission_by_id(id) is None:
        logger.error(f"POST /{id}/assign/{agent_id} failed")
        raise HTTPException(status_code=404,detail="Mission not found")
    if ag_db.agent_by_id(agent_id) is None:
        logger.error(f"POST /{id}/assign/{agent_id} failed")
        raise HTTPException(status_code=404,detail="Agent not found")
    if miss_db.get_mission_by_id(id).get("status") != "NEW":
        logger.error(f"POST /{id}/assign/{agent_id} failed")
        raise HTTPException(status_code=400,detail="Mission not available")
    if not ag_db.agent_by_id(agent_id).get("is_active"):
        logger.error(f"POST /{id}/assign/{agent_id} failed")
        raise HTTPException(status_code=400,detail="Agent is not active")
    if len(miss_db.get_open_missions_by_agent(agent_id))>2:
        logger.error(f"POST /{id}/assign/{agent_id} failed")
        raise HTTPException(status_code=400,detail="Agent has reached maximum missions")
    if miss_db.get_mission_by_id(id).get("risk_level") == "CRITICAL"\
    and ag_db.agent_by_id(agent_id).get("agent_rank") != "Commander":
        logger.error(f"POST /{id}/assign/{agent_id} failed")
        raise HTTPException(status_code=400,detail="Only Commander can handle critical missions")
    try:
        assign=miss_db.assign_mission(id,agent_id)
        if assign:
            logger.info(f"POST /{id}/assign/{agent_id} succeed")
            return {"message": "assign success"}
        else:
            logger.error(f"POST /{id}/assign/{agent_id} failed")
            return {"message": "assign failed"}
    except Exception as ecs:
        logger.warning(f"message: {ecs}", exc_info=True)
        raise HTTPException(status_code=500,detail=f"{ecs}")

@router.put("/{id}/start")
def start_mission(id:int):
    logger.info(f"PUT /{id}/start call")

    mission = miss_db.get_mission_by_id(id)
    if not mission:
        logger.error(f"mission id {id} not found")
        raise HTTPException(status_code=404, detail=f"mission id {id} not found.")
    
    
    try:
        updated = miss_db.update_mission_status(id, "IN_PROGRESS")
        
        logger.info(f"PUT missions/{id}/start finish")
        return {"message": f"update mission id {id}  successfully."}
    
    except ValueError as e:
        logger.info(f"mission start failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{id}/complete")
def complete_mission(id:int):
    logger.info(f"PUT /{id}/complete call")

    mission = miss_db.get_mission_by_id(id)
    if not mission:
        logger.error(f"mission id {id} not found")
        raise HTTPException(status_code=404, detail=f"mission id {id} not found.")
    
    try:
        updated = miss_db.update_mission_status(id, "COMPLETED")
        logger.info(f"PUT missions/{id}/complete finish")
        return {"message": f"update mission id {id}  successfully."}
    
    except ValueError as e:
        logger.info(f"mission start failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id}/fail")
def fail_mission(id:int):
    logger.info(f"PUT /{id}/fail call")

    mission = miss_db.get_mission_by_id(id)
    if not mission:
        logger.error(f"mission id {id} not found")
        raise HTTPException(status_code=404, detail=f"mission id {id} not found.")

    try:
        updated = miss_db.update_mission_status(id, "FAILED")
        logger.info(f"PUT missions/{id}/fail finish")
        return {"message": f"update mission id {id}  successfully."}
    
    except ValueError as e:
        logger.info(f"mission start failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id}/cancel")
def cancel_mission(id:int):
    logger.info(f"PUT /{id}/cancel call")

    mission = miss_db.get_mission_by_id(id)
    if not mission:
        logger.error(f"mission id {id} not found")
        raise HTTPException(status_code=404, detail=f"mission id {id} not found.")
    
    try: 
        updated = miss_db.update_mission_status(id, "CANCELED")
        logger.info(f"PUT missions/{id}/cancel finish")
        return {"message": f"update mission id {id}  successfully."}
    
    except ValueError as e:
        logger.info(f"mission start failed: {e}")
        raise HTTPException(status_code=409, detail=str(e))
