from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True,
)

models = {}
def init():
    with open("./models/classification.plk","rb") as f:
        models["classification"] = pickle.load(f)
init()

@app.route("/")
def index():
    return render_template("index.html")


# API
@app.route("/predict/", methods=["POST"])
def predict():

    classification_list = ["정치","경제","사회","생활/문화","세계","IT/과학"]
    model = models["classification"]

    if request.method == 'POST':
        sentence = request.values.get("sentence")

        predict_data = model.predict_proba([sentence])[0]

        result = {"status":200, "result":list(predict_data),
            "category":classification_list}
    else:
        result = {"status":201}

    return jsonify(result)







# $ gunicorn --reload dss:app
