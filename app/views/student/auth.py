from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
# import db model
from app.models.student import Student
from flask_login import login_user, logout_user, login_required
from app.utils.student.validate_email import validate_email
from app.utils.student.validate_password import validate_password
from app.utils.student.validate_name import validate_name

# sign up as a student
@app.route('/students/join',methods=['GET','POST'])
def student_signup():
    if request.method == 'POST':
            email = request.form.get('email')
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            password = request.form.get('password')
            user = Student.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
            name=fname+" "+lname

            if user: # if a user is found, we want to redirect back to signup page so user can try again
                flash('Already Registered, Try Login.')
                return redirect(url_for('student_login'))
            else:
                if validate_name(name) == True:
                    if validate_email(email) == True :
                        if validate_password(password) == True:
                            student = Student(email=email, name=name, password=generate_password_hash(password, method='sha256'))
                            # add the new user to the database
                            db.session.add(student)
                            db.session.commit()
                            flash('Registered Successfully, Login Now.', 'success')
                            return redirect(url_for('student_login'))
                        else:
                            flash('Please enter a valid Password.','error')
                            flash('Password must contain:')
                            flash('.Minimun 8 characters', 'success')
                            flash('.Atleast one capital case','success')
                            flash('.Atleast one numeric characters','success')
                            flash('.Atleast one special charecter','success')
                            flash('.No white spaces', 'success')
                            flash('.Should not start with numeric charecter.','success')
                    else:
                        if validate_password(password) == False:
                            flash('Please check the Email ID and Password.', 'error')
                            flash('Password must contain:')
                            flash('.Minimun 8 characters', 'success')
                            flash('.Atleast one capital case','success')
                            flash('.Atleast one numeric characters','success')
                            flash('.Atleast one special charecter','success')
                            flash('.No white spaces', 'success')
                            flash('.Should not start with numeric charecter.','success')
                        else:
                            flash('Please enter a valid Email ID.', 'error')
                else:
                    if validate_email(email) == False:
                        if validate_password(password) == False:
                            flash('Please check all the details', 'error')
                        else:
                            flash('Please check the Name (must not countain digit) and  Email ID', 'error')
                    else:
                        if validate_password(password) == True:
                            flash('Please check the Name (must not countain digit)', 'error')
                        else:
                            flash('Please check the Name (must not countain digit) and  Password', 'error')
                            flash('Password must contain:')
                            flash('.Minimun 8 characters', 'success')
                            flash('.Atleast one capital case','success')
                            flash('.Atleast one numeric characters','success')
                            flash('.Atleast one special charecter','success')
                            flash('.No white spaces', 'success')
                            flash('.Should not start with numeric charecter.','success')

    return render_template('home/student-signup.html')

# login as a student
@app.route('/students/login', methods=['GET','POST'])
def student_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        student = Student.query.filter_by(email=email).first()
        if not student or not check_password_hash(student.password, password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('student_login')) # if the user doesn't exist or password is wrong, reload the page
        else:
            # if the above check passes, then we know the user has the right credentials
            login_user(student, remember=remember)
            return redirect(url_for('student_dashboard'))
    
    return render_template('home/student-login.html', role="Student")

# log out a student
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


