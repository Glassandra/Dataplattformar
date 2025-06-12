from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route("/")
def data():
    image_url = url_for('static', filename='diagram1.png')
    return render_template('index.html', image_url=image_url)
@app.route("/analysis")
def analysis():
    return render_template('project.html')

if __name__== "__main__":
    app.run(debug=True)