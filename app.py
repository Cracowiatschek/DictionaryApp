import json

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
    editable = ""


    if "campaign" in content.keys():
        content["campaign"] = [i for i in content["campaign"] if i.saved is False]
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

    if "editable" in content.keys():
        editable = content["editable"][session["min_id"]:session["max_id"]]
        print(editable, content["editable"])

    return render_template("index.html", navbar_class=navbar_class, campaigns=filter_campaign,
                           all_campaigns = all_campaigns, editable = editable)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    no_relation_fields = json.load(open("no_relation_fields.json", 'r', encoding = "utf-8"))
    lv_1 = json.load(open("relation_lv1_lv2.json", 'r', encoding = "utf-8"))
    lv_2 = json.load(open("relation_lv1_lv2.json", 'r', encoding = "utf-8"))
    lv_3 = json.load(open("relation_lv2_lv3.json", 'r', encoding = "utf-8"))
    lv_4 = json.load(open("relation_lv3_lv4.json", 'r', encoding = "utf-8"))

    if username == "admin" and password == "admin":
        session["person"] = no_relation_fields["person"]
        session["succType"] = no_relation_fields["succType"]
        session["lv_1"] = [i for i in lv_1]
        content["lv_2"] = lv_2
        content["lv_3"] = lv_3
        content["lv_4"] = lv_4
        session["logged_in"] = True
        session["loading"] = True
        session["pick_active"] = True
        session["data_active"] = True
        session["hasData"] = False
        session["page_size"] = 5

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
    session.pop("render_table", None)
    content.pop("editable", None)
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


@app.route("/pick-data", methods=["POST", "GET"])
def pick_data():
    action = request.args.get('action')
    data = request.args.get('data')

    for i,x in enumerate(content["campaign"]):
        content["campaign"][i].id = i+1

    for req in request.form:
        if req.isdigit():
            content["campaign"][int(req)-1].checked = True

    if request.form.get("filter-button"):
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
        for act_id in ["searchBatch", "searchRT", "searchPlaceholder"]:
            if act_id in session:
                session.pop(act_id)

        for act_id,camp in enumerate(content["campaign"]):
            content["campaign"][act_id].checked = False

    if action == 'check':
        if content["campaign"][int(data)-1].checked:
            content["campaign"][int(data)-1].checked = False
        else:
            content["campaign"][int(data)-1].checked = True

    if action == 'uncheck':
        content["campaign"][int(data)-1].checked = False

    if action == 'show':
        if session.get("pick_active"):
            session["pick_active"] = False
        else:
            session["pick_active"] = True

    if request.form.get("edit"):
        session["render_table"] = True
        if "editable" in content:
            campaign_names = [content["editable"][i].name for i, n in enumerate(content["editable"])]
            campaigns = [val for i, val in enumerate(content["campaign"]) if
                         content["campaign"][i].name not in campaign_names and content["campaign"][i].checked]
            content["editable"] += campaigns

        else:
            content["editable"] = [camp for i,camp in enumerate(content["campaign"]) if
                                   content["campaign"][i].checked]

        content["editable"] = content["editable"].copy()

        for act_id, camp in enumerate(content["editable"]):
            content["editable"][act_id].id = act_id
            if type(content["editable"][act_id].lv2_options) != list:
                if content["editable"][act_id].lv1 in content["lv_2"]:
                    content["editable"][act_id].lv2_options = content["lv_2"][content["editable"][act_id].lv1]
                else:
                    content["editable"][act_id].lv2_options = [content["editable"][act_id].lv2_options]

            if type(content["editable"][act_id].lv3_options) != list:
                if content["editable"][act_id].lv2 in content["lv_3"]:
                    content["editable"][act_id].lv3_options = content["lv_3"][content["editable"][act_id].lv2]
                else:
                    content["editable"][act_id].lv3_options = [content["editable"][act_id].lv3_options]

            if type(content["editable"][act_id].lv4_options) != list:
                content["editable"][act_id].lv4_options = [content["editable"][act_id].lv4_options]

        for act_id, camp in enumerate(content["campaign"]):
            content["campaign"][act_id].id = act_id+1

        for item in ["searchBatch", "searchRT", "searchPlaceholder"]:
            if item in session:
                session.pop(item)

        for i,camp in enumerate(content["campaign"]):
            content["campaign"][i].checked = False

        session["pick_active"] = False
        session["data_active"] = True
        session["page"] = 0
        session["min_page"] = 0
        session["min_id"] = 0
        session["max_id"] = min(len(content["editable"]), 5)

        if len(content["editable"]) % session["page_size"] == 0:
            session["max_page"] = len(content["editable"]) // session["page_size"]
        else:
            session["max_page"] = len(content["editable"]) // session["page_size"] + 1

        session["pages"] = list(range(session["max_page"]))

    return redirect(url_for("index"))

