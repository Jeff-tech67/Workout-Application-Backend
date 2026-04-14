#!/usr/bin/env python3

from app import app
from models import *
from datetime import date, timedelta

def seed_database():
    """Seed the database with sample data."""
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        
        # Create exercises
        print("Creating exercises...")
        exercises = [
            Exercise(
                name="Push-ups",
                category="Upper Body",
                equipment_needed=False
            ),
            Exercise(
                name="Squat",
                category="Lower Body",
                equipment_needed=False
            ),
            Exercise(
                name="Bench Press",
                category="Upper Body",
                equipment_needed=True
            ),
            Exercise(
                name="Deadlift",
                category="Full Body",
                equipment_needed=True
            ),
            Exercise(
                name="Pull-ups",
                category="Upper Body",
                equipment_needed=False
            ),
            Exercise(
                name="Running",
                category="Cardio",
                equipment_needed=False
            ),
            Exercise(
                name="Plank",
                category="Core",
                equipment_needed=False
            ),
            Exercise(
                name="Dumbbell Curls",
                category="Upper Body",
                equipment_needed=True
            ),
        ]
        
        for exercise in exercises:
            db.session.add(exercise)
        db.session.commit()
        print(f"✓ Created {len(exercises)} exercises")
        
        # Create workouts
        print("Creating workouts...")
        today = date.today()
        workouts = [
            Workout(
                date=today - timedelta(days=7),
                duration_minutes=60,
                notes="Upper body day - felt strong"
            ),
            Workout(
                date=today - timedelta(days=5),
                duration_minutes=45,
                notes="Lower body day - good form on squats"
            ),
            Workout(
                date=today - timedelta(days=3),
                duration_minutes=30,
                notes="Cardio session - morning run"
            ),
            Workout(
                date=today - timedelta(days=1),
                duration_minutes=75,
                notes="Full body workout - strength focus"
            ),
            Workout(
                date=today,
                duration_minutes=50,
                notes="Core and cardio mix"
            ),
        ]
        
        for workout in workouts:
            db.session.add(workout)
        db.session.commit()
        print(f"✓ Created {len(workouts)} workouts")
        
        # Create workout exercises
        print("Creating workout-exercise associations...")
        
        # Workout 1 - Upper body
        we1 = WorkoutExercise(
            workout_id=1,
            exercise_id=1,  # Push-ups
            sets=3,
            reps=15
        )
        we2 = WorkoutExercise(
            workout_id=1,
            exercise_id=3,  # Bench Press
            sets=4,
            reps=8
        )
        we3 = WorkoutExercise(
            workout_id=1,
            exercise_id=8,  # Dumbbell Curls
            sets=3,
            reps=12
        )
        
        # Workout 2 - Lower body
        we4 = WorkoutExercise(
            workout_id=2,
            exercise_id=2,  # Squat
            sets=4,
            reps=10
        )
        we5 = WorkoutExercise(
            workout_id=2,
            exercise_id=4,  # Deadlift
            sets=3,
            reps=5
        )
        
        # Workout 3 - Cardio
        we6 = WorkoutExercise(
            workout_id=3,
            exercise_id=6,  # Running
            duration_seconds=1800
        )
        
        # Workout 4 - Full body
        we7 = WorkoutExercise(
            workout_id=4,
            exercise_id=5,  # Pull-ups
            sets=4,
            reps=8
        )
        we8 = WorkoutExercise(
            workout_id=4,
            exercise_id=2,  # Squat
            sets=3,
            reps=12
        )
        we9 = WorkoutExercise(
            workout_id=4,
            exercise_id=3,  # Bench Press
            sets=3,
            reps=10
        )
        
        # Workout 5 - Core and cardio
        we10 = WorkoutExercise(
            workout_id=5,
            exercise_id=7,  # Plank
            duration_seconds=300
        )
        we11 = WorkoutExercise(
            workout_id=5,
            exercise_id=6,  # Running
            duration_seconds=1200
        )
        
        workout_exercises = [
            we1, we2, we3, we4, we5, we6, we7, we8, we9, we10, we11
        ]
        
        for we in workout_exercises:
            db.session.add(we)
        db.session.commit()
        print(f"✓ Created {len(workout_exercises)} workout-exercise associations")
        
        print("\n✅ Database seeded successfully!")
        print(f"Total exercises: {Exercise.query.count()}")
        print(f"Total workouts: {Workout.query.count()}")
        print(f"Total workout-exercise associations: {WorkoutExercise.query.count()}")


if __name__ == '__main__':
    seed_database()
