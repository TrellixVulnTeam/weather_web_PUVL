# Run APP:
export FLASK_APP=project
export FLASK_DEBUG=1
flask run

# Working Methods:
http POST http://localhost:5000/api/registration name=<NAME> password=<PASSWORD>        # Registration new user
http POST http://localhost:5000/api/login name=<NAME> password=<PASSWORD>               # Login user
http POST http://localhost:5000/api/items/new token=<TOKEN> name=<NAME> text=<TEXT>     # Create new item (TOKEN- from 'api/login')
http GET http://localhost:5000/api/items/<TOKEN>                                        # Show user's items
http DELETE http://localhost:5000/api/items/<ID> token=<TOKEN>                          # Delete user's item
http POST http://localhost:5000/api/send id=<ID> name=<NAME> token=<TOKEN>              # Send item to another user (ID- item's id; NAME- who get; TOKEN- who gives)
http GET http://localhost:5000/api/get/<LINK> token=<TOKEN>                             # Confirm recievied item (LINK- link from 'api/send'; TOKEN- who get) 
