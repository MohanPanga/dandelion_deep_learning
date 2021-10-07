import os
from flask import Flask, render_template, request, send_from_directory
from keras_preprocessing import image
from keras.models import load_model
from tensorflow.keras.models import Sequential
import numpy as np
import tensorflow as tf

app = Flask(__name__)

STATIC_FOLDER = 'static'
# Path to the folder where we'll store the upload before prediction
UPLOAD_FOLDER = STATIC_FOLDER + '/uploads'
# Path to the folder where we store the different models
MODEL_FOLDER = STATIC_FOLDER + '/models'


def load__model():
    """Load model once at running time for all the predictions"""
    print('[INFO] : Model loading ................')
    global model
    # model = tf.keras.models.load_model(MODEL_FOLDER + '/DandelionModel1.h5')
    # model = load_model(MODEL_FOLDER + '/DandelionModel1.h5')
    # model 2
    model = load_model(MODEL_FOLDER + '/DandelionModel2.h5')
    

    print('[INFO] : Model loaded')

# Home Page
@app.route('/')
def index():
    return render_template('index.html')


# Process file and predict label
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        file = request.files['image']
        fullname = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(fullname)

        # img = tf.keras.utils.load_img(
        # #must be same as what is in training model
        # fullname, target_size=(180, 180)
        # )
        # img_array = tf.keras.utils.img_to_array(img)
        # img_array = tf.expand_dims(img_array, 0) # Create a batch


# # Model 2
        img = tf.keras.utils.load_img(
        fullname, target_size=(540, 540)
)
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) 

        

        result = model.predict(img_array)[0]
        pred_prob=result[0]


# tightened specs to account for dandelion leaves in training set
        if pred_prob > .25:
            label = 'Not a Dandelion'
           
        else:
            label = 'Dandelion'
           

        return render_template('predict.html', image_file_name=file.filename, label=label)



@app.route('/upload/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


def create_app():
    load__model()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
