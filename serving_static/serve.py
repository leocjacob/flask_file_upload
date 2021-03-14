import os
from flask import Flask, flash, request, redirect, render_template, jsonify
from werkzeug.utils import secure_filename
# creates a Flask application, named app
app = Flask(__name__)

#It will allow below 16MB contents only, you can change it
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# a route where we will display a welcome message via an HTML template
@app.route('/api/info',methods=['GET','POST'])
def api_info():
    data = {
                "data": [
                {
                    "id": "1",
                    "name": "John Q Public",
                    "position": "System Architect",
                    "salary": "$320,800",
                    "start_date": "2011/04/25",
                    "office": "Edinburgh",
                    "extn": "5421"
                },
                {
                    "id": "2",
                    "name": "Larry Bird",
                    "position": "Accountant",
                    "salary": "$170,750",
                    "start_date": "2011/07/25",
                    "office": "Tokyo",
                    "extn": "8422"
                }]
            }
    return jsonify(data)

@app.route('/process',methods= ['POST'])
def process():
    print(request.data)
    return request.data

@app.route("/")
def hello():
    projectTitle = "Project Title Here"
    return render_template('index.html', projectTitle=projectTitle)

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part','alert alert-danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading','alert alert-warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded','alert alert-success')
            return redirect('/')
        else:
            flash('Allowed file types are pdf','alert alert-warning')
            return redirect(request.url)



# run the application
if __name__ == "__main__":
    app.run(debug=True)