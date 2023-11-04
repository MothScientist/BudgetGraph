<image src="readme_images/homepage.png" alt="Текст с описанием картинки">

## <font color="cyan">Project objectives:</font>
- ### <font color="lime">Full details of your income and expenses (website and bot)</font>
- ### <font color="lime">Creating temporary groups (for example, to track travel expenses)</font>
- ### <font color="lime">Analytics in text and graphic format</font>
- ### <font color="lime">Flexible group management</font>


| Technology             | Version                           |
|------------------------|-----------------------------------|
| ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)         | <font color="white">3.12.0</font> |
| ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)          | <font color="white">3.0.0</font>  |
| **pyTelegramBotAPI**   | <font color="white">4.14.0</font> |
| ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)         | <font color="white">-</font>      |


![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## Note about <font color="red">hashlib.pbkdf2_hmac()</font>: 
#### Changed in version 3.12: <u>Function now only available when Python is built with OpenSSL</u>. The slow pure Python implementation has been removed.

# <font color="white">Installation</font>:
### For Linux (with <font color="DeepSkyBlue">Docker</font>):
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

### For Windows (with <font color="DeepSkyBlue">Docker Desktop</font>):
1. Clone the repository: </br>
```git clone https://github.com/MothScientist/budget_control.git``` </br></br>

2. Go to the project directory:</br>
```cd main``` </br></br>

3. Create .env file: </br>
```SECRET_KEY="your_secret_key_for_Flask_session"```</br>
```BOT_TOKEN="your_token"```</br>
```DATABASE="db_name.sqlite3"```</br></br>

4. Return to the previous directory:</br>
```cd ..```</br></br>

5. Run Docker Desktop</br></br>

6. Running a PowerShell script: </br> 
```./run_on_windows_with_docker_desktop.ps1``` </br>

### For Windows (without <font color="DeepSkyBlue">Docker Desktop</font>):
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
```./run_on_windows_without_container.ps1``` </br>

### For all users:
1. Clone the repository: </br>
```git clone https://github.com/MothScientist/budget_control.git``` </br></br>

2. Make sure you have the version of Python used in the project installed. </br></br>

3. Install backend dependencies: </br> 
```pip install -r requirements.txt``` </br></br>

4. Go to the project directory:</br>
```cd main``` </br></br>

5. Create .env file: </br>
```SECRET_KEY="your_secret_key_for_Flask_session"```</br>
```BOT_TOKEN="your_token"```</br>
```DATABASE="db_name.sqlite3"```</br></br>

6. Database and directories creation: </br> 
```python creating_db_and_directoriespy``` </br></br>

7. Running project files: </br>
```python app.py``` </br>
```python bot.py``` </br></br>
