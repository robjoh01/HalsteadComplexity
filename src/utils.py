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

def extract_version(file_path):
    """
    Extract the version number from a file path.

    Args:
        file_path (str): The full path to the file (e.g., "plotly\python\plotly.py-6.0.0\packages\python\plotly\_plotly_utils\files.py")

    Returns:
        str: The version number (e.g., "6.0.0")
    """
    # Normalize path separators (convert backslashes to forward slashes)
    normalized_path = file_path.replace('\\', '/')

    # Split the path into parts
    parts = normalized_path.split('/')

    # Look for parts containing version numbers (like "plotly.py-6.0.0")
    for part in parts:
        if '-' in part:
            # Look for patterns like "name-X.Y.Z"
            possible_version = part.split('-')[-1]
            # Check if it looks like a version number (contains dots and digits)
            if '.' in possible_version and any(c.isdigit() for c in possible_version):
                return possible_version

    # If no version found in the path, return a default or None
    return None

def remove_path_prefix(file_path, prefix):
    """
    Remove a specified prefix from a file path.

    Args:
        file_path (str): The full path to the file
        prefix (str): The prefix to remove (e.g., 'plotly/python', 'plotly/js')

    Returns:
        str: The file path with the prefix removed
    """
    # Normalize path separators for both file_path and prefix
    normalized_path = file_path.replace('\\', '/')
    normalized_prefix = prefix.replace('\\', '/')

    # Ensure prefix ends with a slash
    if not normalized_prefix.endswith('/'):
        normalized_prefix += '/'

    # Find the position of the prefix in the path
    start_pos = normalized_path.find(normalized_prefix)

    # If found, return everything after the prefix
    if start_pos != -1:
        return normalized_path[start_pos + len(normalized_prefix):]

    # If not found (which shouldn't happen if prefix is always there)
    return normalized_path