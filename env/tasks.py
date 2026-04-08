def grade_easy(score):
    return 1.0 if score >= 0.8 else 0.0

def grade_medium(score):
    if score >= 0.6:
        return 1.0
    elif score >= 0.3:
        return 0.5
    return 0.0

def grade_hard(score):
    if score >= 0.5:
        return 1.0
    elif score >= 0.2:
        return 0.5
    return 0.0