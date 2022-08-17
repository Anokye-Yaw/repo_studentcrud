from itertools import count
from flask import Flask, render_template, request, redirect
from models import db, StudentModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test1@localhost:5432/students'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()
    
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
       return render_template('create.html')

    if request.method == 'POST':
       # hobby variable stores an array
       hobby = request.form.getlist('hobbies')
       # hobbies variable covert hobby array into string
       hobbies = ",".join(map(str, hobby))
       first_name = request.form['first_name']
       last_name = request.form['last_name']
       email = request.form['email']
       password = request.form['password']
       gender = request.form['gender']
       hobbies = hobbies
       country = request.form['country']
       
       students = StudentModel(first_name=first_name, last_name=last_name, email=email, password=password, gender=gender, hobbies=hobbies,country=country)
       db.session.add(students)
       db.session.commit()
       return redirect('/')
@app.route('/')
def RetrieveList():
    students = StudentModel.query.all()
    return render_template('index.html', students=students)

@app.route('/<int:id>/edit', methods = ['GET', 'POST'])
def update(id):
    student = StudentModel.query.filter_by(id=id).first()
    
    if request.method == 'POST':
      if student:   
            # hobby variable stores an array
            hobby = request.form.getlist('hobbies')
            # hobbies variable covert hobby array into string
            hobbies = ",".join(map(str, hobby))
            student.first_name = request.form['first_name']
            student.last_name = request.form['last_name']
            student.email = request.form['email']
            student.password = request.form['password']
            student.gender = request.form['gender']
            student.hobbies = hobbies
            student.country = request.form['country']
            
            #student = StudentModel(first_name=first_name, last_name=last_name, email=email, password=password, gender=gender, hobbies=hobbies,country=country)
            #db.session.add(students)
            db.session.commit()
            return redirect('/')
      return f"Student with id ={id} does not exist" 
    else:
      return render_template('update.html', student = student)

@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    students = StudentModel.query.get_or_404(id)
    if request.method == 'POST':
       if students:    
          db.session.delete(students)
          db.session.commit()
          return redirect('/')
       abort(404)
    return render_template('delete.html')
    
    
if __name__ == "__main__":
   app.run(host='localhost', port=5000)