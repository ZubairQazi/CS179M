import os
import utils
from flask import Flask, abort, render_template, request, redirect, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.secret_key = "secretStuff"
app.config['UPLOAD_EXTENSIONS'] = ['.txt']
app.config['UPLOAD_PATH'] = 'uploads' 

@app.route("/")
def home():
    return render_template("home.html")

# Route for handling the login page logic
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        session['user'] = username
        return redirect('/dashboard')

    return render_template("login.html")


@app.route('/dashboard', methods = ['POST', 'GET'])
def dashboard():
    if 'user' in session:

        return render_template("dashboard.html", username=session['user'])

    return '<h1>You are not logged in.</h1>'
	
@app.route('/service', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      if f != '':
          file_ext = os.path.splitext(filename)[1]
          if file_ext not in app.config['UPLOAD_EXTENSIONS']:
              return "Invalid file", 400
          filePath = os.path.join(app.config['UPLOAD_PATH'],filename)
          f.save(filePath)
          openFile = open(filePath,'r')
          containers = []
          ship_grid = utils.create_ship_grid(8,12)
          utils.update_ship_grid(openFile,ship_grid,containers)
          ship_grid_flipped = ship_grid[::-1][:]
      option = request.form['services']
      if option == 'Transfer':
          return render_template('transferService.html',ship_grid=ship_grid_flipped, enumerate=enumerate)
      else:
          return render_template('balanceService.html',ship_grid=ship_grid_flipped, enumerate=enumerate)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')
