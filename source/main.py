from flask import Flask, request, render_template, redirect, send_file

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
    return render_template("upload.html")

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