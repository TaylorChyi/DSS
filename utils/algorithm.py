from common.constants import *
from log.logger import log_function
from common.dosage import *

@log_function
def clincian_decision_system(age, weight, pregnant, allergy_or_interacting_medicine, morolide_needed, disease_or_impaired_organ):
    if pregnant == "Y":
        if morolide_needed == "Y":
            if 2 not in allergy_or_interacting_medicine:
                if disease_or_impaired_organ == "Y":
                    prescription = erythromycin_dosage(age)
                else:
                    prescription = erythromycin_concentrated_dosage(age)
            else:
                prescription = ""
        else:
            if 1 not in allergy_or_interacting_medicine:
                prescription = amoxicillin_dosage(age)
            else:
                prescription = ""            
    else:
        if age >= 18:
            if 4 not in allergy_or_interacting_medicine:
                prescription = doxycycline_dosage(age)
            elif 1 not in allergy_or_interacting_medicine:
                prescription = amoxicillin_dosage(age)
            elif 2 not in allergy_or_interacting_medicine:
                prescription = erythromycin_dosage(age)
            elif 3 not in allergy_or_interacting_medicine:
                prescription = clarithromycin_dosage(age, weight)
        else:
            if 1 not in allergy_or_interacting_medicine:
                prescription = amoxicillin_dosage(age)
            else:
                prescription = ""
    return prescription

@log_function
def clincian_decision_system_preference(choice, age, weight):
    if choice == "AMOXICILLINE":
        prescription = amoxicillin_dosage(age)
    elif choice == "ERYTHROMYCIN":
        prescription = erythromycin_dosage(age)
    elif choice == "CLARITHROMYCIN":
        prescription = clarithromycin_dosage(age, weight)
    else:
        prescription = doxycycline_dosage(age)
            
    return prescription

@log_function
def amoxicillin_dosage(age):
    if age < 1:
        return AMOXICILLIN_AGE_UNDER_1
    elif age >= 1 and age <= 4:
        return AMOXICILLIN_AGE_1_TO_4
    else:
        return AMOXICILLIN_AGE_4_AND_ABOVE

@log_function
def erythromycin_dosage(age):
    if age < 1:
        return ERYTHROMYCIN_AGE_UNDER_2
    elif age >=  1 and age <= 7:
        return ERYTHROMYCIN_AGE_2_TO_7
    else:
        return ERYTHROMYCIN_AGE_8_AND_ABOVE
    
@log_function
def erythromycin_concentrated_dosage(age):
    if age < 1:
        return ERYTHROMYCIN_AGE_UNDER_2_CONCENTRATED
    elif age >=  1 and age <= 7:
        return ERYTHROMYCIN_AGE_2_TO_7_CONCENTRATED
    else:
        return ERYTHROMYCIN_AGE_8_AND_ABOVE_CONCENTRATED
    
@log_function
def clarithromycin_dosage(age, weight):
    if age <= 11:
        if weight < 8:
            return CLARITHROMYCIN_AGE_11_AND_UNDER_WEIGHT_UNDER_8
        elif weight >= 8 and weight <= 11:
            return CLARITHROMYCIN_AGE_11_AND_UNDER_WEIGHT_8_TO_11
        elif weight >= 12 and weight <= 19:
            return CLARITHROMYCIN_AGE_11_AND_UNDER_WEIGHT_12_TO_19
        elif weight >= 20 and weight <= 29:
            return CLARITHROMYCIN_AGE_11_AND_UNDER_WEIGHT_20_TO_29
        elif weight >= 30 and weight <= 40:
            return CLARITHROMYCIN_AGE_11_AND_UNDER_WEIGHT_30_TO_40
        else:
            return CLARITHROMYCIN_AGE_11_AND_UNDER_WEIGHT_ABOVE_40
    else:
        return CLARITHROMYCIN_AGE_ABOVE_11

@log_function
def doxycycline_dosage(age):
    if age >= 12:
        return DOXYCYCLINE_AGE_12_AND_ABOVE
    else:
        return DOXYCYCLINE_AGE_UNDER_12
