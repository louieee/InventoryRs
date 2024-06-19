
# How to Set up 


### <li> After downloading or cloning the app, Go to your terminal and navigate to the app's root directory</li>
### <li> Setup the Virtual environment, and activate it.</li>
### <li> Run <code>pip install -r requirements.txt</code> to install the dependencies to the virtual environment.</li>
### <li> Run <code>python manage.py makemigrations</code> to create a migration file.</li>
### <li> Run <code>python manage.py migrate</code> to create the tables in the database.</li>
### <li> Run <code>python manage.py create_employee</code> to create an employee</li>
### <li> Run <code>python manage.py runserver</code> to start up the server </li>
### <li> Navigate to <a href="http://localhost:8000/api/docs/"> Docs </a> to view the documentation and interact with the endpoints.</li>
### <li> Using the login endpoint, login and get your auth token with which you can authorize.</li>
### <li> Then you can access the endpoints freely.</li>

## Bonus Tip
### <li>Run <code>python manage.py createsuperuser</code> to create a super user
### <li> navigate to <a href="http://localhost:8000/admin/">Admin Dashboard</a>, login and access all the records.

