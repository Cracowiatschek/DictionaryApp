from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Camapign(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    camp_name = db.Column(db.String(80), unique = True, nullable = True)
    person = db.Column(db.String(30), unique = False, nullable = True)
    lv1 = db.Column(db.String(20), unique = False, nullable = True)
    lv2_options = db.Column(db.String(256), unique = False, nullable = True, default="Brak")
    lv2 = db.Column(db.String(20), unique = False, nullable = True)
    lv3_options = db.Column(db.String(256), unique = False, nullable = True, default="Brak")
    lv3 = db.Column(db.String(20), unique = False, nullable = True)
    lv4_options = db.Column(db.String(256), unique = False, nullable = True, default="Brak")
    lv4 = db.Column(db.String(20), unique = False, nullable = True)
    succType = db.Column(db.String(3), unique = False, nullable = True)
    rt = db.Column(db.Boolean, default = False)
    checked = db.Column(db.Boolean, default = False)
    offline = db.Column(db.Boolean, default = False)
    wrong = db.Column(db.Boolean, default = False)
    saved = db.Column(db.Boolean, default = False)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "camp_name": self.camp_name,
            "person": self.person,
            "lv1": self.lv1,
            "lv2_options": self.lv2_options,
            "lv2": self.lv2,
            "lv3_options": self.lv3_options,
            "lv3": self.lv3,
            "lv4_options": self.lv4_options,
            "lv4": self.lv4,
            "succType": self.succType,
            "rt": self.rt,
            "checked": self.checked,
            "offline": self.offline,
            "wrong": self.wrong,
            "saved": self.saved
        }
