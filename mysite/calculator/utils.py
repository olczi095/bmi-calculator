def calculate_bmi(height, weight):
    """
    Calculate BMI (Body Mass Index) based on height (in centimeter) and weight (in kilograms).
    """
    bmi_result = round(weight / (height * 0.01) ** 2, 2)
    return bmi_result


def calculate_bmr(age, gender, height, weight):
    """
    Calculate BMR (Basal Metabolic Rate) based on age, gender ('female' or 'male'),
    height (in centimeters) and weight (in kilograms).
    """
    if gender == 'male':
        bmr_result = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr_result = (10 * weight) + (6.25 * height) - (5 * age) - 161
    return bmr_result


def calculate_tmr(age, gender, height, weight, pal):
    """
    Calculate TMR (Total Metabolic Rate) based on age, gender ('female' or 'male'),
    height (in centimeters), weight (in kilograms) and PAL.
    """
    if gender == 'male':
        tmr_result = round(((10 * weight) + (6.25 * height) -
                           (5 * age) + 5) * float(pal), 2)
    else:
        tmr_result = round(((10 * weight) + (6.25 * height) -
                            (5 * age) - 161) * float(pal), 2)
    return tmr_result
