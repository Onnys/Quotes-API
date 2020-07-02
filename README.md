# Quotes API
Reflexoes is a restful API where Authors can write quotes and share with others, this api allows users to be spontaneous on their ideas without being censured.
## Getting Started 

### Installing Dependencies

#### Python 3.7
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


## Running the server

From within the  directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source setup.sh
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
## Endpoints
- GET '/authors'
- GET '/quotes'
    Returns a list of all quotes.
- GET '/authors/<int:author_id>/quotes'
    Returns a list of all quotes from an author.
- GET '/authors/search'

- GET '/quotes/search'
- POST '/authors'
- POST '/quotes'
- PATCH '/quotes/<int:quote_id>'
- DELETE '/quotes/<quote_id>'

GET '/authors'
- Fetches a dictionary of Authors.
- Request Argument: none.
- Returns: A JSON with list of Authors objects and a success value.
bash``` ```