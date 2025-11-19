"""
Lightweight model for Vercel deployment to reduce bundle size
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LightweightCKDModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'age', 'bp_systolic', 'bp_diastolic', 'specific_gravity',
            'albumin', 'sugar', 'red_blood_cells', 'pus_cell',
            'bacteria', 'blood_glucose', 'blood_urea', 'serum_creatinine',
            'sodium', 'potassium', 'hemoglobin', 'packed_cell_volume',
            'white_blood_cell_count', 'red_blood_cell_count', 'hypertension',
            'diabetes_mellitus', 'coronary_artery_disease', 'appetite',
            'pedal_edema', 'anemia'
        ]
        logger.info("Lightweight CKD Model initialized")
    
    def predict_risk(self, patient_data):
        """Return default values to avoid loading heavy model on Vercel"""
        logger.info("Using lightweight prediction (no model loaded)")
        
        stage = self.calculate_ckd_stage(patient_data)
        
        return {
            'risk_percentage': 0,
            'stage': stage,
            'risk_level': 'Unknown - Model not loaded on Vercel',
            'feature_importance': [],
            'egfr': self.calculate_egfr(patient_data.get('age'), patient_data.get('serum_creatinine', 1.0), patient_data.get('gender', 'male'))
        }
    
    def prepare_features(self, data):
        features = []
        for feature_name in self.feature_names:
            if feature_name in data:
                features.append(float(data[feature_name]))
            else:
                features.append(0.0)
        return features
    
    def calculate_egfr(self, age, creatinine, gender):
        if creatinine <= 0:
            creatinine = 1.0
        
        if gender.lower() == 'female':
            egfr = 186 * (creatinine ** -1.154) * (age ** -0.203) * 0.742
        else:
            egfr = 186 * (creatinine ** -1.154) * (age ** -0.203)
        
        return round(egfr, 2)
    
    def calculate_ckd_stage(self, data):
        egfr = self.calculate_egfr(
            data.get('age', 50),
            data.get('serum_creatinine', 1.0),
            data.get('gender', 'male')
        )
        
        if egfr >= 90:
            return 1
        elif egfr >= 60:
            return 2
        elif egfr >= 30:
            return 3
        elif egfr >= 15:
            return 4
        else:
            return 5
    
    def get_risk_level(self, risk_percentage):
        if risk_percentage < 20:
            return 'Low'
        elif risk_percentage < 50:
            return 'Moderate'
        elif risk_percentage < 75:
            return 'High'
        else:
            return 'Critical'
    
    def predict_batch(self, patient_list):
        results = []
        for patient in patient_list:
            result = self.predict_risk(patient)
            result['patient_id'] = patient.get('patient_id', 'Unknown')
            result['patient_name'] = patient.get('patient_name', 'Unknown')
            results.append(result)
        return results

# Create a global instance
lightweight_model = LightweightCKDModel()