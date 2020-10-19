from flask import Flask, request, Response, jsonify

from controler import Controler

POST = 'POST'
API_VERSION = 'v1'

app = Flask(__name__)
control = Controler()


@app.route('/')
def hello_world():
    # TODO: @oran - add in index.html here!
    return jsonify({'landing page!'})


@app.route(f'{API_VERSION}/health/')
def health():
    return jsonify({'msg': 'I am healthy!'})


@app.route(f'{API_VERSION}/plot/<id>/')
def get_plot(id):
    """
    @type id: str
    @param id: unique filename
    """
    # Note: please check control.get_plots(..) for future implementation details
    return Response({'msg': 'not implemented'}, 501)


@app.route(f'{API_VERSION}/plot/', methods=[POST])
def create_plot():
    data = request.json
    # Mandatory field as part of the schema
    # TODO: @oran - if we server many future API's we should consider using Swagger now.
    # That way we will easily simplify the testing and schema between FE (client) and BE.
    ids = 'ids'
    if ids not in data:
        return Response(jsonify({'msg': 'Bad request, missing ids in payload'}), 400)

    app.logger.debug('received %s: %s', ids, data[ids])
    for filename in data[ids]:
        # TODO: @oran - add multiprocess to send the work to the controler
        # TODO: @oran - I need to get the status of each run of this method, use repsonse handler
        #       in multiprocess
        control.create_plot(filename)

    # TODO return a list of successful ids or partial success with HTTP 206 or failed
    # Better to use multiprocess with "202 Accepted", since it could be a long process.
    return Response(jsonify({'msg': 'created'}), 201)
