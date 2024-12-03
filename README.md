[![UnitTests](https://github.com/MothScientist/BudgetGraph/actions/workflows/unit_tests.yml/badge.svg?branch=master)](https://github.com/MothScientist/BudgetGraph/actions/workflows/unit_tests.yml)
[![Build Test](https://github.com/MothScientist/BudgetGraph/actions/workflows/build_test.yml/badge.svg?branch=master)](https://github.com/MothScientist/BudgetGraph/actions/workflows/build_test.yml)
[![Pylint](https://github.com/MothScientist/BudgetGraph/actions/workflows/pylint.yml/badge.svg?branch=master)](https://github.com/MothScientist/BudgetGraph/actions/workflows/pylint.yml)
[![Flake8](https://github.com/MothScientist/BudgetGraph/actions/workflows/flake8.yml/badge.svg)](https://github.com/MothScientist/BudgetGraph/actions/workflows/flake8.yml)
![Status](https://img.shields.io/github/v/release/MothScientist/BudgetControl?label=Unstable&color=yellow)
![Static Badge](https://img.shields.io/badge/python-3.12-blue)
![Static Badge](https://img.shields.io/badge/First_commit-August_20%2C_2023-blue)


![GIF](media/budget_donuts.gif)

<image src="media/homepage.png" alt="homepage">

## <font color="cyan">Project objectives:</font>
- ### <font color="lime">Creating temporary groups (for example, to track travel expenses)</font>
- ### <font color="lime">Full details of your income and expenses (website and bot)</font>
- ### <font color="lime">Maximum reliability and fault tolerance</font>
- ### <font color="lime">Analytics in text and graphic formats</font>
- ### <font color="lime">Flexible group management</font>
- ### <font color="lime">High priority testing</font>


| Technology            | Version                                            |
|-----------------------|----------------------------------------------------|
| ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)        | <center><font color="white">3.12.7</font></center> |
| ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)         | <center><font color="white">3.1.0</font></center>  |
| **pyTelegramBotAPI**  | <center><font color="white">4.24.0</font></center> |
| ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)      | <center><font color="white">16.2</font></center>   |

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

## When installed on <font color="aqua">MacOS</font> or run in a container on this operating system:
#### When running on MacOS, pay attention to errors in the psycopg2 library - to solve them, you will need to install psycopg2-binary instead.

# <font color="white">Installation:</font>
### For Linux (with <font color="DeepSkyBlue">Docker</font>):


### For Linux (without <font color="DeepSkyBlue">Docker</font>):


### For Windows (with <font color="DeepSkyBlue">Docker Desktop</font>):


### For Windows (without <font color="DeepSkyBlue">Docker Desktop</font>):


# <font color="white">How to run testing:</font>

## License
This source code is distributed under [AGPL - 3.0](https://www.gnu.org/licenses/agpl-3.0.en.html).
