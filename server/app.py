from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from functools import wraps
import json

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

migrate = Migrate(app, db)

db.init_app(app)


def handle_errors(f):
 
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)
        except Exception as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)
    return decorated_function


# Workout Endpoints 

@app.route('/workouts', methods=['GET'])
def get_workouts():
    
    from schemas import WorkoutSchema
    workouts = Workout.query.all()
    schema = WorkoutSchema(many=True)
    return make_response(jsonify(schema.dump(workouts)), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
   
    from schemas import WorkoutSchema
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    schema = WorkoutSchema()
    return make_response(jsonify(schema.dump(workout)), 200)


@app.route('/workouts', methods=['POST'])
@handle_errors
def create_workout():
    
    from schemas import WorkoutSchema
    data = request.get_json()
    schema = WorkoutSchema()
    
    
    errors = schema.validate(data)
    if errors:
        return make_response(jsonify({"errors": errors}), 400)
    
    # Load data and create workout
    workout_data = schema.load(data, partial=False)
    workout = Workout(**workout_data)
    db.session.add(workout)
    db.session.commit()
    
    return make_response(jsonify(schema.dump(workout)), 201)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """DELETE /workouts/<id> - Delete a workout and its associated exercises."""
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    
    db.session.delete(workout)
    db.session.commit()
    
    return make_response(jsonify({"message": "Workout deleted successfully"}), 200)


# Exercise Endpoints

@app.route('/exercises', methods=['GET'])
def get_exercises():
    
    from schemas import ExerciseSchema
    exercises = Exercise.query.all()
    schema = ExerciseSchema(many=True)
    return make_response(jsonify(schema.dump(exercises)), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
   
    from schemas import ExerciseSchema
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    schema = ExerciseSchema()
    return make_response(jsonify(schema.dump(exercise)), 200)


@app.route('/exercises', methods=['POST'])
@handle_errors
def create_exercise():
    """POST /exercises - Create a new exercise."""
    from schemas import ExerciseSchema
    data = request.get_json()
    schema = ExerciseSchema()
    
    # Validate input
    errors = schema.validate(data)
    if errors:
        return make_response(jsonify({"errors": errors}), 400)
    
    # Load data and create exercise
    exercise_data = schema.load(data, partial=False)
    exercise = Exercise(**exercise_data)
    db.session.add(exercise)
    db.session.commit()
    
    return make_response(jsonify(schema.dump(exercise)), 201)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """DELETE /exercises/<id> - Delete an exercise and its associated workouts."""
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    
    db.session.delete(exercise)
    db.session.commit()
    
    return make_response(jsonify({"message": "Exercise deleted successfully"}), 200)


# WorkoutExercise Endpoints 

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
@handle_errors
def add_exercise_to_workout(workout_id, exercise_id):
    """POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Add an exercise to a workout."""
    from schemas import WorkoutExerciseSchema
    
    # Verify workout and exercise exist
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    
    # Get request data
    data = request.get_json() or {}
    data['workout_id'] = workout_id
    data['exercise_id'] = exercise_id
    
    schema = WorkoutExerciseSchema()
    
    # Validate input
    errors = schema.validate(data)
    if errors:
        return make_response(jsonify({"errors": errors}), 400)
    
    # Load data and create workout exercise
    workout_exercise_data = schema.load(data, partial=False)
    workout_exercise = WorkoutExercise(**workout_exercise_data)
    db.session.add(workout_exercise)
    db.session.commit()
    
    return make_response(jsonify(schema.dump(workout_exercise)), 201)





# Error Handling

@app.errorhandler(404)
def not_found(error):
    """to handle the 404 errors."""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(500)
def internal_error(error):
    """to handle the 500 errors."""
    db.session.rollback()
    return make_response(jsonify({"error": "Internal server error"}), 500)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
