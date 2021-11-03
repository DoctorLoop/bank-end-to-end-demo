from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from pathlib import Path
import parse
from markupsafe import Markup

import prediction_model
from single_input_form import InputPredictionForm
from config import Config

config_obj = Config()

app = Flask(__name__)
Bootstrap(app)

app.config.from_object(config_obj)

@app.route("/")
def index():
    """
    Default entry point in absence of any requests
    :return: Flask render template object
    """
    predict_form = InputPredictionForm()
    return render_template('index.html', form=predict_form, message="")

@app.route("/", methods=['POST','GET'])
def upload_csv():
    """
    Entry point in presence of requests
    :return: Flask render template object
    """

    predict_form = InputPredictionForm()

    if "upload-submit" in request.form:

        uploaded_file = request.files['file']  # get the uploaded file
        if uploaded_file.filename != '':

            file_path = Path(app.config['UPLOAD_FOLDER']) / Path(uploaded_file.filename)  # set the file path
            uploaded_file.save(file_path)  # save uploaded csv to disk

            csv_data, missing_columns = parse.parse_csv(file_path)

            success_message, message_type = ("Upload success", 'success') if len(missing_columns) == 0 else (f"Partial upload success. Missing {len(missing_columns)} expected column{'s' if len(missing_columns)>1 else ''}: {missing_columns}", "warning")
            flash(Markup(success_message), message_type)
            return render_template('index.html', form=predict_form)

        flash(Markup('Invalid csv file'), 'danger')
        return render_template('index.html', form=predict_form, message="Upload Error")

    else:
        if request.method == 'POST':
            d = request.form.to_dict()
        else:
            d = request.args.to_dict()

        df, missing_columns = parse.form_as_dataframe(d)
        if len(missing_columns) > 0:
            prediction_message = ""
            success_message, message_type = (f"Prediction failure. Missing {len(missing_columns)} expected field{'s' if len(missing_columns)>1 else ''}: {', '.join(missing_columns)}", 'danger')

        else:
            predictions = prediction_model.predict_liklihood(df)
            prediction_message = f"Liklihood of subscription {round(predictions[0], 4)}" if len(predictions) > 0 else ""

            success_message, message_type = ("Prediction success", 'success') if len(predictions) > 0 else (f"Prediction failure. Unable to get predictions from model.", "danger")

        flash(Markup(success_message), message_type)
        return render_template('index.html', form=predict_form, prediction_likelihood_message=prediction_message)


if (__name__ == "__main__"):
    app.run(port=5000)
