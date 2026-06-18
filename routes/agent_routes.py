from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from typing import Literal
from database.agent_db import AgentDB as ag_db
import logging

class CreateAgent(BaseModel):
    name:str
    specialty:str
    agent_rank:Literal["Junior","Senior","Commander"]
    
class UpdateAgent(BaseModel):
    name:str | None=None
    specialty:str | None=None
    agent_rank:Literal["Junior","Senior","Commander"] | None=None
    completed_missions:int | None=None
    failed_missions:int | None=None
    is_active:bool | None=None
    
router=APIRouter()

logger=logging.getLogger(__name__)

@router.post("")
def create_agent(new_agent:CreateAgent):
    try:
        logger.info("POST /agents called")
        agent=ag_db.create_agent(new_agent.model_dump())
        if agent:
            logger.info("POST /agents success")
            return {"message": "Agent created!"}
        else:
            logger.error("POST /agents failed")
            return{"message": "Created Failed, check the rules"}
    except Exception as ecs:
        logger.warning(f"message: {ecs}", exc_info=True)
        raise HTTPException(status_code=500,detail=f"{ecs}")
        
@router.get("")
def get_all():
    logger.info("GET /agents called")
    try:
        agents = ag_db.get_all_agents()
        logger.info("GET all agents successfully")
        return agents
    except Exception as ecs:
        logger.warning(f"message: {ecs}", exc_info=True)
        raise HTTPException(status_code=500,detail=f"{ecs}")
    

@router.put("{id}/deactivate")
def agent_deactivate(id:int):
    logger.info(f"PUT {id}/deactivate called")
    try:
        agent = ag_db.deactivate_agent(id)
        if agent:
            logger.info(f"PUT {id}/deactivate success")
            return {"message": "Deactivate Done!"}
        else:
            logger.error(f"PUT {id}/deactivate failed")
            return{"message": "check this agent you can't deactivate him for any reason."}
    except ValueError:
        raise HTTPException(status_code=404,detail="Id not found")
    except Exception as ecs:
        logger.warning(f"message: {ecs}", exc_info=True)
        raise HTTPException(status_code=500,detail=f"{ecs}")
    

@router.get("/{id}/performance")
def agent_performance(id:int):
    logger.info(f"GET /{id}/performance called")
    try:
        agent=ag_db.get_agent_performance(id)
        if agent:
            logger.info(f"GET /{id}/performance success")
            return agent
        else:
            logger.info(f"GET /{id}/performance failed")
            return {"message":"something happened and you cannot get agent performance"}
    except ValueError:
        raise HTTPException(status_code=404,detail="Id not found")
    except Exception as ecs:
        logger.warning(f"message: {ecs}", exc_info=True)
        raise HTTPException(status_code=500,detail=f"{ecs}")
    

@router.get("/{id}")
def get_gent_by_id(id:int):
    logger.info(f"GET /agent by id:{id} called")
    try:
        agent= ag_db.agent_by_id(id)
        if agent:
            logger.info("GET /agent by id:{id} success")
            return agent
        else:
            logger.error(f"GET /agent by id:{id} failed")
            raise HTTPException(status_code= 404,detail="Id not found")
    except Exception as ecs:
        logger.warning(f"message: {ecs}", exc_info=True)
        raise HTTPException(status_code=500,detail=f"{ecs}")
        
@router.put("/{id}")
def update_agent(id,up_agent:UpdateAgent):
    logger.info(f"PUT /agent update by id:{id} called")
    try:
        agent = ag_db.update_agent(id,up_agent.model_dump(exclude_none=True))
        if agent:
            logger.info(f"PUT /agent update by id:{id} success")
            return {"message": "Update succeed!"}
        else:
            logger.error(f"PUT /agent update by id:{id}: not updated")
            return {"message": "Update not done"}
    except ValueError:
        raise HTTPException(status_code=404,detail="Id not found")    
    except Exception as ecs:
        logger.warning(f"message: {ecs}", exc_info=True)
        raise HTTPException(status_code=500,detail=f"{ecs}")
    