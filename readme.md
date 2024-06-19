
# How to Set up 


### <li> After downloading or cloning the app, Go to your terminal and navigate to the app's root directory
### <li> Setup the Virtual environment, and activate it.
### <li> Run <code>pip install -r requirements.txt</code> to install the dependencies to the virtual environment.
### <li> Run <code>python manage.py makemigrations</code> to create a migration file.
### <li> Run <code>python manage.py migrate</code> to create the tables in the database.
### <li> Run <code>python manage.py create_employee</> to create an employee
### <li Run <code>python manage.py runserver</code> to start up the server
### <li>navigate to <a href="http://localhost:8000/api/docs/"> Docs </a> to view the documentation and interact with the endpoints.
### using the login endpoint, login and get your auth token with which you can authorize.
### then you can access the endpoints freely.</li>

## Bonus Tip
### <li>Run <code>python manage.py createsuperuser</code> to create a super user
### <li> navigate to <a href="http://localhost:8000/admmin/">Admin Dashboard</a>, login and access all the records.

