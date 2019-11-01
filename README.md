# Jogging-Tracker


## STACK
- React + Typescript
- Redux + Redux-saga
- Apollo/GraphQL
- Django
- Django RESTframework
- Postgres

## INSTALLATION
1. Make sure you create a virtual env with python3
2. Install pipenv
  - For windows, `pip install pipenv`
  - For OS X, `pip3 install pipenv`
3. Activate virtual env you crated
4. Install python packages
```
pipenv install
```
5. Install npm packages and run dev server
```
npm install
npm run dev
```
6. Make migrations
```
cd jogging
python manage.py makemigrations
python manage.py migrate
```
7. Run the server
```
python manage.py runserver
```

## CONTRIBUTION