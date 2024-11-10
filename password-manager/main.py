from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String
from flask import Flask, render_template, request
from wtforms import StringField, PasswordField, SubmitField, Form, BooleanField
from wtforms.validators import DataRequired, InputRequired




app = Flask(__name__)
app.config['SECRET_KEY'] = "your-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project-manager.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=False, nullable=False)
    password = Column(String(100), nullable=False)


with app.app_context():
    db.create_all()


class AddAccount(Form):
    email = StringField(label="Email", validators=[DataRequired()], render_kw={"placeholder": "Email "})
    password = PasswordField(label="Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
    add = SubmitField(label="Add")


@app.route("/", methods=["GET", "POST"])
def home():
    form = AddAccount(request.form)
    if request.method == "POST" and form.validate():
        user = User(
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        form.email.data = None
    return render_template("index.html", form=form)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
