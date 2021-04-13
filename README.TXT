# Run APP:
export FLASK_APP=project
export FLASK_DEBUG=1
flask run

# Working Methods:
http POST http://localhost:5000/api/registration name=<NAME> password=<PASSWORD>
http POST http://localhost:5000/api/login name=<NAME> password=<PASSWORD>
http POST http://localhost:5000/api/items/new token=<TOKEN> name=<NAME> text=<TEXT>
http GET http://localhost:5000/api/items/<TOKEN>
http DELETE http://localhost:5000/api/items/<ID> token=<TOKEN>
http POST http://localhost:5000/api/send id=<ID> name=<NAME> token=<TOKEN>
http GET http://localhost:5000/api/get link=<NAME> token=<TOKEN>


http POST http://localhost:5000/api/registration name=Alex password=123
http POST http://localhost:5000/api/login name=Alex password=123
http POST http://localhost:5000/api/items/new token=o0tPw7pjOhSUjRIDNjAQhfNq1xZ8i2Ry name=Note_2 text='Its my first test note'
http GET http://localhost:5000/api/items/o0tPw7pjOhSUjRIDNjAQhfNq1xZ8i2Ry
http DELETE http://localhost:5000/api/items/6 token=o0tPw7pjOhSUjRIDNjAQhfNq1xZ8i2Ry
http POST http://localhost:5000/api/send id=7 name=Jack token=o0tPw7pjOhSUjRIDNjAQhfNq1xZ8i2Ry
http GET http://localhost:5000/api/get link=http://localhost:5000/api/get/NzpKYWNrOm8wdFB3N3BqT2hTVWpSSUROakFRaGZOcTF4WjhpMlJ5 token=myXQdU9B7MOrRM76l6AEBatFaJMXgrB2
