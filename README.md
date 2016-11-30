# wordlinks
I'm redoing my python-wordladder app. You will notice very quickly that this is just one huge hack as I try to find the time to work out my thoughts and put everything to code -- one stumbling step at a time. However, the app pretty much works.
# Install instructions
1. I use `pip` and `virtualenv` so install that, then do a `pip install -r requirements.txt` to get the required libraries.
2. If you have `mysql` create a database, then update the `config.py` file by changing the `SQLALCHEMY_DATABASE_URI` setting.
3. If you prefer to use `sqlite` (it will be quite slow), uncomment the connection string details in same setting.
4. Run `./db_create.py` to create the database.
5. A default user will be created. Login with `buttsmckraken@bikinibottom.com/password`.
6. Update the `config.py` by changing the `ADMINS` email address list.
7. Get everything running by `./run.py`.
8. You may want to go [http://127.0.0.1:5000/apihelper] (apihelper page) before you actually log in just to see what API calls are available which I have not yet implemented in the UI.
9. There is a scrabble word scorer, and a target word and wordladder api. Along the way you'll see logging, email, user registration/authentication, database access, algorithms, lambda expressions, list comprehensions, set partitioning, bootstrap, REST, and a whole lot of other stuff you can expect to see from someone sipping Oros and eating cherry licorice late at night.
