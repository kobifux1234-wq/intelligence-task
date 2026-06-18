# intelligence-task-manager

## System description
The purpose of the system is to manage agents and tasks from a DATABASE.

## The folder structure

```
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Table structure

### Agents Table

Field | Type | Comments
----|----|----
id | INT,AUTO_INCREMENT,PK | UNIQUE type
name | VARCHAR | Agent name
specialty| VARCHAR | Area of ​​expertise
is_active | BOOLEAN | Default TRUE
completed_missions | INT | Default 0
failed_missions | INT | Default 0
agent_rank| VARCHAR / ENUM | only Comander/Senior/Junior  

### Missions Table
Field | Type | Comments
----|----|----
id | INT,AUTO_INCREMENT,PK | PK type
title | VARCHAR | mission's title
description | TEXT | full description of mission
location | VARCHAR | location
difficulty | INT | only between 1-10
importance | INT | only between 1-10
status | VARCHAR | Default : NEW
risk_level | VARCHAR | automatically calculated
assigned_agent_id | INT | NULL until someone will get it

## Classes Explanation 
### db_connection
Responsible for managing connections to the database.

Role | Method
---- | ----
return active connection | get_connection()
create intelligence if not exists | create_database()
create two tables if not exists | create_tables()

### MissionDB
Responsible for all SQL operations against the missions table.
Role | Method
---- | ----
Create new mission ad return full object | create_mission(data)
Return all missions |  get_all_missions()
Return mission by ID or NONE | get_get_mission_by_id(id)
Assigns a task to an agent | assign_mission(m_id, a_id)
Used for status changing | update_mission_status(id, status)
Return missions ASSIGNED/IN_PROGRESS of agent | get_open_missions_by_agent(id)
Total missions | count_all_missions()
Count missions by status | count_by_status(status)
Count opening missions | count_open_missions()
Count critical missions | count_critical_missions()
Agent with highest completed missions | get_top_agent()


### AgentDB
Responsible for all SQL operations against the agents table.

Role | Method
---- | ----
Create new agent and return obj of agent |  create_agent(data)
Return list of all agents | get_all_agents()
Return agent by ID or NONE | get_agent_by_id(id)
Update to whole row (cant change ID) | update_agent(id, data)
Set agent deactivate | deactivate_agent(id)
Update missions completed | increment_completed(id)
Update missions failed | increment_failed(id)
Returns a dictionary with these keys completed, failed, total, success_rate (note that this value is calculated as success_rate - what percentage of tasks completed successfully out of the total) | get_agent_performance(id)
Return sum agents active | count_active_agents()


## system rules

**Business rules to be implemented in the data layer**

- 1 rank must be Junior / Senior / Commander — any other value throws an error.
- 2 difficulty and importance must be between 1 and 10 — otherwise an error.
- 3 risk_level is calculated automatically when creating a task — the user does not submit it.
- 4 An agent with is_active=False cannot accept tasks.
- 5 An agent cannot have more than 3 open tasks (ASSIGNED / IN_PROGRESS) at the same time.
- 6 If risk_level=CRITICAL — only an agent with the Commander rank can accept the task.
- 7 Only a task with the status NEW can be assigned. After assignment: status=ASSIGNED.
- 8 Only a task with the status ASSIGNED can be started. After: status=IN_PROGRESS.
- 9 Only a task can be finished. IN_PROGRESS and change to failed or completed status
- 10 Only a task in NEW or ASSIGNED status can be canceled — otherwise an error.

---
**Running instructions**
```
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
    -e MYSQL_DATABASE=Intelligence_db \
    -p 3306:3306 mysql:8.0

```

# DAY 2
Today we build the server for database that we created yesterday

## Updated folder structure

```
intelligence-task-manager/
├── main.py
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── routes/
│   ├── agent_routes.py
│   ├── mission_routes.py
│   └── report_routes.py
├── logs/
│   └── app.log
├── README.md
├── requirements.txt
└── .gitignore
```

## Agents endpoints — `agent_routes.py`

| Method | Endpoint | Description |
|---|---|---|
| POST | /agents/ | Create a new agent |
| GET | /agents/ | Get all agents |
| GET | /agents/{id} | Get agent by ID |
| PUT | /agents/{id} | Update agent |
| PUT | /agents/{id}/deactivate | Deactivate agent |
| GET | /agents/{id}/performance | Get agent performance |

## Missions endpoints — mission_routes.py

| Method | Endpoint | Description |
|---|---|---|
| POST | /missions/ | Create a new mission |
| GET | /missions/ | Get all missions |
| GET | /missions/{id} | Get mission by ID |
| PUT | /missions/{id}/assign/{agent_id} | Assign mission to agent |
| PUT | /missions/{id}/start | Start mission |
| PUT | /missions/{id}/complete | Finish mission successfully |
| PUT | /missions/{id}/fail | Finish mission as failed |
| PUT | /missions/{id}/cancel | Cancel mission |

## Reports endpoints — report_routes.py

| Method | Endpoint | Description |
|---|---|---|
| GET | /reports/summary | General system report |
| GET | /reports/missions-by-status | Missions grouped by status |
| GET | /reports/top-agent | Top agent (get_top_agent()) |

## System flow — full scenario

1. **Create an agent** — POST /agents/ (name, specialty, agent_rank, is_active defaults to TRUE).
2. **Create a mission** — POST /missions/ (title, description, location, difficulty, importance). risk_level is calculated automatically, status starts at NEW.
3. **Assign the mission** — PUT /missions/{id}/assign/{agent_id}. Goes through the 6 checks above, on success, assigned_agent_id is set and status becomes ASSIGNED.
4. **Start the mission** — PUT /missions/{id}/start. Only works if status is ASSIGNED, moves to IN_PROGRESS.
5. **Finish the mission** — one of:
   - PUT /missions/{id}/complete - status completed, agent's completed_missions incremented.
   - PUT /missions/{id}/fail - status failed, agent's failed_missions incremented.
   - PUT /missions/{id}/cancel - status canceled (only allowed from NEW or ASSIGNED).
6. **Check agent performance** — GET /agents/{id}/performance reflects the updated completed/failed/success_rate.
7. **Pull reports** — GET /reports/summary, GET /reports/missions-by-status, GET /reports/top-agent reflect the change across the whole system.

## Running instructions

### 1. Start MySQL with Docker

```bash
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
    -e MYSQL_DATABASE=Intelligence_db \
    -p 3306:3306 mysql:8.0
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI server

```
python main.py
```