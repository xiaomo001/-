from flask import Flask, request
import time
import json

app = Flask(__name__)


@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        _txtName = '%s_%s.txt' % (request.remote_addr,
                                  time.strftime('%Y%m%d%H%M%S', time.localtime()))
        with open(_txtName, 'w', encoding='utf-8') as f:
            f.writelines(json.loads(request.data))
    return "GetVer OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)