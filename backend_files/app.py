import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask application
superkart_api = Flask("SuperKart Sales Forecaster")

# Load the serialized pipeline (preprocessing + model)
model = joblib.load("superkart_model.joblib")

# Columns the model expects, in order
FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area", "Product_MRP",
    "Store_Size", "Store_Location_City_Type", "Store_Type", "Product_Id_char",
    "Store_Age_Years", "Product_Type_Category",
]


@superkart_api.get("/")
def home():
    """Health-check endpoint."""
    return "Welcome to the SuperKart Sales Forecasting API!"


@superkart_api.post("/v1/predict")
def predict_sales():
    """Online inference: predict sales for a single product-store record sent as JSON."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be a JSON object"}), 400

    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    sample = pd.DataFrame([{f: data[f] for f in FEATURES}])
    prediction = float(model.predict(sample)[0])
    return jsonify({"Predicted Sales": round(prediction, 2)})


@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    """Batch inference: predict sales for every row of an uploaded CSV file."""
    file = request.files.get("file")
    if file is None:
        return jsonify({"error": "Upload a CSV file using the form field 'file'"}), 400

    input_data = pd.read_csv(file)
    missing = [f for f in FEATURES if f not in input_data.columns]
    if missing:
        return jsonify({"error": f"Missing columns: {missing}"}), 400

    predictions = model.predict(input_data[FEATURES])
    # Key = row index, value = predicted sales
    output = {str(i): round(float(p), 2) for i, p in zip(input_data.index, predictions)}
    return jsonify(output)


if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860, debug=False)
