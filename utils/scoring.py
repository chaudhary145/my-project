def calculate_percentage(scores: list[int]) -> int:
    max_score = len(scores) * 10
    return round((sum(scores) / max_score) * 100)

def grade_from_percentage(percent: int) -> str:
    if percent >= 85:
        return "A"
    elif percent >= 70:
        return "B"
    elif percent >= 55:
        return "C"
    else:
        return "D"
