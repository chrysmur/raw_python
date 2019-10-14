# raw_python
- username and password are just a user i created for postgres

# Testing User Creation
```
python userdb.py 
Create a User:

Username: lae

Email: lae@shang.io     
Password:password
Role, (administration,hr,accounts,support,customer service): customer service 
{"message": "user lae created successfully"} #response
```


# Testing User Authentication
```
python userdb.py 
User: chrys
password:password
{"message": "logged in successfully"} #response

python userdb.py 
User: chrys
password:anotherpass
{"error": "invalid password for user chrys"}

```
