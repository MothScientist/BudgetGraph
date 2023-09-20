A microservice using **Flask**, which has a very simple web interface and a telegram bot (as the main communication channel between the client and the program).</br>This service allows you to control your/family/team budget, receive advanced statistics and has flexible functionality within the scope of its purpose.

| Technology                                                                                              | Version |
|---------------------------------------------------------------------------------------------------------|---------|
| ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  | 3.11.5  |
| ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)  | 2.3.3   |
| **pyTelegramBotAPI**  |  4.13.0 |
| ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)  |  - |


![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## *Installation*
1. Clone the repository: </br>
```git clone https://github.com/MothScientist/budget_control.git``` </br></br>
2. Write __db_path__ in the database_control.py file (by default it is pulled from the .env file). </br></br> 
3. Running a bash script: </br> 
```./run.sh``` </br></br>

_**OR**_ </br> </br>

1. Clone the repository: </br>
```git clone https://github.com/MothScientist/budget_control.git``` </br></br>
2. Install backend dependencies: </br> 
```pip install -r requirements.txt``` </br></br>
3. Go to the project directory:</br>
```cd main``` </br></br>
4. Write __db_path__ in the database_control.py file (by default it is pulled from the .env file). </br></br> 
5. Database creation: </br> 
```python database_control.py``` </br></br>
6. Running project files: </br>
```python app.py``` </br>
```python bot.py``` </br></br>
