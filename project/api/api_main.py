import base64
from flask import jsonify, Blueprint, request
from project import db
from project.api.api_errors import bad_request, good_request
from project.models import Item, User

api_main = Blueprint('api_main', __name__)


@api_main.route('/api/user/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@api_main.route('/api/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = []
    for user in users:
        id = user.id
        data = User.query.get(id).to_dict()
        users_list.append(data)
    return jsonify(users_list)


@api_main.route('/api/items/new', methods=['POST'])
def create_item():
    data = request.get_json() or {}
    token = data['token']
    name = data['name']
    text = data['text']
    user_items = Item.query.filter_by(token=token).all()
    for item in user_items:
        if str(item.name) == name:
            return bad_request('Please use a different item name')

    new_item = Item(name=name, text=text, token=token)
    db.session.add(new_item)
    db.session.commit()
    responce = Item.query.filter_by(token=token).all()
    for item in responce:
        if item.name == name:
            return jsonify({'message': 'Item successfully created'},
                           {'id': item.id,
                            'name': item.name,
                            'text': item.text})
    return


@api_main.route('/api/items/<token>', methods=['GET'])
def get_items(token):
    find_items = Item.query.filter_by(token=token).first()
    items = Item.query.filter_by(token=token).all()
    if find_items is None:
        return bad_request('Items list is empty')
    else:
        items_list = []
        for item in items:
            id = int(item.id)
            data = Item.query.get(id).to_dict()
            items_list.append(data)
        return jsonify(items_list)


@api_main.route('/api/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    data = request.get_json() or {}
    token = data['token']

    user_items = Item.query.filter_by(token=token).all()
    for item in user_items:
        if int(item.id) == id:
            obj = Item.query.filter_by(id=int(item.id)).first()
            db.session.delete(obj)
            db.session.commit()
            return good_request('Item deleted')
    return bad_request('Id/token missing')


@api_main.route('/api/send', methods=['POST'])
def send_item():
    data = request.get_json() or {}
    if 'id' not in data or 'name' not in data or 'token' not in data:
        return bad_request("Must include item's id, user's login and token fields")

    item_id = int(data['id'])
    user_name = data['name']
    token_send = data['token']
    user = User.query.filter_by(name=user_name).first()
    if user is None:
        return bad_request("User '%s' does not exist" % user_name)

    user_items = Item.query.filter_by(token=token_send).all()
    for item in user_items:
        if item_id == item.id:
            data = str(item_id) + ':' + user_name + ':' + token_send
            encoded = (base64.b64encode(data.encode('ascii')))
            encoded_link = encoded.decode('ascii')
            return 'http://localhost:5000/api/get/%s' % encoded_link
    return bad_request('Link is incorrect')


@api_main.route('/api/get/<link>', methods=['GET'])
def get_item(link):
    data = request.get_json() or {}
    if 'token' not in data:
        return bad_request("Must include item's link and token fields")

    try:
        received_token = data['token']
        decoded = base64.b64decode(link.encode('ascii'))
        decoded_link = decoded.decode('ascii')

        item_id = decoded_link[:decoded_link.find(':')]
        name = decoded_link[decoded_link.find(':') + 1:decoded_link.rfind(':')]
        sented_token = decoded_link[decoded_link.rfind(':') + 1:]
        user = User.query.filter_by(name=name).first()
        if user.token == received_token:
            item = Item.query.filter_by(id=item_id).first()
            if item.token == sented_token:
                item.token = received_token
                db.session.add(item)
                db.session.commit()
                return good_request('Item received successfully')
        return bad_request('Link expired')
    except Exception:
        return bad_request('Link incorrect')
