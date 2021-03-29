from flask import jsonify, Blueprint, request
from project import db
from project.api.api_errors import bad_request, good_request
from project.models import Item, User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

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
    responce = Item.query.filter_by(name=name).first()
    return jsonify({'message': 'Item successfully created'},
                   {'id': responce.id,
                    'name': responce.name,
                    'text': responce.text})


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
    id = int(data['id'])
    name = data['name']
    token_sent = data['token']
    user = User.query.filter_by(name=name).first()
    token_reciev = user.token
    s = Serializer('WEBSITE_SECRET_KEY', 60 * 30)  # 60 secs by 5 mins
    link = s.dumps({'id': id, 'token_sent': token_sent, 'token_reciev': token_reciev}).decode('utf-8')  # encode
    return jsonify(link)


@api_main.route('/get')
def get_item():
    data = request.get_json() or {}
    pass
