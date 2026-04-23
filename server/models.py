from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates, relationship
from datetime import date

db = SQLAlchemy()


class Exercise(db.Model):
    """Represents a type of exercise (e.g., push-ups, running)."""

    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(db.String(100), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    # Link to workouts through the join table
    workout_exercises = relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )

    # --- Validations ---
    @validates('name')
    def validate_name(self, _, value):
        value = (value or "").strip()
        if not value:
            raise ValueError("Exercise name can't be empty")
        if len(value) > 255:
            raise ValueError("Exercise name is too long (max 255 characters)")
        return value

    @validates('category')
    def validate_category(self, _, value):
        value = (value or "").strip()
        if not value:
            raise ValueError("Category can't be empty")
        return value

    def __repr__(self):
        return f"<Exercise {self.name}>"


class Workout(db.Model):
    """Represents a workout session done on a specific day."""

    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )

    # --- Validations ---
    @validates('date')
    def validate_date(self, _, value):
        if not value:
            raise ValueError("Workout date is required")

        if isinstance(value, str):
            value = date.fromisoformat(value)

        if value > date.today():
            raise ValueError("Workout date can't be in the future")

        return value

    @validates('duration_minutes')
    def validate_duration(self, _, value):
        if value is None:
            raise ValueError("Duration is required")

        if value <= 0:
            raise ValueError("Duration must be greater than 0")

        if value > 1440:
            raise ValueError("Duration can't exceed 24 hours")

        return value

    def __repr__(self):
        return f"<Workout {self.date}>"


class WorkoutExercise(db.Model):
    """Connects a workout with an exercise, including details like reps, sets, or duration."""

    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = relationship('Workout', back_populates='workout_exercises')
    exercise = relationship('Exercise', back_populates='workout_exercises')

    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),
    )

    # --- Validations ---
    @validates('reps')
    def validate_reps(self, _, value):
        if value is not None and value <= 0:
            raise ValueError("Reps must be greater than 0")
        return value

    @validates('sets')
    def validate_sets(self, _, value):
        if value is not None and value <= 0:
            raise ValueError("Sets must be greater than 0")
        return value

    @validates('duration_seconds')
    def validate_duration_seconds(self, _, value):
        if value is not None and value <= 0:
            raise ValueError("Duration must be greater than 0")
        return value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Make sure at least one metric is provided
        if not any([self.reps, self.sets, self.duration_seconds]):
            raise ValueError("Provide at least reps, sets, or duration")

    def __repr__(self):
        return f"<WorkoutExercise workout={self.workout_id}, exercise={self.exercise_id}>"