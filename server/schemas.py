from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from datetime import date


class ExerciseSchema(Schema):
    """Schema for Exercise model with serialization and validation."""
    
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=255, error="Exercise name must be between 1 and 255 characters"),
            validate.Regexp(r'^[a-zA-Z0-9\s\-_()]+$', error="Exercise name contains invalid characters")
        ]
    )
    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100, error="Category must be between 1 and 100 characters")
    )
    equipment_needed = fields.Bool(dump_default=False)
    
    @validates('name')
    def validate_name_unique(self, value):
        """Validate that exercise name is unique (schema level)."""
        from models import Exercise
        existing = Exercise.query.filter_by(name=value).first()
        if existing:
            raise ValidationError("Exercise name must be unique")


class WorkoutExerciseDetailSchema(Schema):
    """Schema for WorkoutExercise model with nested exercise details."""
    
    id = fields.Int(dump_only=True)
    exercise_id = fields.Int()
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(Schema):
    """Schema for Workout model with validation."""
    
    id = fields.Int(dump_only=True)
    date = fields.Date(
        required=True,
        validate=validate.Range(
            error="Workout date cannot be in the future"
        )
    )
    duration_minutes = fields.Int(
        required=True,
        validate=[
            validate.Range(min=1, error="Duration must be greater than 0"),
            validate.Range(max=1440, error="Duration cannot exceed 1440 minutes (24 hours)")
        ]
    )
    notes = fields.Str(allow_none=True)
    workout_exercises = fields.Nested(WorkoutExerciseDetailSchema, many=True, dump_only=True)
    
    @validates('date')
    def validate_date_not_future(self, value):
        """Validate that the date is not in the future."""
        if value > date.today():
            raise ValidationError("Workout date cannot be in the future")


class WorkoutExerciseSchema(Schema):
    """Schema for WorkoutExercise model with validation."""
    
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1, error="Reps must be greater than 0 if provided")
    )
    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1, error="Sets must be greater than 0 if provided")
    )
    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1, error="Duration seconds must be greater than 0 if provided")
    )
    
    @validates_schema
    def validate_at_least_one_metric(self, data, **kwargs):
        """Ensure at least one of reps, sets, or duration_seconds is provided."""
        if not any([data.get('reps'), data.get('sets'), data.get('duration_seconds')]):
            raise ValidationError("At least one of reps, sets, or duration_seconds must be provided")


class ExerciseDetailSchema(Schema):
    """Schema for Exercise with associated workouts."""
    
    id = fields.Int(dump_only=True)
    name = fields.Str()
    category = fields.Str()
    equipment_needed = fields.Bool()
    workouts = fields.Nested(
        lambda: WorkoutSchema(only=['id', 'date', 'duration_minutes', 'notes']),
        many=True,
        dump_only=True
    )
