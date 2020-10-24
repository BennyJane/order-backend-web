# coding: utf-8
from flask import current_app

from web.extensions import db


class FoodCat(db.Model):
    __tablename__ = 'food_cat'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    weight = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    @property
    def status_desc(self):
        return current_app.config['STATUS_MAPPING'][str(self.status)]
