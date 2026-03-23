from flask import Flask, render_template, request
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline.predict_pipe import PredictPipeline


app = Flask(__name__)
pipeline = PredictPipeline()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        data = {
            "LIMIT_BAL": float(request.form.get("LIMIT_BAL", 0)),
            "AGE": int(request.form.get("AGE", 0)),

            "SEX": request.form.get("SEX"),
            "EDUCATION": request.form.get("EDUCATION"),
            "MARRIAGE": request.form.get("MARRIAGE"),

            "PAY_1": request.form.get("PAY_1"),
            "PAY_2": request.form.get("PAY_2"),
            "PAY_3": request.form.get("PAY_3"),
            "PAY_4": request.form.get("PAY_4"),
            "PAY_5": request.form.get("PAY_5"),
            "PAY_6": request.form.get("PAY_6"),

            "BILL_AMT1": float(request.form.get("BILL_AMT1", 0)),
            "BILL_AMT2": float(request.form.get("BILL_AMT2", 0)),
            "BILL_AMT3": float(request.form.get("BILL_AMT3", 0)),
            "BILL_AMT4": float(request.form.get("BILL_AMT4", 0)),
            "BILL_AMT5": float(request.form.get("BILL_AMT5", 0)),
            "BILL_AMT6": float(request.form.get("BILL_AMT6", 0)),

            "PAY_AMT1": float(request.form.get("PAY_AMT1", 0)),
            "PAY_AMT2": float(request.form.get("PAY_AMT2", 0)),
            "PAY_AMT3": float(request.form.get("PAY_AMT3", 0)),
            "PAY_AMT4": float(request.form.get("PAY_AMT4", 0)),
            "PAY_AMT5": float(request.form.get("PAY_AMT5", 0)),
            "PAY_AMT6": float(request.form.get("PAY_AMT6", 0)),
        }

        df = pd.DataFrame([data])

        try:
            prob = pipeline.predict(df)[0]

            result = {
                "probability": round(float(prob), 4),
                "risk": "High" if prob >= 0.5 else "Low"
            }

        except Exception as e:
            import traceback
            return f"<pre>{traceback.format_exc()}</pre>"

    return render_template("index.html", result=result)




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
