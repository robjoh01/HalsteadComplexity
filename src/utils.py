"""
Utilities module
"""

# Scoring thresholds
GRADE_THRESHOLDS = {
    'A+': 90,
    'A': 85,
    'A-': 80,
    'B+': 75,
    'B': 70,
    'B-': 65,
    'C+': 60,
    'C': 55,
    'C-': 50,
    'D+': 45,
    'D': 40,
    'F': 0
}

def assign_grade(score):
    """
    Assigns a grade based on the given score.

    Args:
        score (int): The score to assign a grade for.

    Returns:
        str: The assigned grade.
    """

    for grade, threshold in GRADE_THRESHOLDS.items():
        if score >= threshold:
            return grade

    return 'F'

def calc_score_and_grade(loc: dict, halstead: dict, key_freq: dict, avg_line: float) -> tuple:
    """
    Calculates the final score and grade based on the given metrics.

    Args:
        loc (dict): Dictionary containing LOC metrics.
        halstead (dict): Dictionary containing Halstead metrics.
        key_freq (dict): Dictionary containing keyword frequencies.
        avg_line (float): Average line length.

    Returns:
        tuple: A tuple containing the final score and the assigned grade.
    """

    score = 100

    # LOC Metrics Adjustments
    if loc['Comment Lines'] < 1:
        score -= 10  # Lack of comments
    if loc['Code Lines'] > 10 and loc['Total Lines'] > 10 and loc['Comment Lines'] / loc['Code Lines'] < 0.2:
        score -= 5  # Low comment-to-code ratio

    # Halstead Metrics Adjustments
    if halstead['Effort'] > 500:
        score -= 15  # High effort for understanding
    if halstead['Difficulty'] > 10:
        score -= 10  # High difficulty
    if halstead['Vocabulary'] > 20:
        score -= 5   # Excessive vocabulary

    # Average Line Length
    if avg_line > 80:
        score -= 5  # Lines too long
    elif avg_line < 20:
        score -= 5  # Excessively short lines

    # Assign grade
    grade = assign_grade(score)
    return score, grade