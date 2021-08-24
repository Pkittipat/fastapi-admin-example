# fastapi-admin-example
### How to run local server
#### 1. Set environment file. 
change example.env to .env
#### 2. Run database and redis on docker
```
docker-compose up -d
```
#### 3. Install python package
```
pip install -r requirements.txt
```
#### 4. Run server
```
uvicorn app.main:app --reload
```

#### Create super admin first
like create admin http://127.0.0.1:8000/admin/init
#### login
like http://127.0.0.1:8000/admin/login
