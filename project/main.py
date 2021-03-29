from flask import Blueprint, render_template, url_for, flash, request
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from .models import Item
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/profile', methods=['POST'])
@login_required
def profile_post():
    return redirect(url_for('main.profile'))


@main.route('/items/<int:id>')
@login_required
def item(id):
    item = Item.query.filter_by(id=id).first()
    db.session.commit()
    return render_template('item.html', item=item)


@main.route('/items/<int:id>/delete')
@main.route('/items/<int:id>/delete', methods=['POST'])
@login_required
def delete_item(id):
    item_del = Item.query.filter_by(id=id).first()
    db.session.delete(item_del)
    db.session.commit()
    flash('Item deleted', 'success')
    return redirect(url_for('main.items'))


@main.route('/inbox_items')
@login_required
def inbox_items():
    # item = Item.query.filter_by(id=id).first()
    # db.session.commit()
    return render_template('inbox_items.html')


@main.route('/items')
@login_required
def items():
    user_token = current_user.token
    is_none = Item.query.filter_by(token=user_token).first()
    items_list = Item.query.filter_by(token=user_token).all()
    if is_none is None:
        flash('Items list is empty', 'warning')
        return redirect(url_for('main.profile'))
    return render_template('items.html', items_list=items_list)


@main.route('/items', methods=['POST'])
def items_post():
    return redirect(url_for('main.items'))


@main.route('/items/new')
@main.route('/items/new', methods=['POST'])
@login_required
def items_new():
    return render_template('items_new.html')


@main.route('/new', methods=['POST'])
@login_required
def items_new_post():
    name = request.form.get('name')
    text = request.form.get('text')
    user_token = current_user.token
    if str(name).lstrip() != '':
        flash('Item successfully created', 'success')
        new_item = Item(name=name, text=text, token=user_token)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('main.profile'))
    else:
        flash('The name is empty. Please enter it', 'error')
        return redirect(url_for('main.items_new'))
