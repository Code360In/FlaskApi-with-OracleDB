import cx_Oracle
import flask
from flask import request, jsonify


app = flask.Flask(__name__)
app.config["DEBUG"] = True


def makeDictFactory(cursor):
    columnNames = [d[0] for d in cursor.description]
    def createRow(*args):
       return dict(zip(columnNames, args))
    return createRow


@app.route('/')
def index():
    return flask.jsonify(response_value_1=1, response_value_2="value")


@app.route('/welcome', methods=['GET'])
def home():
    return '''
    <h1>API TESTE</h1>
    <p>FLASK É INCRIVEL</p>'''


@app.route('/api/kl/v1/closure/omspos', methods=['GET'])
def closurePos():

    orderid = request.args.get('orderid', default=1, type=int)

    query = f'''
SELECT       

*

FROM     

table    

WHERE   id = {orderid}
        '''
    conn = cx_Oracle.connect(user="user",
                             password="pass",
                             dsn="host",
                             encoding="UTF-8")

    cursor = conn.cursor()
    cursor.execute(query)
    cursor.rowfactory = makeDictFactory(cursor)
    result = cursor.fetchall()

    if result == None:
        return page_not_found()
    else:
        return jsonify(result)


@app.errorhandler(404)
def page_not_found():
    return "<h1>404</h1><p>Nem vi nada...</p>", 404

if __name__ == '__main__':
    app.run()
