# Workout Tracking Application Backend

A RESTful API for fitness trainers to track and manage workout sessions and exercises. Built with Flask, SQLAlchemy, and Marshmallow.

## Overview

This backend API enables personal trainers to:
- Create and manage workout sessions with dates, durations, and notes
- Create and manage a reusable exercise library
- Track exercises within specific workouts with sets, reps, or duration metrics
- Ensure data integrity through comprehensive validations at multiple levels

## Technology Used

- **Framework**: Flask 2.2.2
- **Database**: SQLite with Flask-SQLAlchemy 3.0.3
- **Migrations**: Flask-Migrate 3.1.0
- **Serialization**: Marshmallow 3.20.1
- **Language**: Python 3.8+

## Project Structure

```
server/
├── app.py              # Flask application and all endpoints
├── models.py           # SQLAlchemy models (Exercise, Workout, WorkoutExercise)
├── schemas.py          # Marshmallow schemas for validation and serialization
├── seed.py             # Database seeding with sample data
├── migrations/         # Alembic migration files
└── app.db             # SQLite database (generated at runtime)
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Workout-Application-Backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r Pipfile
   # Or if using pipenv:
   pipenv install
   ```

4. **Navigate to server directory**
   ```bash
   cd server
   ```

5. **Run database migrations**
   ```bash
   flask db upgrade head
   ```

6. **Seed the database with sample data**
   ```bash
   python seed.py
   ```

## Running the Application

### Start the development server
```bash
cd server
source ../.venv/bin/activate  # Activate virtual environment if not already active
python app.py
```

The API will be available at `http://localhost:5555`

### Using Flask CLI
```bash
cd server
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## API Endpoints

### Workouts

#### List all workouts
```
GET /workouts
```
**Response**: Array of all workouts with their associated exercises

**Example Response**:
```json
[
  {
    "id": 1,
    "date": "2026-04-08",
    "duration_minutes": 60,
    "notes": "Upper body day - felt strong",
    "workout_exercises": [...]
  }
]
```

#### Get a specific workout
```
GET /workouts/<id>
```
**Parameters**: `id` (integer) - Workout ID

**Response**: Workout object with all associated exercises, sets, reps, and durations

**Example Response**:
```json
{
  "id": 1,
  "date": "2026-04-08",
  "duration_minutes": 60,
  "notes": "Upper body day - felt strong",
  "workout_exercises": [
    {
      "id": 1,
      "exercise_id": 1,
      "reps": 15,
      "sets": 3,
      "duration_seconds": null,
      "exercise": {
        "id": 1,
        "name": "Push-ups",
        "category": "Upper Body",
        "equipment_needed": false
      }
    }
  ]
}
```

#### Create a new workout
```
POST /workouts
Content-Type: application/json
```
**Request Body**:
```json
{
  "date": "2026-04-15",
  "duration_minutes": 45,
  "notes": "Morning session"
}
```

**Response**: Created workout object (HTTP 201)

#### Delete a workout
```
DELETE /workouts/<id>
```
**Parameters**: `id` (integer) - Workout ID

**Response**: Success message (HTTP 200)

**Note**: Deleting a workout also deletes all associated `WorkoutExercise` records

---

### Exercises

#### List all exercises
```
GET /exercises
```
**Response**: Array of all exercises

**Example Response**:
```json
[
  {
    "id": 1,
    "name": "Push-ups",
    "category": "Upper Body",
    "equipment_needed": false
  }
]
```

#### Get a specific exercise
```
GET /exercises/<id>
```
**Parameters**: `id` (integer) - Exercise ID

**Response**: Exercise object with all associated workouts

**Example Response**:
```json
{
  "id": 1,
  "name": "Push-ups",
  "category": "Upper Body",
  "equipment_needed": false,
  "workouts": [
    {
      "id": 1,
      "date": "2026-04-08",
      "duration_minutes": 60,
      "notes": "Upper body day - felt strong"
    }
  ]
}
```

#### Create a new exercise
```
POST /exercises
Content-Type: application/json
```
**Request Body**:
```json
{
  "name": "Squat",
  "category": "Lower Body",
  "equipment_needed": false
}
```

**Response**: Created exercise object (HTTP 201)

#### Delete an exercise
```
DELETE /exercises/<id>
```
**Parameters**: `id` (integer) - Exercise ID

**Response**: Success message (HTTP 200)

**Note**: Deleting an exercise also deletes all associated `WorkoutExercise` records

---

### Workout Exercises (Join Table Operations)

#### Add an exercise to a workout
```
POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
Content-Type: application/json
```
**Parameters**: 
- `workout_id` (integer) - ID of the workout
- `exercise_id` (integer) - ID of the exercise

**Request Body** (at least one of reps/sets/duration_seconds required):
```json
{
  "reps": 12,
  "sets": 3,
  "duration_seconds": null
}
```

**Response**: Created WorkoutExercise object (HTTP 201)

**Example Response**:
```json
{
  "id": 1,
  "workout_id": 1,
  "exercise_id": 1,
  "reps": 12,
  "sets": 3,
  "duration_seconds": null
}
```

---

## Data Validation

### Table-Level Constraints

1. **Exercise Name Uniqueness**: Exercise names must be unique in the database
2. **Workout-Exercise Uniqueness**: Each exercise can appear only once per workout (composite unique constraint on `workout_id` and `exercise_id`)

### Model-Level Validations

**Exercise**:
- `name`: Cannot be empty, max 255 characters
- `category`: Cannot be empty, max 100 characters

**Workout**:
- `date`: Cannot be empty, cannot be in the future, must be a valid date
- `duration_minutes`: Must be greater than 0, cannot exceed 1440 (24 hours)

**WorkoutExercise**:
- `reps`: Must be greater than 0 if provided
- `sets`: Must be greater than 0 if provided
- `duration_seconds`: Must be greater than 0 if provided
- At least one of `reps`, `sets`, or `duration_seconds` must be provided

### Schema-Level Validations

Same validations as model-level, enforced during request deserialization:
- Exercise name uniqueness
- Date not in future
- Duration ranges
- At least one metric (reps/sets/duration) required for WorkoutExercise

## Database Models

### Exercise
```python
id (Integer, Primary Key)
name (String, Unique, Required)
category (String, Required)
equipment_needed (Boolean, Default: False)
```

### Workout
```python
id (Integer, Primary Key)
date (Date, Required)
duration_minutes (Integer, Required)
notes (Text, Optional)
```

### WorkoutExercise (Join Table)
```python
id (Integer, Primary Key)
workout_id (Integer, Foreign Key → Workout.id)
exercise_id (Integer, Foreign Key → Exercise.id)
reps (Integer, Optional)
sets (Integer, Optional)
duration_seconds (Integer, Optional)
```

**Constraints**:
- `Unique(workout_id, exercise_id)`: Ensures each exercise appears once per workout

## Relationships

- **Exercise → WorkoutExercise**: One-to-Many (one exercise has many WorkoutExercise records)
- **Workout → WorkoutExercise**: One-to-Many (one workout has many WorkoutExercise records)
- **Exercise ↔ Workout**: Many-to-Many (through WorkoutExercise join table)

## Development

### Database Migrations

If you modify the models, create a new migration:
```bash
flask db migrate -m "Your migration message"
flask db upgrade head
```

### Reset Database

To reset the database and reseed with sample data:
```bash
rm server/app.db
flask db upgrade head
python seed.py
```

### Flask Shell

Interactive database exploration:
```bash
flask shell
```

Examples:
```python
# Get all exercises
Exercise.query.all()

