#!/usr/bin/env python3

"""

Rest API server - 2020, Nien Huei Chang

rest_server.py - server

"""

import flask
import json


DATABASE_FILE_NAME = "rest.json"

database = []

app = flask.Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


def read_database_file():
    """ Read database from local json file """

    global database

    try:
        with open(DATABASE_FILE_NAME) as database_file:
            database = json.load(database_file)
            return True

    except (IOError, json.decoder.JSONDecodeError):
        return False


def write_database_file():
    """ Write database to local json file """

    try:
        with open(DATABASE_FILE_NAME, "w") as database_file:
            json.dump(database, database_file, indent=4)
            return True

    except IOError:
        return False


def db_list_records():
    """ Return list of the names from all records """

    return [record["name"] for record in database]


def db_add_record(record):
    """ Add new record to database """

    if record["name"] not in db_list_records():
        database.append(record)
        return True


def db_get_record(name):
    """ Get record from database """

    for record in database:
        if record["name"] == name:
            return record


def db_update_record(name, data):
    """ Update data in record """

    for record in database:

        if record["name"] == name:
            record.update(data)

            for key in list(record.keys()):
                if record[key] == "":
                    del record[key]

            return True


def db_delete_record(name):
    """ Delete record """

    for record in database:
        if record["name"] == name:
            del database[database.index(record)]
            return True


@app.before_first_request
def flask_init():
    read_database_file()


@app.route("/")
def flask_root():
    print("*** Displaying the webpage. ***")
    return flask.jsonify(database), 200


@app.route("/api/names", methods=["GET", "POST"])
def api_names():
    """ REST API handler for: providing list of records, adding new record """

    if flask.request.method == "GET":

        return flask.jsonify(db_list_records()), 200

    if flask.request.method == "POST":

        if type(flask.request.json) is not dict:
            return flask.jsonify({"message": "Received data is not properly formatted."}), 400

        if "name" not in flask.request.json.keys():
            return flask.jsonify({"message": "Received data does not contain 'name' key."}), 400

        if flask.request.json["name"] == "":
            return flask.jsonify({"message": "Received data contain empty 'name' key."}), 400

        if db_add_record(flask.request.json):
            write_database_file()
            return flask.jsonify(""), 200

        return flask.jsonify({"message": "Record containing the requested name already exists in database."}), 400


@app.route("/api/names/<name>", methods=["GET", "PUT", "DELETE"])
def api_names_name(name):
    """ REST API handler for: providing record, modifying record, deleting record - by name """

    if flask.request.method == "GET":

        record = db_get_record(name)

        if record:
            return flask.jsonify(record), 200

        return flask.jsonify({"message": "Record containing the requested name does not exist in database."}), 400

    if flask.request.method == "PUT":

        if type(flask.request.json) is not dict:
            return flask.jsonify({"message": "Received data is not properly formatted."}), 400

        if "name" in flask.request.json.keys() and flask.request.json["name"] == "":
            return flask.jsonify({"message": "Key 'name' cannot be empty."}), 400

        if db_update_record(name, flask.request.json):
            write_database_file()
            return flask.jsonify(""), 200

        return flask.jsonify({"message": "Record containing the requested name does not exist in database."}), 400

    if flask.request.method == "DELETE":

        if db_delete_record(name):
            write_database_file()
            return flask.jsonify(""), 200

        return flask.jsonify({"message": "Record containing the requested name does not exist in database."}), 400


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1")
