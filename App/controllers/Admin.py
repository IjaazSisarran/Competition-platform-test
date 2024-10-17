import csv
from datetime import datetime
from sqlalchemy import func
from App.controllers import Student
from App.models import Admin, Competition, Results
from App.models import db
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

# Function to create an admin
def create_admin(username, password, first_name, last_name, email):
    # Check if admin with the same email already exists
    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_admin:
        raise ValueError(f"An admin with email '{email}' already exists.")
    
    # Generate a unique adminID in the format 'A001', 'A002', etc.
    max_admin_id = db.session.query(func.max(Admin.adminID)).scalar()
    if max_admin_id is None:
        new_admin_id_number = 1
    else:
        new_admin_id_number = int(max_admin_id[1:]) + 1
    
    admin_id = f"A{new_admin_id_number:03d}"
    
    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password)

    # Create a new Admin object with the hashed password
    new_admin = Admin(
        username=username,
        password=hashed_password,
        firstName=first_name,
        lastName=last_name,
        email=email,
        adminID=admin_id
    )
    
    try:
        db.session.add(new_admin)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError(f"An error occurred while creating the admin with ID '{admin_id}'.")
    
    return admin_id

# Function to get an admin by adminID
def get_admin_by_id(admin_id):
    return Admin.query.filter_by(adminID=admin_id).first()

# Function to return all admins
def get_all_admins():
    return Admin.query.all()

# Function to return all admins as JSON
def get_all_admins_json():
    return [admin.to_dict() for admin in Admin.query.all()]

# Function to create a competition
def create_competition(name, date_str, status, description, admin_id):
    competition_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    admin = get_admin_by_id(admin_id)
    if not admin:
        raise ValueError(f"Admin with ID {admin_id} not found.")
    
    max_id = db.session.query(func.max(Competition.competitionID)).scalar()
    new_id_number = 1 if max_id is None else int(max_id[1:]) + 1
    competition_id = f"C{new_id_number:03d}"
    
    new_competition = Competition(
        competitionID=competition_id,
        title=name,
        date=competition_date,
        competitionType=status,
        description=description,
        adminID=admin_id  
    )
    
    db.session.add(new_competition)
    db.session.commit()
    
    return competition_id

# Function to update the details of a competition
def update_competition_details(competition_id, **kwargs):
    competition = Competition.query.get(competition_id)
    if competition is None:
        print(f"Competition with ID {competition_id} not found.")
        return
    
    for key, value in kwargs.items():
        setattr(competition, key, value)

    db.session.commit()
    print(f"Competition {competition_id} updated successfully.")

# Function to import results from a CSV file
# def import_results_from_file(file_path):
#     try:
#         with open(file_path, newline='') as csvfile:
#             reader = csv.DictReader(csvfile)
#             students_created = set() 

#             for row in reader:
#                 if 'studentID' in row:  
#                     student_id = row['studentID']
#                     username = row['username']
#                     password = row['password']
#                     first_name = row['first_name']
#                     last_name = row['last_name']
#                     email = row['email']

#                     existing_student = db.session.query(Student).filter_by(studentID=student_id).first()

#                     if existing_student is not None or student_id in students_created:
#                         new_student_id = generate_new_student_id()  
#                         student_id = new_student_id
#                         print(f"Student ID {row['studentID']} already exists, assigning new ID: {student_id}")

#                     new_student = Student(
#                         username=username,
#                         password=password,
#                         firstName=first_name,
#                         lastName=last_name,
#                         email=email,
#                         studentID=student_id  
#                     )
#                     db.session.add(new_student)
#                     students_created.add(student_id) 
#                     print(f"Created student with ID: {student_id}")

#                 if 'resultID' in row:
#                     result_id = row['resultID']

#                     if db.session.query(Results).filter_by(resultID=result_id).first() is not None:
#                         print(f"Skipping duplicate resultID: {result_id}")
#                         continue 

#                     competition_id = row['competitionID']
#                     score = int(row['score'])
#                     completion_time = row['completionTime']
#                     ranking = int(row['ranking'])
#                     competition_date = row['date']

#                     competition = db.session.query(Competition).filter_by(competitionID=competition_id).first()
#                     if competition is None:
#                         try:
#                             parsed_date = datetime.strptime(competition_date, "%Y-%m-%d").date()
#                         except ValueError:
#                             parsed_date = datetime.strptime("2024-01-01", "%Y-%m-%d").date()

#                         competition = Competition(
#                             competitionID=competition_id,
#                             title=row.get('name', 'Imported Competition'),
#                             date=parsed_date,
#                             description="Imported competition",
#                             competitionType=row.get('status', 'Closed'), 
#                             adminID=None  
#                         )
#                         db.session.add(competition)
#                         print(f"Imported new competition with ID: {competition_id}")

#                     result = Results(
#                         resultID=result_id,
#                         competitionID=competition_id,
#                         studentID=student_id,
#                         score=score,
#                         completionTime=completion_time,
#                         ranking=ranking
#                     )

#                     db.session.add(result)

#             db.session.commit()
#             print(f'Results and students imported from {file_path}')
#     except Exception as e:
#         print(f"An error occurred while importing results: {e}")


def import_results_from_file(file_path):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            students_created = set()  # Track newly created students within the session

            for row in reader:
                if 'studentID' in row and 'username' in row and 'password' in row:
                    student_id = row['studentID']
                    username = row['username']
                    password = generate_password_hash(row['password'])  # Hash the password
                    first_name = row.get('first_name', 'Unknown')
                    last_name = row.get('last_name', 'Unknown')
                    email = row.get('email', None)

                    # Check if the student already exists
                    existing_student = db.session.query(Student).filter_by(studentID=student_id).first()

                    if existing_student is not None or student_id in students_created:
                        student_id = generate_new_student_id()  # Generate a new ID if needed
                        print(f"Student ID {row['studentID']} already exists, assigning new ID: {student_id}")

                    # Create and add new student
                    new_student = Student(
                        username=username,
                        password=password,  # Use hashed password
                        firstName=first_name,
                        lastName=last_name,
                        email=email,
                        studentID=student_id
                    )
                    db.session.add(new_student)
                    students_created.add(student_id)

                # Process result only if 'resultID' exists
                if 'resultID' in row and 'competitionID' in row and 'score' in row:
                    result_id = row['resultID']

                    if db.session.query(Results).filter_by(resultID=result_id).first() is not None:
                        print(f"Skipping duplicate resultID: {result_id}")
                        continue

                    competition_id = row['competitionID']
                    score = int(row['score'])
                    completion_time = row.get('completionTime', '00:00:00')
                    ranking = int(row.get('ranking', 0))

                    # Create and add new result
                    result = Results(
                        resultID=result_id,
                        competitionID=competition_id,
                        studentID=student_id,
                        score=score,
                        completionTime=completion_time,
                        ranking=ranking
                    )
                    db.session.add(result)

            # Commit all changes once at the end
            db.session.commit()
            print(f'Results and students successfully imported from {file_path}')
    except Exception as e:
        print(f"An error occurred while importing results: {e}")
# Helper Function to generate a new unique student ID
def generate_new_student_id():
    last_student = db.session.query(Student).order_by(Student.studentID.desc()).first()
    if last_student is None:
        return "S001" 
    last_id = int(last_student.studentID[1:]) 
    new_id = f"S{str(last_id + 1).zfill(3)}" 
    return new_id
