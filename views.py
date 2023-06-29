from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from app_db import Session
from models import Advertisement, User
from errors import HttpError
from methods import get_adv, validate, get_user, hash_password
from rules import AdvCreating, AdvEditing, UserCreating, UserEditing

app = Flask('advertisements_app')


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    res = jsonify({'status': 'error', 'description': error.description})
    res.status_code = error.status_code
    return res


class AdvView(MethodView):
    def get(self, adv_id: int):
        with Session() as s:
            adv = get_adv(adv_id, s)
            return jsonify({
                'id': adv.id,
                'title': adv.title,
                'owner': adv.user_id,
                'published': adv.creation_time,
                'description': adv.description,
            })

    def post(self):
        json_data = validate(request.json, AdvCreating)
        with Session() as s:
            adv = Advertisement(**json_data)
            s.add(adv)
            s.commit()
            return jsonify({
                'id': adv.id,
                'title': adv.title,
                'owner': adv.user_id,
                'published': adv.creation_time,
                'description': adv.description,
            })

    def patch(self, adv_id: int):
        json_data = validate(request.json, AdvEditing)
        with Session() as s:
            adv = get_adv(adv_id, s)
            for key, value in json_data.items():
                setattr(adv, key, value)
            s.add(adv)
            s.commit()
            return jsonify({'status': 'success'})

    def delete(self, adv_id: int):
        with Session() as s:
            adv = get_adv(adv_id, s)
            s.delete(adv)
            s.commit()
            return jsonify({'status': 'deleted'})


class UserView(MethodView):
    def get(self, user_id: int):
        with Session() as s:
            user = get_user(user_id, s)
            return jsonify({'id': user.id, 'email': user.email})

    def post(self):
        json_data = validate(request.json, UserCreating)
        json_data['password'] = hash_password(json_data['password'])
        with Session() as s:
            user = User(**json_data)
            s.add(user)
            try:
                s.commit()
            except IntegrityError as error:
                raise HttpError(409, 'Email already exists')
            return jsonify({'id': user.id, 'email': user.email})

    def patch(self, user_id: int):
        json_data = validate(request.json, UserEditing)
        if 'password' in json_data:
            json_data['password'] = hash_password(json_data['password'])
        with Session() as s:
            user = get_user(user_id, s)
            for key, value in json_data.items():
                setattr(user, key, value)
            s.add(user)
            s.commit()
            return jsonify({'status': 'success'})

    def delete(self, user_id: int):
        with Session() as s:
            user = get_user(user_id, s)
            s.delete(user)
            s.commit()
            return jsonify({'status': 'deleted'})


app.add_url_rule('/advertisements/<int:adv_id>/', view_func=AdvView.as_view(
    'adv_properties'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/advertisements/', view_func=AdvView.as_view(
    'advertisements'), methods=['POST'])
app.add_url_rule('/users/<int:user_id>/', view_func=UserView.as_view(
    'user_properties'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users/', view_func=UserView.as_view('users'), methods=[
    'POST'])

if __name__ == '__main__':
    app.run(port=5001)