@app.route("/send-data", methods=["POST", "GET"])
def send_data():
    action = request.args.get('action')
    data = request.args.get('data')

    if request.form.get("clear"):
        content.pop("editable", None)
        session.pop("render_table", None)
        session["pick_active"] = True
        return redirect(url_for("index"))

    def update_changes(requests):
        for req in requests:
            if req.split('-')[0].isdigit():
                req_id = int(req.split('-')[0])

                camp_id = [i for i, x in enumerate(content["editable"]) if content["editable"][i].id == req_id][0]
                if "camp_name" in req:
                    if len(request.form.get(req)) != "":
                        content["editable"][camp_id].camp_name = request.form.get(req)

                if "person" in req:
                    if len(request.form.get(req)) != "":
                        content["editable"][camp_id].person = request.form.get(req)

                if "lv1" in req:
                    if len(request.form.get(req)) != "":
                        content["editable"][camp_id].lv1 = request.form.get(req)
                        content["editable"][camp_id].lv2_options = content["lv_2"][request.form.get(req)]

                if "lv2" in req:
                    if len(request.form.get(req)) != "":
                        content["editable"][camp_id].lv2 = request.form.get(req)
                        content["editable"][camp_id].lv3_options = content["lv_3"][request.form.get(req)]

                if "lv3" in req:
                    if len(request.form.get(req)) != "":
                        content["editable"][camp_id].lv3 = request.form.get(req)
                        content["editable"][camp_id].lv4_options = content["lv_4"][request.form.get(req)]

                if "lv4" in req:
                    if len(request.form.get(req)) != "":
                        content["editable"][camp_id].lv4 = request.form.get(req)

                if "succType" in req:
                    if len(request.form.get(req)) != "":
                        content["editable"][camp_id].succType = request.form.get(req)

    update_changes(request.form)

    if request.form.get("save"):
        update_changes(request.form)
        correct_state = 0
        for row in content["editable"]:
            row.wrong = False
            if row.offline is False:
                if (row.camp_name != "" and row.camp_name is not None and row.person in session["person"]
                        and row.lv1 in session["lv_1"] and row.lv2 in row.lv2_options
                        and row.lv3 in row.lv3_options and row.lv4 in row.lv4_options
                        and row.succType in session["succType"]):
                        pass
                else:
                    row.wrong = True
                    correct_state += 1

        if correct_state == 0:
            return render_template("save_data.html")
        else:
            return redirect(url_for("index"))



    if action == "offline":
        camp_id = [i for i, x in enumerate(content["editable"]) if content["editable"][i].id == int(data)][0]
        if content["editable"][camp_id].offline:
            content["editable"][camp_id].offline = False
        else:
            content["editable"][camp_id].offline = True

    if action == "show":
        if session.get("data_active"):
            session["data_active"] = False
        else:
            session["data_active"] = True


    if action == "page":
        if data.isdigit():
            session["page"] = int(data)
            session["min_id"] = session["page"] * session["page_size"]
            session["max_id"] = min(session["min_id"] + session["page_size"], len(content["editable"]))

        else:
            if data == "left" and session["page"] > session["min_page"]:
                session["page"] -= 1
            elif data == "right" and session["page"] < session["max_page"]:
                session["page"] += 1

    return redirect(url_for("index"))


@app.route("/save-data")
def save_data():
    session["render_table"] = False
    session["pick_active"] = True
    for i in content["editable"]:
        i.wrong = False
        if i.offline is False:
            i.saved = True
    content.pop("editable", None)
    return redirect(url_for("index"))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tworzy tabelę, jeśli jej nie ma
    app.run(debug=True)
