"""
Halstead Complexity Metrics Module
"""

import re
import math

from collections import Counter

# Python example

# Caveats:
# - 'is not' and 'not in' will count as 2 operators
# - braces are counted separately
# - function definitions are counted as operands

# https://docs.python.org/3/reference/lexical_analysis.html#keywords
ALL_KEYWORDS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'async',
    'await', 'break', 'class', 'continue', 'def', 'del', 'elif',
    'else', 'except', 'finally', 'for', 'from', 'global', 'if',
    'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or',
    'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
}

EXCLUDED_KEYWORDS = {
    'False', 'True', 'None',  # Constants (operands)
}

KEYWORDS = ALL_KEYWORDS - EXCLUDED_KEYWORDS

# https://docs.python.org/3/library/token.html
SYMBOLS = [
    "(", ")", "[", "]", ":", ",", ";", "+", "-", "*", "/", "|", "&",
    "<", ">", "=", ".", "%", "{", "}", "==", "!=", "<=", ">=", "~", "^",
    "<<", ">>", "**", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=",
    "<<=", ">>=", "**=", "//", "//=", "@", "@=", "->", "...", ":=", "!"
]

MULTI_WORD_OPERATORS = [
    "is not", "not in"
]

OPERATORS = {
    *SYMBOLS,
    *KEYWORDS,
    *MULTI_WORD_OPERATORS
}

def calc_loc_metrics(lines: list) -> dict:
    """
    Calculate Line of Code (LOC) metrics.

    Args:
        lines (list): List of code lines.

    Returns:
        dict: Dictionary containing LOC metrics.
    """

    total_lines = len(lines)
    blank_lines = sum(1 for line in lines if line.strip() == "")
    comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
    code_lines = total_lines - blank_lines - comment_lines

    return {
        'Total Lines': total_lines,
        'Blank Lines': blank_lines,
        'Comment Lines': comment_lines,
        'Code Lines': code_lines
    }

def tokenize_code(code_text):
    """
    Tokenize code while preserving multi-character and multi-word operators.
    """

    temp_code = code_text
    multi_word_map = {}

    for i, op in enumerate(MULTI_WORD_OPERATORS):
        placeholder = f"__MULTIWORD_{i}__"
        temp_code = temp_code.replace(op, placeholder)
        multi_word_map[placeholder] = op

    sorted_symbols = sorted(SYMBOLS, key=len, reverse=True)

    # Create regex pattern that matches:
    # 1. String literals (double and single quoted)
    # 2. Multi-word operator placeholders
    # 3. Multi-character operators (longest first)
    # 4. Keywords and identifiers
    # 5. Single characters
    multiword_pattern = '|'.join(re.escape(placeholder) for placeholder in multi_word_map.keys())
    symbol_pattern = '|'.join(re.escape(sym) for sym in sorted_symbols)
    keyword_pattern = r'\b(?:' + '|'.join(KEYWORDS) + r')\b'
    identifier_pattern = r'\b\w+\b'

    pattern = f'r"[^"]*"|\'[^\']*\'|{multiword_pattern}|{symbol_pattern}|{keyword_pattern}|{identifier_pattern}'

    tokens = re.findall(pattern, temp_code)

    final_tokens = []
    for token in tokens:
        if token in multi_word_map:
            final_tokens.append(multi_word_map[token])
        else:
            final_tokens.append(token)

    return final_tokens

def calc_halstead_metrics(lines: list) -> dict:
    """
    Calculate Halstead complexity metrics.

    Args:
        lines (list): List of code lines.

    Returns:
        dict: Dictionary containing Halstead metrics.
    """

    code_text = " ".join(lines)
    tokens = tokenize_code(code_text)

    unique_operators = set(tok for tok in tokens if tok in OPERATORS)
    unique_operands = set(tok for tok in tokens if tok not in OPERATORS)

    # Halstead calculations
    n1 = len(unique_operators)
    n2 = len(unique_operands)
    N1 = sum(1 for tok in tokens if tok in OPERATORS)
    N2 = sum(1 for tok in tokens if tok not in OPERATORS)

    vocabulary = n1 + n2
    length = N1 + N2
    volume = length * math.log2(vocabulary) if vocabulary > 0 else 0
    difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
    effort = difficulty * volume
    time = effort / 18
    delivered_bugs = volume / 3000

    return {
        'Unique Operators': n1,
        'Unique Operands': n2,
        'Total Operators': N1,
        'Total Operands': N2,
        'Vocabulary': vocabulary,
        'Program Length': length,
        'Volume': volume,
        'Difficulty': difficulty,
        'Effort': effort,
        'Time': time,
        'Delivered Bugs': delivered_bugs
    }

def calc_keyword_frequency(lines: list) -> dict:
    """
    Calculate keyword frequency.

    Args:
        lines (list): List of code lines.

    Returns:
        dict: Dictionary containing keyword frequency.
    """

    tokens = re.findall(r'\b\w+\b', " ".join(lines))
    keyword_counts = Counter(tok for tok in tokens if tok in KEYWORDS)

    return keyword_counts or Counter({"None": 0})

def calc_average_line_length(lines: list) -> float:
    """
    Calculate the average line length.

    Args:
        lines (list): List of code lines.

    Returns:
        float: Average line length.
    """

    non_blank_lines = [line for line in lines if line.strip()]
    avg_length = sum(len(line) for line in non_blank_lines) / len(non_blank_lines) if non_blank_lines else 0
    return avg_length