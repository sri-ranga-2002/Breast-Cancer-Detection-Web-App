import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle
import re

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/predict',methods=['POST'])

@app.route('/predict',methods=['POST'])
@app.route('/predict',methods=['POST'])

@app.route('/predict', methods=['POST'])
def predict():
    input_features = [x for x in request.form.values()]

    # Check for valid input values
    for feature in input_features:
        if not re.match(r'^[0-9]+$', feature):
            return render_template('index.html', prediction_text='Invalid input. Please enter numeric values only.')

    input_features = [int(x) for x in input_features]

    if len(input_features) != 9:
        return render_template('index.html', prediction_text='Invalid input. Please provide all 9 features.')

    if any(f < 1 for f in input_features):
        return render_template('index.html', prediction_text='Invalid input. All features must be greater than or equal to 1.')

    features_value = [np.array(input_features)]
    features_name = ['clump_thickness', 'uniform_cell_size', 'uniform_cell_shape',
                     'marginal_adhesion', 'single_epithelial_size', 'bare_nuclei',
                     'bland_chromatin', 'normal_nucleoli', 'mitoses']

    df = pd.DataFrame(features_value, columns=features_name)
    output = model.predict(df)

    if output == 4:
        res_val = "Breast cancer"
    else:
        res_val = "No breast cancer"

    return render_template('index.html', prediction_text='Patient has {}'.format(res_val))

if __name__ == "__main__":
    app.run(port=8080)
