from fastapi import FastAPI
import uvicorn
import logging
from database.db_connection import DB_connection
from routes import report_routes,agent_routes,mission_routes

logging.basicConfig(level=logging.INFO,filename="logs/app.log",format="%(asctime)s | %(levelname)s | %(message)s")

app= FastAPI()

app.include_router(mission_routes.router,prefix="/missions")
app.include_router(agent_routes.router,prefix="/agents")
app.include_router(report_routes.router,prefix="/reports")


if __name__ == "__main__":
    DB_connection.create_database()
    DB_connection.create_table()
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)