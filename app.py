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

    filter_campaign = ""
    all_campaigns = ""
    if "campaign" in content.keys():
        filter_campaign = content["campaign"]
        all_campaigns = content["campaign"]
        # for i,x in enumerate(filter_campaign):
        #     print(filter_campaign[i])
        if "searchPlaceholder" in session:
            filter_campaign = [camp for i,camp in enumerate(filter_campaign) if
                            session.get("searchPlaceholder").upper() in filter_campaign[i].name.upper()]

        if "searchRT" in session or "searchBatch" in session:
            if "searchRT" in session and "searchBatch" in session:
                pass
            elif "searchRT" in session:
                filter_campaign = [camp for i, camp in enumerate(filter_campaign) if
                                filter_campaign[i].rt is True]
            elif "searchBatch" in session:
                filter_campaign = [camp for i, camp in enumerate(filter_campaign) if
                                filter_campaign[i].rt is False]

    return render_template("index.html", navbar_class=navbar_class, campaigns=filter_campaign,
                           all_campaigns = all_campaigns)


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


@app.route("/send-data", methods=["POST", "GET"])
def send_data():
    action = request.args.get('action')
    data = request.args.get('data')

    for req in request.form:
        if req.isdigit():
            content["campaign"][int(req)-1].checked = True

    if request.form.get("filter-button"):
        print()
        if request.form.get("filter"):
            session["searchPlaceholder"] = request.form.get("filter")

        if request.form.get("rt"):
            session["searchRT"] = request.form.get("rt")
        else:
            if "searchRT" in session:
                session.pop("searchRT")

        if request.form.get("batch"):
            session["searchBatch"] = request.form.get("batch")
        else:
            if "searchBatch" in session:
                session.pop("searchBatch")

    if request.form.get("clear"):
        for i in ["searchBatch", "searchRT", "searchPlaceholder"]:
            if i in session:
                session.pop(i)
                print(i)

        for i,camp in enumerate(content["campaign"]):
            content["campaign"][i].checked = False

    if action == 'check':
        if content["campaign"][int(data)-1].checked:
            content["campaign"][int(data)-1].checked = False
        else:
            content["campaign"][int(data)-1].checked = True

    if action == 'uncheck':
        content["campaign"][int(data)-1].checked = False


    if request.form.get("edit"):
        session["render_table"] = True

    return redirect(url_for("index"))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tworzy tabelę, jeśli jej nie ma
    app.run(debug=True)
