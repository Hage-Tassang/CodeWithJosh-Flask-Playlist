from flask import Flask
from flask import render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# My App setup
app = Flask(__name__)
Scss(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# define a model
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer,default=0)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"<Task {self.id}>"
    
# create the database tables
with app.app_context():
        db.create_all()
    
#home page
#routes tell the app what to do when a user visits a specific URL
@app.route("/",methods = ["GET", "POST"])
def index():
    
    # add a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f'Error: {e}')
            return f"There was an issue adding your task {e}"
    
    #see all current tasks
    tasks = MyTask.query.order_by(MyTask.created).all()
    return render_template("index.html", tasks=tasks)
 #https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application   
#delete an item
@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"There was a problem deleting that task Error: {e}"

#edit an item
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"There was a problem updating that task Error: {e}"
    else:
        return render_template("edit.html", task=task)
    

#runner and debugger
if __name__ == "__main__":
    #create the database tables
    
    
    #run the app in debug mode on port 5000
    app.run(debug=True)