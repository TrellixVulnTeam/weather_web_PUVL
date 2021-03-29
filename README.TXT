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
