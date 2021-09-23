
from scrap_placa import *
from flask import Flask

app = Flask(__name__)


@app.route('/api/placa/<placa>', methods=['GET'])
def main(placa):
    response = get_information(placa)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
