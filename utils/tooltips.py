# utils/tooltips.py

MEDICAL_TERMS = {
    "Hemoglobin": "Protein in red blood cells that carries oxygen. Low = anemia",
    "CBC": "Complete Blood Count - checks all blood cells",
    "WBC": "White Blood Cells - fight infections in your body",
    "RBC": "Red Blood Cells - carry oxygen throughout body",
    "Platelets": "Tiny cells that help your blood clot when you bleed",
    "PCV": "Packed Cell Volume - percentage of red cells in blood",
    "MCV": "Mean Corpuscular Volume - size of your red blood cells",
    "MCH": "Mean Corpuscular Hemoglobin - hemoglobin amount per cell",
    "MCHC": "Mean Corpuscular Hemoglobin Concentration - hemoglobin concentration",
    "RDW": "Red cell Distribution Width - variation in red cell size",
    "Neutrophils": "Most common white blood cell - fights bacterial infections",
    "Lymphocytes": "White blood cells that fight viral infections",
    "Eosinophils": "White blood cells - fight allergies and parasites",
    "Monocytes": "White blood cells that clean up dead cells",
    "Basophils": "Rare white blood cells involved in inflammation",
    "Absolute Neutrophils": "Exact count of neutrophil cells in blood",
    "Absolute Lymphocytes": "Exact count of lymphocyte cells in blood",
    "Absolute Eosinophils": "Exact count of eosinophil cells in blood",
    "Absolute Monocytes": "Exact count of monocyte cells in blood",
    "Platelet Count": "Number of clotting cells in your blood",
    "Hypertension": "High blood pressure",
    "Glucose": "Blood sugar level",
    "Creatinine": "Waste product filtered by kidneys",
    "Cholesterol": "Fatty substance in blood - high levels are risky",
    "Differential Count": "Breakdown of different types of white blood cells",
    "Blood Indices": "Measurements that describe red blood cells",
}

def get_tooltips(text):
    found_terms = {}
    # Convert text to lowercase for comparison
    text_lower = text.lower()
    
    for term, definition in MEDICAL_TERMS.items():
        if term.lower() in text_lower:
            found_terms[term] = definition
    
    return found_terms