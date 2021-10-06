from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/course-details')
def course_details():
    return render_template('course-details.html')

@app.route('/faculty')
def faculty():
    return render_template('faculty.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/programs')
def programs():
    return render_template('programs.html')

@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@app.route('/students')
def students():
    return render_template('students.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')
    
if __name__ == '__main__':
    app.run(debug=True)
    