from src.Mobile_Price_Prediction.pipelines.prediction_pipeline import CustomData, PredictPipeline
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    if request.method == "GET":
        return render_template("prediction.html")
    else:
        data = CustomData(
            Ratings=float(request.form.get('Ratings')),
            RAM=float(request.form.get('RAM')),
            ROM=float(request.form.get('ROM')),
            Mobile_Size=float(request.form.get('Mobile_Size')),
            Primary_Cam=int(request.form.get('Primary_Cam')),
            Selfi_Cam=float(request.form.get('Selfie_Cam')),
            Battery_Power=int(request.form.get('Battery_Power')),
        )
        final_data = data.get_data_as_dataframe()
        
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_data)
        result = round(pred[0], 2)

        # Prepare data for the chart (example data)
        chart_data = {
            'feature_impact': [12, 19, 3, 5, 2, 3]  # This should reflect actual feature impacts
        }
        
        return render_template("result.html", final_result=result, chart_data=chart_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
