from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import db, Camapign

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.secret_key = 'supersecretkey'  # Klucz wymagany do obsługi sesji

content = {}

@app.route("/", methods=["GET", "POST"])
def index():

    navbar_class = "blue darken-2"

    if session.get("logged_in") is True:
        session["table"] = ""
        navbar_class = "green darken-2"

    if session.get("logged_in") is False:
        session.pop("loading", None)
        session.pop("hasData", None)
        navbar_class = "red darken-3"

    keys_storage = ""

    if "campaign" in content.keys():
        keys_storage = content["campaign"]

        # if len(keys_storage) > 0:
        #     for i, x in enumerate(keys_storage):
        #         print(keys_storage[i].lv1, keys_storage[i].name, keys_storage[i].rt)
    return render_template("index.html", navbar_class=navbar_class, campaigns=keys_storage)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "admin":
        session["logged_in"] = True
        session["loading"] = True
        session["hasData"] = False
        return redirect(url_for("index"))

    session["logged_in"] = False
    session.pop("loading", None)
    session.pop("hasData", None)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("loading", None)
    session.pop("hasData", None)
    session.pop("data", None)
    return redirect(url_for("index"))


@app.route("/get_data")
def get_data():
    # Pobierz dane z API
    camp = Camapign.query.all()
    # Zapisz w sesji jako JSON (lub lista)
    content["campaign"] = camp
    session["loading"] = False
    session["hasData"] = True

    return redirect(url_for("index"))


@app.route("/send-data-table", methods=["POST"])
def send_data_table():

    print(request.form)

    return redirect(url_for("index"))





if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tworzy tabelę, jeśli jej nie ma
    app.run(debug=True)
