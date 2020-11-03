from marshmallow import fields, Schema
import datetime
from . import db
from .FieldModel import FieldSchema
from sqlalchemy import desc

class FormModel(db.Model):

    __tablename__ = 'form_form'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(128), nullable=False)
    version =  db.Column(db.String(128), nullable=False,default='0')
    form_id = db.Column(db.String(128), nullable=False,default='0')
    status = db.Column(db.String(64), nullable=False, default='Active')
    fetchtxt = db.Column(db.String(128), default='')
    flow_id = db.Column(db.String(128),nullable=False,default='0')
    node_id = db.Column(db.String(128), nullable=False, default='0')
    nodes = db.relationship('FieldModel', backref='FormModel', lazy=True)
    children = []


    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('label1')
        self.version = data.get('version')
        self.form_id = data.get('form_id')
        self.status = data.get('status')
        self.fetchtxt = data.get('fetch')
        self.flow_id = data.get('flow_id')
        self.node_id = data.get('node_id')
        self.nodes = data.get('game')
        self.children = []

    def save(self):
        db.session.add(self)
        db.session.commit()

    def getId(self):
        return self.id

    @staticmethod
    def get_all_forms():
        return FormModel.query.all()

    @staticmethod
    def get_formbyId(id):
        return FormModel.query.get(id)

    @staticmethod
    def get_formForVersion(formId):
        return FormModel.query.filter_by(form_id=formId).order_by(desc(FormModel.version))

    @staticmethod
    def get_FormForId(formId):
        return FormModel.query.filter_by(id=formId).order_by(desc(FormModel.version))

    def get_formForFlowAndNodeId(flowId,nodeId):
        return FormModel.query.filter_by(flow_id=flowId,node_id=nodeId).first()


    def __repr(self):
        return '<id {}>'.format(self.id)


class FormSchema(Schema):
    """
    Workflow Schema
    """

    class Meta:
        fields = ("id", "name", "version", "form_id", "status","fetchtxt", "nodes")

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    version = fields.Str(required=True)
    form_id = fields.Str(required=True)
    status = fields.Str(required=True)
    fetchtxt = fields.Str(required=False)
    flow_id = fields.Str(required=False)
    node_id = fields.Str(required=False)
    nodes = fields.Nested(FieldSchema,many=True)
    children = []
