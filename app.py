from flask import Flask, redirect, request, render_template, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
import os.path

app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "32m54hwcon49s1kl6"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    connect_db(app)
    db.create_all()

debug = DebugToolbarExtension(app)

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))
# credit: MarredCheese at https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file
# is used to automatically update static files without having to hard refresh the browser for every change :D

@app.route("/")
def root():
    return render_template("root.html", last_updated=dir_last_updated("static"))


@app.route("/api/cupcakes", methods=["GET"])
def get_cupcakes():
    cupcakes = [serialize_cupcake(c) for c in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<int:id>", methods=["GET"])
def get_cupcake(id):
    cupcake = serialize_cupcake(Cupcake.query.get_or_404(id))
    return jsonify(cupcakes=cupcake)

@app.route("/api/cupcakes", methods=["POST"])
def all_cupcakes_post():
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json.get("image")
    if (image == ""):
        image = None
    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=serialize_cupcake(cupcake)), 201)

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    Cupcake.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'message': "deleted"})

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def patch_cupcake(id):
    cupcake = Cupcake.query.get(id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=serialize_cupcake(cupcake))

def serialize_cupcake(cupcake):
    """Returns a dictionary in place of a Cupcake Object"""
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }
