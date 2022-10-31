

from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.journal import Journal

journal_bp = Blueprint("journal_bp" , __name__, url_prefix = "/journal")


@journal_bp.route("", methods = [ "POST"])
def create_journal():
    
    request_body = request.get_json()
    #can I refator this? how to put in default values if none entered?
    new_journal = Journal(
        design = request_body["design"],
        sub_design = request_body["sub_design"],
        cut = request_body["cut"],
        complete = request_body["complete"],
        size = request_body["size"],
        dye = request_body["dye"],
        dye_gradient = request_body["dye_gradient"]
    )

    db.session.add(new_journal)
    db.session.commit()
    return {"id": new_journal.id}, 201
    
@journal_bp.route("", methods = ["GET"])
def read_all_journals():
    design_query = request.args.get("design")
    if design_query:
        journals = Journal.query.filter_by(design = design_query)
    else:
        journals = Journal.query.all()
    
    response = []
    for journal in journals:
        journal_dict = make_journal_dict(journal)
        response.append(journal_dict)
    return jsonify(response), 200  

@journal_bp.route("/<journal_id>", methods = ["GET"])
def get_one_journal(journal_id):
    journal = validate_journal(journal_id)
    journal_dict = make_journal_dict(journal)
    return journal_dict


@journal_bp.route("/<journal_id>", methods = ["PUT"])
def update_journal(journal_id):
    journal = validate_journal(journal_id)
    request_body = request.get_json()

    #refactor this to make smaller.
    #how can we make this so that the request body doesn't need to be the entire entry?? 
    if "design" not in request_body or \
        "sub_design" not in request_body or \
        "cut" not in request_body or \
        "complete" not in request_body or \
        "size" not in request_body or \
        "dye" not in request_body or \
        "dye_gradient" not in request_body:
            return jsonify({"message": "Request must include design, sub_design, cut, complete, size, dye, and dye_gradient"}), 400


    journal.design = request_body["design"]
    journal.sub_design = request_body["sub_design"]
    journal.cut = request_body["cut"]
    journal.complete = request_body["complete"]
    journal.size = request_body["size"]
    journal.dye = request_body["dye"]
    journal.dye_gradient = request_body["dye_gradient"]

    db.session.commit()

    return make_response(f"Journal #{journal_id} successfully updated"), 200


@journal_bp.route("/<journal_id>", methods = ["DELETE"])
def delete_journal(journal_id):
    journal = validate_journal(journal_id)
    db.session.delete(journal)
    db.session.commit()

    return make_response(f"Journal #{journal_id} successfully deleted")

def validate_journal(journal_id):
    try:
        journal_id = int(journal_id)
    except:
        abort(make_response({"message": f"Journal {journal_id} invalid"}, 400))
    journal = Journal.query.get(journal_id)
    if not journal:
        abort(make_response({"message":f"Journal {journal_id} not found"}, 404))

    return journal

def make_journal_dict(journal):
    """given a journal, return a dictionary with all the info for that journal."""
    journal_dict = {
            "id" : journal.id,
            "design" : journal.design,
            "sub_design" : journal.sub_design,
            "cut": journal.cut,
            "complete": journal.complete,
            "size": journal.size,
            "dye": journal.dye,
            "dye_gradient": journal.dye_gradient
        }
    return journal_dict

