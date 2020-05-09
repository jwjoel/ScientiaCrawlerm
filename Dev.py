from flask import Flask
from flask import request
from tableRequest.getTable import getTable
from basicAccount.bindUni import bind
from basicAccount.wxLogin import wxLogin

app = Flask(__name__)

@app.route('/')
def index():
    return '{"Status":200}'

app.register_blueprint(getTable)
app.register_blueprint(bind)
app.register_blueprint(wxLogin)

if __name__ == '__main__':

    app.run('0.0.0.0', port=80)