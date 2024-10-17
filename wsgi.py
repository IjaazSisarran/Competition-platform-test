import click
from datetime import datetime
from flask.cli import AppGroup
from App.database import get_migrate
from App.main import create_app
from App.controllers import (
    create_student, get_all_students_json, register_for_competition, create_admin, get_all_admins_json, create_competition, get_all_competitions_json, import_results_from_file, get_all_results_json, update_competition_details, get_results_by_competition,  initialize)

# This commands file allow you to create convenient CLI commands for managing models and testing controllers

app = create_app()
migrate = get_migrate(app)

#This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')


#Student Commands


#Create a group for student commands
student_cli = AppGroup('student', help='Student object commands')

#Command to create a student
@student_cli.command("create", help="Creates a student")
@click.argument("username")
@click.argument("password")
@click.argument("first_name")
@click.argument("last_name")
@click.argument("email")
def create_student_command(username,password,first_name, last_name, email):
    student_id = create_student(username,password,first_name, last_name, email)
    print(f'Student {first_name} {last_name} created with ID {student_id}')

#Command to list all students
@student_cli.command("list", help="Lists students in the database")
@click.argument("format", default="string")
def list_students_command(format):
    students = get_all_students_json()
    
    if format == 'string':
        if not students:
            print("No students found.")
        else:
            for student in students:
                print(f"Student ID: {student['studentID']}, Name: {student['firstName']} {student['lastName']}, Email: {student['email']}")
    else:
        print(students)

#Command to register a student to a competition
@student_cli.command("registerCompetition", help="Registers a student for a competition")
@click.argument("student_id")
@click.argument("competition_id")
def register_competition_command(student_id, competition_id):
    register_for_competition(student_id, competition_id)

app.cli.add_command(student_cli)


#Admin Commands


#Create a group for admin commands
admin_cli = AppGroup('admin', help='Admin object commands')

#Command to create an admin
@admin_cli.command("create", help="Creates an admin")
@click.argument("username")
@click.argument("password")
@click.argument("first_name")
@click.argument("last_name")
@click.argument("email")
def create_admin_command(username,password,first_name, last_name, email):
    admin_id = create_admin(username,password,first_name, last_name, email)
    print(f'Admin {first_name} {last_name} created with ID {admin_id}')

#Command to list all admins
@admin_cli.command("list", help="Lists admins in the database")
@click.argument("format", default="string")
def list_admins_command(format):
    admins = get_all_admins_json()
    if format == 'string':
        for admin in admins:
            print(f"Admin ID: {admin['adminID']}, Name: {admin['firstName']} {admin['lastName']}, Email: {admin['email']}")
    else:
        print(admins)

#Command to import results from CSV file
@admin_cli.command("import", help="Imports results from a CSV file")
@click.argument("file_path")
def import_results_command(file_path):
    import_results_from_file(file_path)

# Command to create a competition
@admin_cli.command("createCompetition", help="Creates a competition")
@click.argument("name")
@click.argument("date")
@click.argument("status")
@click.argument("description")
@click.argument("admin_id")
def create_competition_command(name, date, status, description, admin_id):
    try:
        competition_id = create_competition(name, date, status, description, admin_id)
        print(f'Competition {name} created with ID {competition_id}')
    except Exception as e:
        print(f'Error creating competition: {e}')


#Command to Update details of a competition
@admin_cli.command("update_competition", help="Updates a competition in the database")
@click.argument("competition_id")
@click.argument("name")
@click.argument("date")
@click.argument("status")
def update_competition_command(competition_id, name, date, status):
    """Update competition details."""
    update_details = {}

    if name:
        update_details['name'] = name
    if date:
        try:
            update_details['date'] = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
    if status:
        update_details['status'] = status

    update_competition_details(competition_id, **update_details)

app.cli.add_command(admin_cli)


#Competition Commands


#Create a group for competition commands
competition_cli = AppGroup('competition', help='Competition object commands')

#Command to list all competitions
@competition_cli.command("list", help="Lists competitions in the database")
@click.argument("format", default="string")
def list_competitions_command(format):
    competitions = get_all_competitions_json() 
    if format == 'string':
        for comp in competitions:
            print(f"{comp['competitionID']}: {comp['title']} - {comp['date']} - {comp['competitionType']}") 
    else:
        print(competitions) 

app.cli.add_command(competition_cli)


#Results Commands

#Create a group for results commands
results_cli = AppGroup('results', help='Results object commands')

#Command to list all results 
@results_cli.command("list", help="Lists all results in the database")
@click.argument("format", default="string")
def list_results_command(format):
    results = get_all_results_json()  
    if not results:
        print("No results found.")
    else:
        for result in results:
            print(f"Result ID: {result['resultID']}, Competition ID: {result['competitionID']}, "
                  f"Student ID: {result['studentID']}, Score: {result['score']}, "
                  f"Completion Time: {result['completionTime']}, Ranking: {result['ranking']}")

#Command to list results for a specific competition
@results_cli.command("competition", help="Lists results for a specific competition by competitionID")
@click.argument("competition_id")
def list_results_for_competition_command(competition_id):
    results = get_results_by_competition(competition_id)  
    if not results:
        print(f"No results found for competition ID: {competition_id}")
    else:
        for result in results:
            print(f"Result ID: {result.resultID}, Student ID: {result.studentID}, "
                  f"Score: {result.score}, Completion Time: {result.completionTime}, "
                  f"Ranking: {result.ranking}")

app.cli.add_command(results_cli)