[![UnitTests](https://github.com/MothScientist/BudgetGraph/actions/workflows/unit_tests.yml/badge.svg?branch=master)](https://github.com/MothScientist/BudgetGraph/actions/workflows/unit_tests.yml)
[![ScriptsTest](https://github.com/MothScientist/BudgetGraph/actions/workflows/scripts_tests.yml/badge.svg?branch=master)](https://github.com/MothScientist/BudgetGraph/actions/workflows/scripts_tests.yml)
![Status](https://img.shields.io/github/v/release/MothScientist/BudgetControl?label=Unstable&color=yellow)

![GIF](presentation/budget_donuts.gif)

<image src="presentation/homepage.png" alt="homepage">

## <font color="cyan">Project objectives:</font>
- ### <font color="lime">Creating temporary groups (for example, to track travel expenses)</font>
- ### <font color="lime">Full details of your income and expenses (website and bot)</font>
- ### <font color="lime">Maximum reliability and fault tolerance</font>
- ### <font color="lime">Analytics in text and graphic format</font>
- ### <font color="lime">Flexible group management</font>
- ### <font color="lime">High priority testing</font>


| Technology                                                                                                             | Version                                            |
|------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)                 | <center><font color="white">3.12.2</font></center> |
| ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)                 | <center><font color="white">3.0.2</font></center>  |
| **pyTelegramBotAPI**                                                                                                   | <center><font color="white">4.16.1</font></center> |
| ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)   | <center><font color="white">16.2</font></center>   |

### Testing:
- __Python UnitTest__
- __Pytest__
- __Selenium__ (will be added in upcoming updates)

### Launch and deployment:
- __Docker (Docker compose)__
- __Nginx__ (will be added in upcoming updates)

__You can also find configuration files for:__</br>
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)![Dependabot](https://img.shields.io/badge/dependabot-025E8C?style=for-the-badge&logo=dependabot&logoColor=white)

### <font color="aqua">For developers:</font></br>
`requirements.txt` contains the dependencies required __for the applications to work__.</br>
`requirements_external.txt` contains dependencies required __for development__.

To successfully pass the __GitHub Action tests__, you need to create secrets inside the repository with the names specified in the .yml file. This is necessary for the script to create a __.env file__, which is necessary to connect to the database, telegram bot and encrypt Flask sessions.

## Note about <font color="red">hashlib.pbkdf2_hmac()</font>: 
#### Changed in version 3.12: <u>Function now only available when Python is built with OpenSSL</u>. The slow pure Python implementation has been removed.

# <font color="white">Installation:</font>
### For Linux (with <font color="DeepSkyBlue">Docker</font>):
1. Clone the repository:</br>
```git clone https://github.com/MothScientist/budget_control.git``` </br></br>

2. Go to the project directory:</br>
```cd app``` </br></br>

3. Create .env file: </br>
```SECRET_KEY="secret_key_for_encrypt_Flask_session"```</br>
```BOT_TOKEN="bot_token"```</br>
```DATABASE="db_name.sqlite3"```</br>

4. Return to the previous directory:</br>
```cd ..``` </br></br>

5. Running a bash script: </br> 
```./deploy.sh``` </br>

### For Linux (without <font color="DeepSkyBlue">Docker</font>):
1. Clone the repository: </br>
```git clone https://github.com/MothScientist/budget_control.git``` </br></br>

### For Windows (with <font color="DeepSkyBlue">Docker Desktop</font>):
1. Clone the repository: </br>
```git clone https://github.com/MothScientist/budget_control.git``` </br></br>

2. Go to the project directory:</br>
```cd app``` </br></br>

3. Create .env file: </br>
```SECRET_KEY="your_secret_key_for_Flask_session"```</br>
```BOT_TOKEN="your_token"```</br>
```DATABASE="db_name.sqlite3"```</br>

4. Return to the previous directory:</br>
```cd ..```</br></br>

5. Run Docker Desktop</br></br>

6. Running a PowerShell script: </br> 
```./deploy_windows.ps1``` </br>

### For Windows (without <font color="DeepSkyBlue">Docker Desktop</font>):
1. Clone the repository: </br>
```git clone https://github.com/MothScientist/budget_control.git``` </br></br>

2. Make sure you have the version of Python used in the project installed. </br></br>

3. Create .env file: </br>
```SECRET_KEY="your_secret_key_for_Flask_session"```</br>
```BOT_TOKEN="your_token"```</br>
```DATABASE="db_name.sqlite3"```</br>

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
```cd app``` </br></br>

5. Create .env file: </br>
```SECRET_KEY="your_secret_key_for_Flask_session"```</br>
```BOT_TOKEN="your_token"```</br>
```DATABASE="db_name.sqlite3"```</br>

6. Database and directories creation: </br> 
```python build_project.py``` </br></br>

7. Running project files: </br>
```python webapp.py``` </br>
```python bot.py``` </br></br>

# <font color="white">How to run testing:</font>

## License
This source code is distributed under [AGPL - 3.0](https://www.gnu.org/licenses/agpl-3.0.en.html).
