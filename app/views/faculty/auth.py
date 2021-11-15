from flask import render_template, redirect, session, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import app, db
from app.models.faculty import Faculty
from app.utils.auth import validate_email, validate_name, validate_password

### Faculty SignUp View
@app.route('/faculty/join',methods=['GET','POST'])
def faculty_signup():
    if request.method == 'POST':
            email = request.form.get('email')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            password = request.form.get('password')
            # concatenate first name and last name
            name = first_name + ' ' + last_name

            if name and email and password and validate_name(name) and validate_email(email) and validate_password(password):
                user = Faculty.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
                if user: # if a user is found, we want to redirect back to signup page so user can try again
                    flash("User already exits!", 'error')
                else:
                    faculty = Faculty(email=email, name=name, password=generate_password_hash(password, method='sha256'))
                    faculty.role = "faculty"
                    # add the new faculty to the database
                    db.session.add(faculty)
                    db.session.commit()
                    return redirect(url_for('faculty_login'))
            else:
                if not name or not email or not password:
                    flash("Fill the Mandatory Fields", "error")
                if not validate_name(name):
                    flash("Enter a Valid Name","error")
                if not validate_email(email):
                    flash("Enter a Valid Email","error")
                if not validate_password(password):
                    flash("Enter a Valid Password","error")
    return render_template('home/faculty-signup.html')

### Faculty Login View
@app.route('/faculty/login', methods=['GET','POST'])
def faculty_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        if email and password :      
            faculty = Faculty.query.filter_by(email=email).first()
            if not faculty or not check_password_hash(faculty.password, password):
                flash('Invalid credentials!!')
                return redirect(url_for('faculty_login')) # if the user doesn't exist or password is wrong, reload the page
            else:
                # if the above check passes, then we know the user has the right credentials
                login_user(faculty, remember=remember)
                return redirect(url_for('faculty_dashboard'))
        else:
                if not email or not password:
                    flash("Fill the Mandatory Fields", "error")
    return render_template('home/faculty-login.html', role="Faculty")

### Faculty Logout View
@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('home'))


