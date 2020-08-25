Django app for creating and passing tests.

##Installation for Linux(Ubuntu)
#####1. Download from github
```
git clone https://github.com/truekorsar/django-test-platform.git
```
#####2. Then cd into project
```
cd ./django-test-platform
```
#####3. Create Python virtual environment and activate it
```
python3 -m venv venv && source ./venv/bin/activate
```
#####4. Install all requirements
```
pip install -r requirements.txt
```
#####5. Set up environment variables
Some setting variables are sensitive, so should be moved to ***test_platform_service/test_platform_service/settings.env***.
Currently, settings.env is not in ***test_platform_service/test_platform_service***, so you are to add it.
Example for contents of this file are in ***test_platform_service/test_platform_service/settings.env.example***

```
cd ./test_platform_service/test_platform_service
touch settings.env
cat settings.env.example > settings.env
```
Then, export variables from settings.env
```
export $(grep -v '^#' settings.env | xargs -d '\n')
```
#####6. Apply all migrations
```
cd .. 
python3 manage.py migrate
```
#####7. Load prepared tests(Optionally)
```
python3 manage.py loaddata ./data/tests.json
```
#####8. Start Django server
```
python3 manage.py runserver
```