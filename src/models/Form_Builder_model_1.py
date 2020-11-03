from . import db
from sqlalchemy.dialects.postgresql import JSON
from marshmallow import fields, Schema

class Model_1(db.Model):

    __tablename__ = 'Form_Builder_model_1'

    id = db.Column(db.Integer, primary_key=True)
    label1 = db.Column(db.String(256), nullable=False)
    fetch = db.Column(db.String(30), default='')
    game =  db.Column(JSON)

    def __init__(self, item):
        """
        Class constructor
        """
        self.label1 = item.get('label1')
        self.fetch = item.get('fetch')
        self.game = item.get('game')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        #self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_models():
        return Model_1.query.all()

    @staticmethod
    def get_one_model(id):
        return Model_1.query.get(id)

    def __str__(self):
        return self.label1

    @staticmethod
    def serialize(self):
        return {
            'id':self.id,
            'label1': self.label1,
            'fetch': self.fetch,
            'game': self.game
        }


class Model_1Schema(Schema):

  """
  Model1 Schema
  """
  class Meta:
      fields = ('id','label1','fetch','game')

  id = fields.Int(dump_only=True)
  label1= fields.Str(required=False)
  fetch = fields.Str(required=False)
  game = fields.Raw(required=False)


