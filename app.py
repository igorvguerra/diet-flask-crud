from datetime import datetime
from flask import Flask, request, jsonify
from repository.database import db
from db_models.meal import Meal


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY'

db.init_app(app)

@app.route("/meals", methods=["POST"])
def create_meal():
    data = request.get_json()

    if not data:
        return jsonify({"message" : "Invalid data."}), 400
      
    date_time = datetime.now()

    new_meal = Meal(
        name=data["name"], 
        description=data["description"], 
        date_time=date_time, 
        diet=data.get("diet")
    )

    db.session.add(new_meal)
    db.session.commit()

    return jsonify({"message" : "Meal sucessfully created.",
                    "meal": new_meal.to_dict()})

@app.route("/meals", methods=["GET"])
def get_meals():
    meals = Meal.query.all()
    meals_list = [meal.to_dict() for meal in meals]
    return jsonify(meals_list)

@app.route("/meals/<int:meal_id>", methods=["GET"])
def get_meal(meal_id): 
    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({"message": "Meal not found."}), 404
    return jsonify(meal.to_dict())

@app.route("/meals/<int:meal_id>", methods=["DELETE"])
def delete_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({"message": "Meal not found."}), 404

    db.session.delete(meal)
    db.session.commit()

    return jsonify({"message": "Meal successfully deleted."})

@app.route("/meals/<int:meal_id>", methods=["PUT"])
def update_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({"message": "Meal not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid data."}), 400

    meal.name = data.get("name", meal.name)
    meal.description = data.get("description", meal.description)
    meal.date_time = datetime.now()
    if "diet" in data:
        meal.diet = data["diet"]

    db.session.commit()

    return jsonify({
        "message": "Meal successfully updated.",
        "meal": meal.to_dict()
    })

if __name__ == "__main__":
    app.run(debug=True)
