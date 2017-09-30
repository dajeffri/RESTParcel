# RESTParcel

This is a Django REST framework API for a potential REACT or Mobile App. It will allow a front end to process pre address mail pieces.

This is really just something for my development portfolio. If you have any interest in an actual product please contact M.A.I.L. Inc. and ask about there SMARTParcel product.

## Getting Started

Install Python, Django, and the Django REST framework. This was developed with Python v2.7, Django v1.11.4, and djangorestframework v3.6.4.

### Prerequisites

* Python - [https://www.python.org/]
* Django - [https://github.com/django/django]
* Django REST Framework - [https://github.com/encode/django-rest-framework]

### Installing

Download the repository from github, either through the command line or with the "Clone or download" button. Open Powershell or a terminal and navigate to the project directory. 

Now you can run the server.

```
python manage.py runserver
```

Open a browser and navigate to the link that should be provided in the terminal. 

```
http://127.0.0.1:8000/
```

You can log in in the top right. Default users are admin, c1e1, c1e2, c1e3, c2e1...
All passwords are "pass1234"
If you log in as admin you can view the administration panel.

```
http://127.0.0.1:8000/admin
```

You will be able to add and update companies, users, profiles, addresses, costcenters, and mailpieces. You can do this in the browser or by opening another terminal and sending standard JSON requests.

## Running the tests

Tests can be run from the project directory.

```
python manage.py test
```

## Built With

* [Python](https://www.python.org/)
* [Django](https://github.com/django/django)
* [Django REST Framework](https://github.com/encode/django-rest-framework)
* [ATOM](https://atom.io/)



## Authors

* **Dan Jeffries** - *Initial work* - [dajeffri](https://github.com/dajeffri)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to [PurpleBooth](https://github.com/PurpleBooth) for her README template.
