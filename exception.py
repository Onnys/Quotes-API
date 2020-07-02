from flask import abort, jsonify

def has_data(object):
    if not object:
        abort(404)
    else:
        return object    

def has_request_data(object):
    if not object:
        abort(422)
    else:
        return object

def has_value(object):
    for i in object:
        if not i:
            abort(400)
    return True


