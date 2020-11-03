from flask import Flask,render_template
from flask_cors import CORS

from .config import app_config
from .models import db, bcrypt
from .models.FormModel import FormModel

from .views.FormView import form_api as form_blueprint

#https://www.codementor.io/@olawalealadeusi896/restful-api-with-python-flask-framework-and-postgres-db-part-1-kbrwbygx5


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    bcrypt.init_app(app)

    db.init_app(app)

    app.register_blueprint(form_blueprint, url_prefix='/api/v1/form')

    CORS(app)

    @app.route('/', methods=['GET'])
    def index():
        return render_template('formbase.html')
        # return render_template('')

    @app.route('/addForm/<flowId>/<nodeId>', methods=['GET'])
    def addform(flowId,nodeId):
        print(flowId)
        print(nodeId)

        #check if form already exist for given flowId and nodeId
        form = FormModel.get_formForFlowAndNodeId(flowId,nodeId)
        #check if form is null or not
        if(form != None):
            form_id = form.id
            print(form.id)
        else:
            form_id = ''
        return render_template('formbase.html',flowId=flowId,nodeId=nodeId,form_id=form_id)

    return app