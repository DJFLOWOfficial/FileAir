import os
from flask import Flask, request, render_template, redirect, send_file
import random
import shutil

app = Flask(__name__)

@app.route('/')
def index():
    theme_cookie = request.cookies.get("theme")
    if theme_cookie is None:
        return render_template("index.html")
    elif theme_cookie == "light":
        return render_template("index_light.html")
    elif theme_cookie == "dark":
        return render_template("index_dark.html")
    elif theme_cookie == "auto":
        return render_template("index.html")
    else:
        return "Error"

@app.route('/upload')
def upload():
    return render_template("upload_test.html")

@app.route('/upload', methods=['GET', 'POST'])
def uploadpost():
    id = random.randint(1111111111, 9999999999)
    os.makedirs(f'./source/uploads/{id}')
    files = request.files.getlist('file')
    for file in files:
        file.save(f'./source/uploads/{id}/{file.filename}')

    shutil.make_archive(f"./source/uploads/{id}", "zip", root_dir=f"./source/uploads/{id}")

    shutil.rmtree(f'./source/uploads/{id}')

    return "finished1"

@app.route('/download')
def download():
    if request.args.get("id") is None:
        return redirect('/')
    if request.args.get("id"):
        if os.path.exists("./source/uploads/" + request.args.get("id") + ".zip"):
            theme_cookie = request.cookies.get("theme")
            if theme_cookie is None:
                return render_template("download.html", id = request.args.get("id"))
            elif theme_cookie == "light":
                return render_template("download_light.html", id = request.args.get("id"))
            elif theme_cookie == "dark":
                return render_template("download_dark.html", id = request.args.get("id"))
            elif theme_cookie == "auto":
                return render_template("download.html", id = request.args.get("id"))
            else:
                return "Error"
        else:
            return redirect('/')

@app.route('/getfile')
def getfile():
    if request.args.get("id") is None:
        return redirect('/')
    if request.args.get("id"):
        try:
            return send_file("uploads/"+ request.args.get("id") + ".zip", as_attachment=True)
        except:
            return redirect("/")



@app.route("/media")
def media():
    if request.args.get("file") is None:
        return render_template("404.html")
    else:
        try:
            file = str("media/"+request.args.get("file"))
            return send_file(file)
        except:
            return render_template("404.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)