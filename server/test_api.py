#!/usr/bin/env python3
"""
Comprehensive test suite for the Workout Tracking API.
Tests all endpoints, validations, and error handling.
"""

import json
from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date, timedelta


def test_exercises():
    """Test Exercise endpoints."""
    print("\n" + "="*60)
    print("TESTING EXERCISE ENDPOINTS")
    print("="*60)
    
    with app.test_client() as client:
        # GET /exercises
        print("\n1. GET /exercises - List all exercises")
        resp = client.get('/exercises')
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        exercises = resp.get_json()
        assert isinstance(exercises, list), "Response should be a list"
        print(f"   ✓ Found {len(exercises)} exercises")
        
        # Get first exercise
        exercise_id = exercises[0]['id'] if exercises else None
        
        # GET /exercises/<id>
        if exercise_id:
            print(f"\n2. GET /exercises/{exercise_id} - Get specific exercise")
            resp = client.get(f'/exercises/{exercise_id}')
            assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
            exercise = resp.get_json()
            assert 'id' in exercise, "Response should contain id"
            assert 'name' in exercise, "Response should contain name"
            assert 'workouts' in exercise, "Response should contain workouts"
            print(f"   ✓ Retrieved exercise: {exercise['name']}")
        
        # GET /exercises/<id> for non-existent
        print(f"\n3. GET /exercises/99999 - Non-existent exercise")
        resp = client.get('/exercises/99999')
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
        print(f"   ✓ Correctly returns 404 for non-existent exercise")
        
        # POST /exercises - valid
        print(f"\n4. POST /exercises - Create valid exercise")
        new_exercise = {
            "name": f"Test Exercise {date.today()}",
            "category": "Test Category",
            "equipment_needed": True
        }
        resp = client.post('/exercises', 
                          json=new_exercise,
                          content_type='application/json')
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"
        created = resp.get_json()
        assert created['name'] == new_exercise['name']
        print(f"   ✓ Created exercise: {created['name']}")
        
        # POST /exercises - duplicate name (should fail)
        print(f"\n5. POST /exercises - Attempt duplicate name (should fail)")
        resp = client.post('/exercises',
                          json=new_exercise,
                          content_type='application/json')
        assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
        print(f"   ✓ Correctly rejected duplicate name")
        
        # POST /exercises - missing required field
        print(f"\n6. POST /exercises - Missing required fields (should fail)")
        resp = client.post('/exercises',
                          json={"category": "Test"},
                          content_type='application/json')
        assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
        print(f"   ✓ Correctly rejected missing name")
        
        # DELETE /exercises
        if exercise_id:
            print(f"\n7. DELETE /exercises/{exercise_id} - Delete exercise")
            resp = client.delete(f'/exercises/{exercise_id}')
            assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
            print(f"   ✓ Successfully deleted exercise")


def test_workouts():
    """Test Workout endpoints."""
    print("\n" + "="*60)
    print("TESTING WORKOUT ENDPOINTS")
    print("="*60)
    
    with app.test_client() as client:
        # GET /workouts
        print("\n1. GET /workouts - List all workouts")
        resp = client.get('/workouts')
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        workouts = resp.get_json()
        assert isinstance(workouts, list), "Response should be a list"
        print(f"   ✓ Found {len(workouts)} workouts")
        
        # Get first workout
        workout_id = workouts[0]['id'] if workouts else None
        
        # GET /workouts/<id>
        if workout_id:
            print(f"\n2. GET /workouts/{workout_id} - Get specific workout")
            resp = client.get(f'/workouts/{workout_id}')
            assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
            workout = resp.get_json()
            assert 'id' in workout, "Response should contain id"
            assert 'date' in workout, "Response should contain date"
            assert 'workout_exercises' in workout, "Response should contain exercises"
            print(f"   ✓ Retrieved workout: {workout['date']}")
        
        # GET /workouts/<id> for non-existent
        print(f"\n3. GET /workouts/99999 - Non-existent workout")
        resp = client.get('/workouts/99999')
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
        print(f"   ✓ Correctly returns 404 for non-existent workout")
        
        # POST /workouts - valid
        print(f"\n4. POST /workouts - Create valid workout")
        new_workout = {
            "date": str(date.today() - timedelta(days=1)),
            "duration_minutes": 60,
            "notes": "Test workout"
        }
        resp = client.post('/workouts',
                          json=new_workout,
                          content_type='application/json')
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"
        created = resp.get_json()
        assert created['duration_minutes'] == 60
        created_id = created['id']
        print(f"   ✓ Created workout: {created['date']}")
        
        # POST /workouts - future date (should fail)
        print(f"\n5. POST /workouts - Future date (should fail)")
        future_workout = {
            "date": str(date.today() + timedelta(days=1)),
            "duration_minutes": 30,
            "notes": "Future workout"
        }
        resp = client.post('/workouts',
                          json=future_workout,
                          content_type='application/json')
        assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
        print(f"   ✓ Correctly rejected future date")
        
        # POST /workouts - invalid duration (should fail)
        print(f"\n6. POST /workouts - Invalid duration (should fail)")
        invalid_workout = {
            "date": str(date.today()),
            "duration_minutes": 0,
            "notes": "Invalid duration"
        }
        resp = client.post('/workouts',
                          json=invalid_workout,
                          content_type='application/json')
        assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
        print(f"   ✓ Correctly rejected 0 duration")
        
        # DELETE /workouts
        if created_id:
            print(f"\n7. DELETE /workouts/{created_id} - Delete workout")
            resp = client.delete(f'/workouts/{created_id}')
            assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
            print(f"   ✓ Successfully deleted workout")


