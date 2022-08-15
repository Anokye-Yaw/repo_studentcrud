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
    return render_template('create.html')

if __name__ == "__main__":
   app.run(host='localhost', port=5000)