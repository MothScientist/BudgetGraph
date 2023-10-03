A microservice using **Flask**, which has a very simple web interface and a **telegram bot**
(as the main communication channel between the client and the program).</br></br>
This service allows you to control your/family/team budget, receive advanced statistics and has flexible functionality 
within the scope of its purpose.</br></br>

| Technology                                                                                                   | Version |
|--------------------------------------------------------------------------------------------------------------|---------|
| ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)       | 3.11.5  |
| ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)       | 3.0.0   |
| **pyTelegramBotAPI**                                                                                         | 4.14.0  |
| ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) | -       |


![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## Installation:
### For Linux:
1. Clone the repository:</br>
```git clone https://github.com/MothScientist/budget_control.git``` </br></br>

2. Go to the project directory:</br>
```cd main``` </br></br>

3. Create .env file: </br>
```SECRET_KEY="secret_key_for_encrypt_Flask_session"```</br>
```BOT_TOKEN="bot_token"```</br>
```DATABASE="db_name.sqlite3"```</br></br>

4. Return to the previous directory:</br>
```cd ..``` </br></br>

5. Running a bash script: </br> 
```./deploy.sh``` </br>

### For Windows:
1. Clone the repository: </br>
```git clone https://github.com/MothScientist/budget_control.git``` </br></br>

2. Make sure you have the version of Python used in the project installed. </br></br>

3. Create .env file: </br>
```SECRET_KEY="your_secret_key_for_Flask_session"```</br>
```BOT_TOKEN="your_token"```</br>
```DATABASE="db_name.sqlite3"```</br></br>

4. Return to the previous directory:</br>
```cd ..``` </br></br>

5. Running a PowerShell script: </br> 
```./run_windows.ps1``` </br>

### For all:
1. Clone the repository: </br>
```git clone https://github.com/MothScientist/budget_control.git``` </br></br>

2. Install backend dependencies: </br> 
```pip install -r requirements.txt``` </br></br>

3. Go to the project directory:</br>
```cd main``` </br></br>

4. Create .env file: </br>
```SECRET_KEY="your_secret_key_for_Flask_session"```</br>
```BOT_TOKEN="your_token"```</br>
```DATABASE="db_name.sqlite3"```</br></br>

5. Database creation: </br> 
```python database_control.py``` </br></br>

6. Running project files: </br>
```python app.py``` </br>
```python bot.py``` </br></br>
