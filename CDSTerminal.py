from utils.algorithm import *
from common.constants import *
from utils import dispose
from common.config import *
from utils import csv_util
from log.logger import *

SINGLE_LINE = 1
DOUBLE_LINE = 2

@log_function
def get_patient_input(prompt):
    user_input = input(prompt).strip().lower()
    def if_exit():
        if user_input in {"q", "exit"}:
            dispose.remove_pycache(ROOT_PATH)
            sys.exit()
    
    if_exit()
    new_prompt = True
    
    if EXIT_PROMPT == prompt:
        while True:
            
            if user_input in {"q", "exit", "r"} or not user_input:
                return user_input
            else:
                clear_lines_and_print(SINGLE_LINE if new_prompt else DOUBLE_LINE, "== Type 'q', 'exit', 'r', or press 'Enter' to proceed ==" + ENTER)
                new_prompt = False
                user_input = input(prompt).strip().lower()
                continue
    if ALLERGY_PROMPT == prompt:
        while True:
            parts = user_input.split('/')

            if not user_input:
                return []
            
            # 判断所有子字符串都是1-4的数字
            if all(part.isdigit() and 1 <= int(part) <= 4 for part in parts):
                # 去重
                unique_parts = set(int(part) for part in parts)
                return list(unique_parts)
            else:
                clear_lines_and_print(5 if new_prompt else 6, "== Please enter a valid choice number [1-4] and separate with '/' ==" + ENTER)
                new_prompt = False
                user_input = input(prompt).strip().lower()
                if_exit()
                continue
            
    if PREGNANT_PROMPT == prompt or MOROLIDE_PROMPT == prompt or DISEASE_PROMPT == prompt:
        while True:            
            if user_input in {"yes", "y"}:
                return "Y"
            elif user_input in {"no", "n"}:
                return "N"
            else:
                clear_lines_and_print(SINGLE_LINE if new_prompt else DOUBLE_LINE, "== Please type 'yes' or 'no' ==" + ENTER)
                new_prompt = False
                user_input = input(prompt).strip().lower()
                if_exit()
                continue
    if AGE_PROMPT == prompt:
        while True:            
            if user_input.isdigit() and 0 <= int(user_input) <= 150:
                return user_input
            else:
                clear_lines_and_print(SINGLE_LINE if new_prompt else DOUBLE_LINE, "== Please enter a valid age between 0 and 150 ==" + ENTER)
                new_prompt = False
                user_input = input(prompt).strip().lower()
                if_exit()
                continue
    if WEIGHT_PROMPT == prompt:
        while True:            
            if user_input.replace('.', '', 1).isdigit() and 0 <= float(user_input) <= 500:
                weight = round(float(user_input), 2)
                return str(weight)
            else:
                clear_lines_and_print(SINGLE_LINE if new_prompt else DOUBLE_LINE, "== Please enter a valid weight between 0 and 500 with at most 2 decimal places ==" + ENTER)
                new_prompt = False
                user_input = input(prompt).strip().lower()
                if_exit()
                continue
    if CHOICE_PROMPT == prompt:
        while True:
            if user_input.isdigit() or user_input.replace('.', '', 1).isdigit():
                return user_input
            else:
                clear_lines_and_print(SINGLE_LINE if new_prompt else DOUBLE_LINE, "== Please enter a valid choice number [1-4] ==" + ENTER)
                new_prompt = False
                user_input = input(prompt).strip().lower()
                if_exit()
                continue
        
        

@log_function
def choose_antibiotic(allergy_list):
    print(CHOOSE_ANTIBIOTIC_PROMPT)
    i = 1
    if 1 not in allergy_list:
        print(str(i)+"."+AMOXICILLIN_OPTION)
        i += 1
    if 2 not in allergy_list:
        print(str(i)+"."+ERYTHROMYCIN_OPTION)
        i += 1
    if 3 not in allergy_list:
        print(str(i)+"."+CLARITHROMYCIN_OPTION)
        i += 1
    if 4 not in allergy_list:
        print(str(i)+"."+DOXYCYCLINE_OPTION)

    antibiotics_set = ["AMOXICILLIN", "ERYTHROMYCIN", "CLARITHROMYCIN", "DOXYCYCLINE"]
    index = 1
    for i in allergy_list:
        antibiotics_set.pop(i-index)
        index += 1
    choice = antibiotics_set[int(get_patient_input(CHOICE_PROMPT))-1]
    
    return choice

def clear_lines_and_print(lines_to_clear, message):
    for _ in range(lines_to_clear):
        # Move cursor up
        sys.stdout.write('\033[1A')
        # Clear line
        sys.stdout.write('\033[2K\033[1G')
        sys.stdout.flush()

    # Print the new message
    sys.stdout.write(message)
    sys.stdout.flush()
    
def main():
    setup_logging(False)
    while True:
        exit_input = get_patient_input(EXIT_PROMPT)
        if exit_input.lower() in {"q", "exit"}:
            dispose.remove_pycache(ROOT_PATH)
            sys.exit()
        elif exit_input.lower() == "r":
            print(SEPARATOR + ENTER)
            csv_util.read_csv_records()
            print(ENTER + SEPARATOR)
            continue
        try:
            age = int(get_patient_input(AGE_PROMPT))
            pregnant = get_patient_input(PREGNANT_PROMPT)
            if pregnant == "Y":
                morolide_needed = get_patient_input(MOROLIDE_PROMPT)
            else:
                morolide_needed = "N"
            disease_or_impaired_organ = get_patient_input(DISEASE_PROMPT)
            allergy_or_interacting_medicine_list = get_patient_input(ALLERGY_PROMPT)
            if len(allergy_or_interacting_medicine_list) == 4:
                print(SEPARATOR + ENTER)
                print(f"{PRESCRIPTION_LABEL}{ENTER}{ENTER}No choice. Please consult your doctor.")
                print(ENTER + SEPARATOR)
                continue
            weight = float(get_patient_input(WEIGHT_PROMPT))
            
        except ValueError:
            print(INVALID_INPUT)
            return

        try:
            prescription = clincian_decision_system(age, weight, pregnant, allergy_or_interacting_medicine_list, morolide_needed, disease_or_impaired_organ)
            if prescription == "" :
                choice = choose_antibiotic(allergy_or_interacting_medicine_list)
                prescription = clincian_decision_system_preference(choice, age, weight)
        except Exception as e:
            print(f"{ERROR_OCCURRED}{e}")
            return

        print(SEPARATOR + ENTER)
        print(f"{PRESCRIPTION_LABEL}{ENTER}{ENTER}{prescription}")
        print(ENTER + SEPARATOR)
        csv_util.save_to_csv(age, pregnant, allergy_or_interacting_medicine_list, weight, prescription)

if __name__ == "__main__":
    main()

