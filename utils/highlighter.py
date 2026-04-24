# utils/highlighter.py

import pandas as pd
import re

def highlight_abnormal(text):
    flagged = []

    # Define patterns to search with normal ranges
    tests = {
        "Hemoglobin":          (r"Hemoglobin[^\d]*(\d+\.?\d*)",      13.0, 17.0),
        "RBC Count":           (r"RBC count[^\d]*(\d+\.?\d*)",        4.5,  5.5),
        "PCV":                 (r"Packed Cell Volume[^\d]*(\d+\.?\d*)", 40, 50),
        "MCV":                 (r"Mean Corpuscular Volume[^\d]*(\d+\.?\d*)", 83, 101),
        "MCH":                 (r"MCH[^\d]*(\d+\.?\d*)",              27,   32),
        "MCHC":                (r"MCHC[^\d]*(\d+\.?\d*)",             32.5, 34.5),
        "RDW":                 (r"RDW[^\d]*(\d+\.?\d*)",              11.6, 14.0),
        "WBC Count":           (r"WBC count[^\d]*(\d+\.?\d*)",        4000, 11000),
        "Neutrophils":         (r"Neutrophils[^\d]*(\d+\.?\d*)",      50,   62),
        "Lymphocytes":         (r"Lymphocytes[^\d]*(\d+\.?\d*)",      20,   40),
        "Eosinophils":         (r"Eosinophils[^\d]*(\d+\.?\d*)",      0,    6),
        "Monocytes":           (r"Monocytes[^\d]*(\d+\.?\d*)",        0,    10),
        "Basophils":           (r"Basophils[^\d]*(\d+\.?\d*)",        0,    2),
        "Platelet Count":      (r"Platelet[^\d]*(\d+\.?\d*)",         150000, 410000),
        "Abs Neutrophils":     (r"Absolute Neutrophils[^\d]*(\d+\.?\d*)", 1500, 7500),
        "Abs Lymphocytes":     (r"Absolute Lymphocytes[^\d]*(\d+\.?\d*)", 1300, 3500),
        "Abs Eosinophils":     (r"Absolute Eosinophils[^\d]*(\d+\.?\d*)", 0, 500),
        "Abs Monocytes":       (r"Absolute Monocytes[^\d]*(\d+\.?\d*)", 200, 950),
        "Abs Basophils":       (r"Absolute Basophils[^\d]*(\d+\.?\d*)", 0, 300),
    }

    for test_name, (pattern, low, high) in tests.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                value = float(match.group(1))
                if value < low or value > high:
                    status = "🔴 HIGH" if value > high else "🔵 LOW"
                    flagged.append({
                        "Test": test_name,
                        "Your Value": value,
                        "Normal Range": f"{low} - {high}",
                        "Status": status
                    })
            except:
                continue

    if flagged:
        return pd.DataFrame(flagged)
    return pd.DataFrame()