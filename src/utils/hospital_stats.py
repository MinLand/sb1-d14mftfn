from typing import Dict, List
from models.hospital import Hospital
from models.activity import Activity
from models.doctor import Doctor

class HospitalStats:
    @staticmethod
    def calculate_bio_usage(hospital_id: int, game_id: int) -> float:
        """Calculate biological drug usage percentage for a hospital"""
        doctors = Doctor.query.filter_by(hospital_id=hospital_id).all()
        if not doctors:
            return 0.0
            
        total_prescriptions = 0
        bio_prescriptions = 0
        
        for doctor in doctors:
            total = doctor.a_drug + doctor.d_drug + doctor.generic
            bio = doctor.a_drug + doctor.d_drug
            total_prescriptions += total
            bio_prescriptions += bio
            
        return (bio_prescriptions / total_prescriptions * 100) if total_prescriptions > 0 else 0

    @staticmethod
    def calculate_market_share(hospital_id: int, game_id: int, company: str) -> float:
        """Calculate market share for a specific company in a hospital"""
        doctors = Doctor.query.filter_by(hospital_id=hospital_id).all()
        if not doctors:
            return 0.0
            
        total_prescriptions = 0
        company_prescriptions = 0
        
        for doctor in doctors:
            total = doctor.a_drug + doctor.d_drug + doctor.generic
            company_rx = doctor.a_drug if company == 'A' else doctor.d_drug
            total_prescriptions += total
            company_prescriptions += company_rx
            
        return (company_prescriptions / total_prescriptions * 100) if total_prescriptions > 0 else 0