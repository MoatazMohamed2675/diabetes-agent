import os
import json
import joblib
import pandas as pd

# تحديد مسار الموديل نسبة لمكان الملف ده عشان ميحصلش FileNotFoundError عند باقي التيم
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "diabetes_model.joblib")

# تحميل الموديل مرة واحدة بس وقت استدعاء الملف عشان السرعة
try:
    _model = joblib.load(MODEL_PATH)
except Exception as e:
    _model = None
    _load_error = str(e)
else:
    _load_error = None


def _categorize_risk(probability: float) -> str:
    """تقسيم نسبة الاحتمالية لـ 3 فئات خطر واضحة."""
    if probability < 0.35:
        return "Low Risk"
    elif probability < 0.65:
        return "Moderate Risk"
    else:
        return "High Risk"


def predict_diabetes_risk(glucose: float, blood_pressure: float, bmi: float, age: float) -> str:
    """
    Predicts diabetes-related risk category using basic health measurements.

    Args:
        glucose (float): Plasma glucose concentration in mg/dL (valid range: 40 to 400).
        blood_pressure (float): Diastolic blood pressure in mm Hg (valid range: 30 to 200).
        bmi (float): Body Mass Index in kg/m^2 (valid range: 10 to 80).
        age (float): Age in years (valid range: 1 to 120).

    Returns:
        str: A JSON-formatted string containing risk category, probability,
             inputs used, and an educational disclaimer (or an error message).
    """
    # 1. التأكد إن الموديل اتحمل بنجاح
    if _model is None:
        return json.dumps({
            "status": "error",
            "error_type": "model_load_error",
            "message": f"Failed to load ML model: {_load_error}"
        }, indent=2)

    # 2. التحقق من إن المدخلات أرقام فعلاً (Input Type Validation)
    raw_inputs = {
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "BMI": bmi,
        "Age": age
    }

    parsed_inputs = {}
    for key, value in raw_inputs.items():
        if value is None or isinstance(value, bool):
            return json.dumps({
                "status": "error",
                "error_type": "missing_or_invalid_input",
                "message": f"Invalid or missing value for '{key}'. Please provide a valid number."
            }, indent=2)
        try:
            parsed_inputs[key] = float(value)
        except (ValueError, TypeError):
            return json.dumps({
                "status": "error",
                "error_type": "invalid_type",
                "message": f"'{key}' must be a numeric value, got '{value}'."
            }, indent=2)

    # 3. التحقق من المنطقية الطبية للأرقام (Range Validation)
    valid_ranges = {
        "Glucose": (40, 400),
        "BloodPressure": (30, 200),
        "BMI": (10, 80),
        "Age": (1, 120)
    }

    for key, (min_val, max_val) in valid_ranges.items():
        val = parsed_inputs[key]
        if not (min_val <= val <= max_val):
            return json.dumps({
                "status": "error",
                "error_type": "out_of_range",
                "message": f"'{key}' value ({val}) is out of realistic range ({min_val} to {max_val})."
            }, indent=2)

    # 4. تنفيذ التوقع وترجيع النتيجة كـ JSON منظم
    try:
        input_df = pd.DataFrame([parsed_inputs])
        prob = float(_model.predict_proba(input_df)[0][1])
        risk_category = _categorize_risk(prob)

        result = {
            "status": "success",
            "risk_category": risk_category,
            "risk_probability_percent": round(prob * 100, 2),
            "inputs_used": parsed_inputs,
            "disclaimer": "This is an educational risk estimate, not a medical diagnosis or treatment recommendation."
        }
        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "error_type": "prediction_error",
            "message": f"An unexpected error occurred during prediction: {str(e)}"
        }, indent=2)
