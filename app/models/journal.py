from app import db
#from sqlalchemy.sql import func

#book is inheriting from db.Model, 
class Journal(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    #time_created = db.Column(db.DateTime(timezone = True), server_default = func.now() )
    #time_updated = db.Column(db.DateTime(timezone = True), onupdate = func.now())
    design = db.Column(db.String)
    sub_design = db.Column(db.String)
    cut = db.Column(db.Boolean, default = True)
    complete = db.Column(db.Boolean, default = True)
    size = db.Column(db.String, default = "A6")
    dye = db.Column(db.String)
    dye_gradient = db.Column(db.Boolean, default = False)