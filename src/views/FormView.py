from flask import request, json, Response, Blueprint,render_template
from ..models.FormModel import FormModel, FormSchema
from ..models.FieldModel import FieldModel,FieldSchema
from flask import redirect

form_api = Blueprint('form_api', __name__)
form_schema = FormSchema()


@form_api.route('/addForm/<flowId>/<nodeId>', methods=['GET'])
def addForm(flowId,nodeId):
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
    return render_template('new.html',flowId=flowId,nodeId=nodeId,form_id=form_id,mode='view')

@form_api.route('/', methods=['GET'])
def get_all():
    forms = FormModel.get_all_forms()
    print('forms are',forms[0].nodes)
    #ser_flow = workflow_schema.dump(flows,many=True)

    parent = {}
    for item in forms:
        if item.form_id == '0':
            parent[item.id] = item
            parent[item.id].children = []


    for child in forms:
        key = int(child.form_id)
        if key in parent:
            print('parent found',parent[key])
            parentFlow = parent[key]
            parent[key].children.append(child)
           # parent[key] = parentFlow

    for par in parent:
        print(parent[par] ,"::",parent[par].children)

    print('parent is ',parent)

    #ser_flow = workflow_schema.dump(parent, many=True)
    return render_template('formList.html',data=parent)
    # return custom_response({'data':parent}, 200)

@form_api.route('/viewForm/<int:id>')
def viewForm(id):
    return render_template('formbase.html',mode='view',form_id=id)

@form_api.route('/editForm/<int:id>')
def editForm(id):
    form = FormModel.get_formbyId(id)
    form_id = form.id
    print("form id is ", form_id)
    return render_template('formbase.html',mode='edit',id=id,form_id=form_id)

@form_api.route('/', methods=['POST'])
def create():
    req_data = request.get_json()
    print(req_data)
    print('*****************')
    nodes = req_data.get("game")
    form_id = req_data.get('form_id')
    flow_id = req_data.get('flow_id')
    if(flow_id == ''):
        flow_id = '0'
    node_id = req_data.get('node_id')
    if (node_id == ''):
        node_id = '0'
    if(form_id != '0'):
        wList = list(FormModel.get_formForVersion(form_id))
        listLen = len(wList)
        # len will be 0 for the first version
        if (listLen == 0):
            wList = list(FormModel.get_formForId(form_id))
            listLen = len(wList)
        if (listLen > 0):
            print("form from order_by is ", wList[0].id)
            print("form from order_by is ", wList[listLen - 1].id)
            version = int(wList[listLen - 1].version) + 1
            req_data['version'] = str(version)


    many = isinstance(req_data, list)
    i = 0
    parent = ''

    for node in nodes[:]:
        child = node
        nodes.remove(node)
        item = {}
        item["node_id"] = child.get("node_id")
        item["type"] = child.get("type")
        item["status"] = child.get("status")
        item["data"] = child
        item["parent"] = parent
        node = FieldModel(item)
        nodes.append(node)
        nodeId = child.get("node_id")
        if('circle' in nodeId) or ('diamond' in nodeId) or ('rect' in nodeId) or ('rrect' in nodeId):
            parent = nodeId
            print('parent is ',parent)

    print(req_data)

    formModel = FormModel(req_data)
    formModel.save()
    print('in create method data is saved', formModel.getId())

   #return redirect('http://localhost:5000/api/v1/flow/viewFlow/32', code=301)
    return custom_response({'id':formModel.getId()}, 200)
    #data,error = workflow_schema.load(json.dumps(req_data))


@form_api.route('/<int:id>', methods=['GET'])
def get_formById(id):
    form = FormModel.get_formbyId(id)
    print('form is ',form)
    if not form:
        return custom_response({'error': 'form not found'}, 404)

    ser_flow = form_schema.dump(form)
    return custom_response(ser_flow,200)


def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
