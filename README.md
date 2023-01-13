# ku-polls

## Online Polls And Surveys

[![Unittest](https://github.com/ThanadolU/ku-polls/actions/workflows/test.yml/badge.svg)](https://github.com/ThanadolU/ku-polls/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/ThanadolU/ku-polls/branch/main/graph/badge.svg?token=PTPT1VUUCO)](https://codecov.io/gh/ThanadolU/ku-polls)

An application for conducting online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/4.1/intro/tutorial01/), with
additional features.

App created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## Install and Run

1. first clone this repository by type this command in your terminal at your choose path
   ```
   git clone https://github.com/ThanadolU/ku-polls.git
   ```

2. make sure that you install all the requirements by run this command, its can be whether `pip`, `pip3`, or `python -m pip`
   ```
   pip install -r requirements.txt
   ```

3. You will need to configure your server using `.env` (you may get your secret key [here](https://djecrety.ir/)). Take a look at `sample.env`.

4. Create the database run
   ```
   python manage.py migrate
   ```
5. Load the data
   ```
   python manage.py loaddata data/polls.json data/users.json
   ```

6. The final step is to run the development server by,
   ```
   python manage.py runserver
   ```

You can now visit, `http://127.0.0.1:8000/` or `http://localhost:8000`

## Demo Admin

|   Username   |   password   |
|:-------------|:-------------|
|  test_admin  |   789630     |

## Demo Users

|   Username   |   password   |
|:-------------|:-------------|
|   harry	   |   hackme22   |
|   guest123   |   8520       |

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](https://github.com/ThanadolU/ku-polls/wiki/Vision-Statement)
- [Requirements](https://github.com/ThanadolU/ku-polls/wiki/Requirements)
- [Development Plan](https://github.com/ThanadolU/ku-polls/wiki/Development-Plan)
- [Iteration 1](https://github.com/ThanadolU/ku-polls/wiki/Iteration-1-Plan) and [Task Board](https://github.com/users/ThanadolU/projects/6/views/2)
- [Iteration 2](https://github.com/ThanadolU/ku-polls/wiki/Iteration-2-Plan) and [Task Board](https://github.com/users/ThanadolU/projects/6/views/11)
- [Iteration 3](https://github.com/ThanadolU/ku-polls/wiki/Iteration-3-Plan) and [Task Board](https://github.com/users/ThanadolU/projects/6/views/12)
- [Iteration 4](https://github.com/ThanadolU/ku-polls/wiki/Iteration-4-Plan) and [Task Board](https://github.com/users/ThanadolU/projects/6/views/13)