# Find exercise by name
Exercise.query.filter_by(name='Push-ups').first()

# Get a workout with all its exercises
workout = Workout.query.get(1)
workout.workout_exercises

# Create a new exercise
ex = Exercise(name='Bench Press', category='Upper Body', equipment_needed=True)
db.session.add(ex)
db.session.commit()
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **200**: Success
- **201**: Created successfully
- **400**: Bad request (validation error)
- **404**: Resource not found
- **500**: Internal server error

Error responses include an `errors` field with validation details:
```json
{
  "errors": {
    "date": ["Workout date cannot be in the future"],
    "duration_minutes": ["Duration must be greater than 0"]
  }
}
```

## Sample Data

The `seed.py` file creates sample data including:
- 8 exercises across various categories (Upper Body, Lower Body, Cardio, Core, Full Body)
- 5 workout sessions with varied dates and durations
- 11 WorkoutExercise associations with sets, reps, and duration data

Run `python seed.py` to populate or refresh the database.

## Testing

To test endpoints manually, use curl or Postman:

```bash
# Get all workouts
curl http://localhost:5555/workouts

# Get a specific workout
curl http://localhost:5555/workouts/1

# Create a workout
curl -X POST http://localhost:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"date":"2026-04-15","duration_minutes":30,"notes":"Quick session"}'

# Create an exercise
curl -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name":"Lunges","category":"Lower Body","equipment_needed":false}'

# Add exercise to workout
curl -X POST http://localhost:5555/workouts/1/exercises/1/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"sets":3,"reps":12}'
```

## Future Enhancements

- Update endpoints for modifying existing workouts and exercises
- Authentication and authorization for individual trainers
- Performance metrics and workout analytics
- REST API pagination for large datasets
- More comprehensive test suite
- OpenAPI/Swagger documentation

## License

This project is provided for educational purposes as part of the Moringa School curriculum.
