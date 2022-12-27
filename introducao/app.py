from distutils.log import debug
from flask import Flask, request, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_maneger = LoginManager(app)

@login_maneger.user_loader
def current_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(84), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)

    def __str__(self) -> str:
        return self.name
    

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Unicode(124), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # user = db.relationship('User', backref='profiles')

    def __str__(self) -> str:
        return self.name

@app.route('/')
def index():
    users = User.query.all() # SELECT * FROM users;
    return render_template("users.html", users=users)

@app.route("/user/<int:id>")
def unique(id):
    user = User.query.get(id)
    return render_template("user.html", user=user)

@app.route('/user/delete/<int:id>')
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)