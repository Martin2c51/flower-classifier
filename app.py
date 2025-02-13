from flask import Flask, request, jsonify
from fastai.vision.all import *
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

# load the learner
learn = load_learner("./models/trained_model.pkl")
lyrics_gen = load_learner("./modelsfinal_lyric_gen.pkl")
classes = learn.data.classes


def predict_single(img_file):
    "function to take image and return prediction"
    prediction = learn.predict(load_image(img_file))
    probs_list = prediction[2].numpy()
    return {
        "category": classes[prediction[1].item()],
        "probs": {c: round(float(probs_list[i]), 5) for (i, c) in enumerate(classes)},
    }


# route for prediction
@app.route("/predict", methods=["POST"])
def predict():
    return jsonify(predict_single(request.files["image"]))


# route for lyrics generation
@app.route("/generate_lyrics", methods=["POST"])
def generate_lyrics():
    print(request)
    return jsonify(
        {
            "lyrics": lyrics_gen.predict(
                request.form["prompt"],
                int(request.form["word_count"]),
                temperature=0.85,
            )
        }
    )


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run()

