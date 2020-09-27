#Web app project - simple portfolio site with contact form that automatically sends resume
# and project library summary to requestor
# v01 - Frontend - HTML template site
# v02 - Backend -
# #     1) Python script to interact with html input forms
#       and saving contact form information to database.
#       2) check if email already exists in DB and alter index.html to display error message
#       3) if new email is used, commit changes
# v03 - <Pending> - automatic email
#

#Modules
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

#Initialize db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Membrillo1.@localhost/contact_collector'
db = SQLAlchemy(app)

#Define class for table structure
class Data(db.Model):
    __tablename__ = "data"  # this is a table name
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120), unique=True)
    website = db.Column(db.String(120), unique=True)
    comment = db.Column(db.String(120), unique=False)

    #Return the dictionary object
    def __repr__(self):
        return f'<user:{self.id} email:{self.email} name:{self.name} website:{self.website} comment:{self.comment}'


#Define the index route
@app.route("/")
def index():
    #render_template opens .html from templates folder
    return render_template("index.html",
                           text="Welcome")



# use a decorator for other sites; in this case /success which gets called after the POST method is executed
@app.route("/success", methods=['POST'])
#success is called from the action
# if a form calls POST - see contact-form in index.html
def success():
    if request.method == 'POST': #is true if html form has method="POST"

        # get content of form fields
        name = request.form["name"]
        website = request.form["website"]
        comment = request.form["comment"]
        email = request.form["mail"]

        #Get db object; select from data, where email is the email, if the count is 0,
        # this is a new email, we want to add it
        if db.session.query(Data).filter(Data.email == email).count() == 0:
            #input_records calls the Data class and passes the parameters, repr will build the return string
            input_records = Data(email=email, name=name, website=website, comment=comment)
            db.session.add(input_records) #append
            db.session.commit() #commit changes
            return render_template("success.html") #change to success.html webpage

    #if there are more than one row for the email address entered, this return gets executed;
    return render_template('index.html',
                           text="It looks like that email was already submitted.  Thank you!")

#To get the debug information in case of errors
if __name__ == '__main__':
    app.debug = True
    app.run()

#End | https://github.com/eabdiel