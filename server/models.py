from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates, relationship
from datetime import date

db = SQLAlchemy()


class Exercise(db.Model):
    """Exercise model representing an exercise that can be added to workouts."""
    
    __tablename__ = 'exercises'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(db.String(100), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationships
    workout_exercises = relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    
    # Model Validations
    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty")
        if len(value) > 255:
            raise ValueError("Exercise name must be 255 characters or less")
        return value.strip()
    
    @validates('category')
    def validate_category(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise category cannot be empty")
        return value.strip()
    
    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    """Workout model representing a single workout session."""
    
    __tablename__ = 'workouts'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    
    # Relationships
    workout_exercises = relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    
    # Model Validations
    @validates('date')
    def validate_date(self, key, value):
        if value is None:
            raise ValueError("Workout date cannot be empty")
        if isinstance(value, str):
            value = date.fromisoformat(value)
        if value > date.today():
            raise ValueError("Workout date cannot be in the future")
        return value
    
    @validates('duration_minutes')
    def validate_duration_minutes(self, key, value):
        if value is None:
            raise ValueError("Duration minutes cannot be empty")
        if value <= 0:
            raise ValueError("Duration minutes must be greater than 0")
        if value > 1440:  # More than 24 hours
            raise ValueError("Duration minutes cannot exceed 1440 (24 hours)")
        return value
    
    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'


class WorkoutExercise(db.Model):
    """WorkoutExercise join table linking exercises to workouts with set/rep/duration data."""
    
    __tablename__ = 'workout_exercises'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    
    # Relationships
    workout = relationship('Workout', back_populates='workout_exercises')
    exercise = relationship('Exercise', back_populates='workout_exercises')
    
    # Table Constraints
    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),
    )
    
    # Model Validations
    @validates('reps')
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Reps must be greater than 0 if provided")
        return value
    
    @validates('sets')
    def validate_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Sets must be greater than 0 if provided")
        return value
    
    @validates('duration_seconds')
    def validate_duration_seconds(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Duration seconds must be greater than 0 if provided")
        return value
    
    def __init__(self, **kwargs):
        """Ensure at least one of reps, sets, or duration_seconds is provided."""
        super().__init__(**kwargs)
        if not any([self.reps, self.sets, self.duration_seconds]):
            raise ValueError("At least one of reps, sets, or duration_seconds must be provided")
    
    def __repr__(self):
        return f'<WorkoutExercise workout_id={self.workout_id} exercise_id={self.exercise_id}>'
