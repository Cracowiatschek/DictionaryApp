from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Camapign(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    person = db.Column(db.String(30), unique = False, nullable = True)
    lv1 = db.Column(db.String(20), unique = False, nullable = True)
    lv2 = db.Column(db.String(20), unique = False, nullable = True)
    rt = db.Column(db.Boolean, default = False)
    checked = db.Column(db.Boolean, default = False)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "person": self.person,
            "lv1": self.lv1,
            "lv2": self.lv2,
            "rt": self.rt,
            "checked": self.checked
        }
