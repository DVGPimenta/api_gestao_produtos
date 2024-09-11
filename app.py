from flask import Flask
from controllers.produtos_routes import produtos_page

app = Flask(__name__)
app.json.sort_keys = False
app.register_blueprint(produtos_page)


@app.route('/')
def rota_teste():
    return 'Hello'


if __name__ == '__main__':
    app.run(debug=True)