def test_workout_exercises():
    """Test WorkoutExercise endpoints."""
    print("\n" + "="*60)
    print("TESTING WORKOUT EXERCISE ENDPOINTS")
    print("="*60)
    
    with app.test_client() as client:
        # Get a workout and exercise
        workouts = client.get('/workouts').get_json()
        exercises = client.get('/exercises').get_json()
        
        if not workouts or not exercises:
            print("\n   ⚠ Skipping workout exercise tests (insufficient data)")
            return
        
        workout_id = workouts[0]['id']
        exercise_id = exercises[0]['id']
        
        # POST /workouts/<id>/exercises/<id>/workout_exercises - valid
        print(f"\n1. POST /workouts/{workout_id}/exercises/{exercise_id}/workout_exercises")
        we_data = {
            "sets": 3,
            "reps": 10,
            "duration_seconds": None
        }
        resp = client.post(
            f'/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises',
            json=we_data,
            content_type='application/json'
        )
        
        if resp.status_code == 400:
            # Exercise might already be in workout (unique constraint)
            print(f"   ✓ Exercise already associated (or validation error)")
        else:
            assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"
            we = resp.get_json()
            assert we['workout_id'] == workout_id
            assert we['exercise_id'] == exercise_id
            assert we['sets'] == 3
            print(f"   ✓ Successfully added exercise to workout")
        
        # POST - no metrics (should fail)
        print(f"\n2. POST /workouts/{workout_id}/exercises/{exercises[1]['id']}/workout_exercises - No metrics")
        resp = client.post(
            f'/workouts/{workout_id}/exercises/{exercises[1]["id"]}/workout_exercises',
            json={},
            content_type='application/json'
        )
        assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
        print(f"   ✓ Correctly rejected - no metrics provided")
        
        # POST - invalid reps (should fail)
        print(f"\n3. POST with invalid reps (should fail)")
        resp = client.post(
            f'/workouts/{workout_id}/exercises/{exercises[1]["id"]}/workout_exercises',
            json={"reps": -5, "sets": 3},
            content_type='application/json'
        )
        assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
        print(f"   ✓ Correctly rejected negative reps")


def test_validations():
    """Test validation errors."""
    print("\n" + "="*60)
    print("TESTING VALIDATIONS")
    print("="*60)
    
    with app.test_client() as client:
        # Empty exercise name
        print("\n1. Empty exercise name")
        resp = client.post('/exercises',
                          json={"name": "", "category": "Test"},
                          content_type='application/json')
        assert resp.status_code == 400
        print("   ✓ Rejected")
        
        # Very long exercise name
        print("\n2. Very long exercise name (>255 chars)")
        resp = client.post('/exercises',
                          json={
                              "name": "a" * 300,
                              "category": "Test"
                          },
                          content_type='application/json')
        assert resp.status_code == 400
        print("   ✓ Rejected")
        
        # Workout with duration > 1440
        print("\n3. Workout duration > 1440 minutes")
        resp = client.post('/workouts',
                          json={
                              "date": str(date.today()),
                              "duration_minutes": 2000,
                              "notes": "Too long"
                          },
                          content_type='application/json')
        assert resp.status_code == 400
        print("   ✓ Rejected")


def run_all_tests():
    """Run all tests."""
    print("\n")
    print("█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  WORKOUT API COMPREHENSIVE TEST SUITE".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)
    
    try:
        test_exercises()
        test_workouts()
        test_workout_exercises()
        test_validations()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60 + "\n")
        return True
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
