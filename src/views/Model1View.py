from flask import request, json, Response, Blueprint, render_template, jsonify
from ..models.Form_Builder_model_1 import Model_1,Model_1Schema

model1_api = Blueprint('model1_api', __name__)
model1_schema = Model_1Schema()

@model1_api.route('/', methods=['GET'])
def get_all():
    flows = Model_1.get_all_models()
    print('flows are',flows)
    ser_model = model1_schema.dump(flows,many=True)
    #return jsonify({'data':ser_model}), 200
    return custom_response(ser_model,200)


@model1_api.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    print("in create method request data is ",req_data)
    formModel = Model_1(req_data)
    formModel.save()
    return custom_response({'data':'saved'}, 200)


def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )