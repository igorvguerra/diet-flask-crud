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

    new_meal = Meal(name=data["name"], description=data["description"], date_time=date_time)

    db.session.add(new_meal)
    db.session.commit()

    return jsonify({"message" : "Meal sucessfully created.",
                    "meal": new_meal.to_dict()})

if __name__ == "__main__":
    app.run(debug=True)
