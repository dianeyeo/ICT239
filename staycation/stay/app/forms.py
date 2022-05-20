# flask_wtf is a Flask extension that provides a simple interface for creating WTForms
# it is also a great tool to help with validation
from flask_wtf import FlaskForm
# 'StringField' : is the base for most of the fields, usually represents <input type='text'>
# 'PasswordField' : is a StringField except its input type is <input type='password'>
# ^ the value that is accepted by the field is not rendered back to the browser like normal fields
# 'DateTimeField' : a text field that stores a datetime.datetime matching format
# 'FloatField' : a text field, except all input is coerced into a float, inputs with errors are ignored and will not be accepted as a value
from wtforms import StringField, PasswordField, DateTimeField, FloatField
# import validators to use on fields to ensure user submits valid data
from wtforms.validators import Email, Length, InputRequired


# Registration Form inherits from FlaskForm
class RegForm(FlaskForm):
    # create a field for users' email
    # users' email take on data type 'StringField'
    # email field has validators to ensure users input valid data
    # 'InputRequired' : email field cannot be empty, if left empty upon submission, prompts error message
    # 'Length(max=30)' : email field not more than 30 characters
    email = StringField('Email',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=30)])
    # create a field for users' password
    # users' password take on data type 'PasswordField'
    # password field has validators to ensure users input valid data
    # 'InputRequired' : password field cannot be empty
    # 'Length(min=5, max=30)' : password field must be at least 5 characters and not more than 20 characters
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=5, max=20)])
    # create a field for users' name
    # users' name take on data type 'StringField'
    # name field has no validators, it is not required to be filled out
    name = StringField('Name')
