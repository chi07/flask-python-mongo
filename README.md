# cpd-account-service


```bash
python -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```
On Mac OSX or Ubuntu run
```bash
export MONGO_URI="mongodb+srv://<username>:<password>@cluster0.xzizm.mongodb.net/cdp-account-service?retryWrites=true&w=majority"
export MONGO_DB_NAME="cdp-account-service"
export DEBUG=true
python server.py
```

# Example API
## Add User
```json
curl --location --request POST 'http://0.0.0.0:5001/api/v1/users/add' \
--header 'Content-Type: application/json' \
--data-raw '{
	"username": "chipv",
	"name": "Chi Pham",
	"email": "chipv@gmail.com",
	"password": "secret",
	"password_confirmation": "secret",
	"role": "admin"
}'
```

## Login
```json
curl --location --request POST 'http://0.0.0.0:5001/api/v1/login' \
--header 'Content-Type: application/json' \
--data-raw '{
	"email": "chipv@gmail.com",
	"password": "secret"
}'
```