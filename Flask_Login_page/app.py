from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'your_secret_key'



#sql Configuration

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' #database location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to suppress a warning message
db =  SQLAlchemy(app)

#Database model class ~single row within our db
class User(db.Model):
    #class variables 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(125),unique=True,nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)

    #class methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
#Home Routes
@app.route('/')
def index():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

#Login route
@app.route('/login',methods=['POST'])
def login():
    #collect info from the form
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    
    #check if its in the db /login the user
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', message="Invalid username or password")
    #Otherwise show home page redirecting to login page

#Registration
@app.route('/register',methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('index.html', message="Username already exists")
    #create new user
    new_user = User(username=username)
    new_user.set_password(password)
    #add to db
    db.session.add(new_user)
    db.session.commit()
    session['username'] = username
    return redirect(url_for('dashboard'))
#Dashboard
@app.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('index'))
    
#logout route
@app.route('/logout')
def logout():
    #its like a list data u have to pop it out of the session
    session.pop("username",None)
    return redirect(url_for('index'))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
