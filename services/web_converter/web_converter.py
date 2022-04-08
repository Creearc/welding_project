import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

import functions

ALLOWED_EXTENSIONS = set(['zip'])
path = 'files'  # path for files to save

if not os.path.exists(path):
    os.makedirs(path)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = path

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            r = filename.split('.')[-1]
            print(r)
            
            path_arg, name = functions.unzip(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            split = False
            if request.form['action'] in {'Разбить на слои','Разбить на слои и конвертировать в TP'}:
                output_path = functions.split_layers(path_arg, '')
                split = True
            if request.form['action'] in {'Конвертировать в TP','Разбить на слои и конвертировать в TP'}:
                output_path = functions.convert(path_arg, split)
            out = functions.zip(output_path, app.config['UPLOAD_FOLDER'], name)
            
            return redirect(url_for('uploaded_file',
                                    filename=out))
    return '''
    <!doctype html>
    <title>upload_and_download_files</title>
    <h1>Загрузите файл</h1>
    <form action="" method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit name=action value='Разбить на слои'>
        <input type=submit name=action value='Конвертировать в TP'>
        <input type=submit name=action value='Разбить на слои и конвертировать в TP'>
    </form>
    '''



from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):  
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
