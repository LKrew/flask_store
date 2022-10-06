from db import db
from typing import Dict, List, Union

UserJSON = Dict[str, Union[int, str]]

class UserModel(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    activated = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_username(cls, username) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id) -> "UserModel":
        return cls.query.filter_by(id=id).first()