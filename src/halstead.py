"""
Halstead Complexity Metrics Module
"""

import re
import math

from collections import Counter

# Note:
# - braces are counted separately
# - function definitions and calls are both counted as operands
# - template literals are combined with the string, counting as a single operand (f"{n} is odd.")

# https://docs.python.org/3/reference/lexical_analysis.html#keywords
# Excluded 'False', 'True', 'None' Constants (operands)
PY_KEYWORDS = [
    'and', 'as', 'assert', 'async',
    'await', 'break', 'class', 'continue', 'def', 'del', 'elif',
    'else', 'except', 'finally', 'for', 'from', 'global', 'if',
    'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or',
    'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
]

# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#keywords
# Excluded 'false', 'true' Constants (operands)
JS_KEYWORDS = [
    'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger',
    'default', 'delete', 'do', 'else', 'export', 'extends',
    'finally', 'for', 'function', 'if', 'import', 'in', 'instanceof',
    'new', 'null', 'return', 'super', 'switch', 'this', 'throw',
    'try', 'typeof', 'var', 'void', 'while', 'with',
    'let', 'static', 'yield', 'await',
    'implements', 'interface', 'package', 'private', 'protected',
    'arguments', 'as', 'async', 'eval', 'from', 'get', 'of', 'set'
]

# https://docs.python.org/3/library/token.html
PY_SYMBOLS = [
    '(', ')', '[', ']', ':', ',', ';', '+', '-', '*', '/', '|', '&',
    '<', '>', '=', '.', '%', '{', '}', '==', '!=', '<=', '>=', '~', '^',
    '<<', '>>', '**', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=',
    '<<=', '>>=', '**=', '//', '//=', '@', '@=', '->', '...', ':=', '!'
]

# https://tc39.es/ecma262/#sec-punctuators
JS_SYMBOLS = [
    '?.', '{', '(', ')', '[', ']', '.', '...', ',', ';', '<', '>', '<=', '>=',
    '==', '!=', '===', '!==', '+', '-', '*', '%', '**', '++', '--', '<<',
    '>>', '>>>', '&', '|', '^', '!', '~', '&&', '||', '??', '?', ':', '=',
    '+=', '-=', '*=', '%=', '**=', '<<=', '>>=', '>>>=', '&=', '|=', '^=',
    '&&=', '||=', '??=', '=>', '/', '/=', '}'
]

PY_COMMENT = '#'
JS_COMMENT = '//'

PY_MULTI_WORD_OPERATORS = [
    'is not', 'not in'
]
JS_MULTI_WORD_OPERATORS = []

KEYWORDS = PY_KEYWORDS
SYMBOLS = PY_SYMBOLS
MULTI_WORD_OPERATORS = PY_MULTI_WORD_OPERATORS
COMMENT = PY_COMMENT

OPERATORS = [
    *SYMBOLS,
    *KEYWORDS,
    *MULTI_WORD_OPERATORS
]

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
    # Remove single-line comments (# to end of line)
    lines = code_text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Find # that's not inside a string
        in_string = False
        quote_char = None
        comment_pos = None

        for i, char in enumerate(line):
            if not in_string and char in ['"', "'"]:
                in_string = True
                quote_char = char
            elif in_string and char == quote_char and (i == 0 or line[i-1] != '\\'):
                in_string = False
                quote_char = None
            elif not in_string:
                if len(COMMENT) == 1 and char == COMMENT:
                    comment_pos = i
                    break
                elif len(COMMENT) == 2 and i + 1 < len(line) and char + line[i+1] == COMMENT:
                    comment_pos = i
                    break

        if comment_pos is not None:
            cleaned_lines.append(line[:comment_pos])
        else:
            cleaned_lines.append(line)

    code_text = '\n'.join(cleaned_lines)

    # Handle multi-word operators, but only outside of strings
    temp_code = ""
    i = 0
    multi_word_map = {}

    while i < len(code_text):
        # Check if we're starting a string
        if code_text[i] in ['"', "'", '`']:
            quote_char = code_text[i]
            # Find the end of the string
            j = i + 1
            while j < len(code_text):
                if code_text[j] == quote_char and (j == i + 1 or code_text[j-1] != '\\'):
                    break
                j += 1
            # Add the entire string (including quotes) without modification
            temp_code += code_text[i:j+1]
            i = j + 1
        else:
            # Check for multi-word operators at this position
            found_multiword = False
            for op_idx, op in enumerate(MULTI_WORD_OPERATORS):
                if code_text[i:i+len(op)] == op:
                    # Make sure it's a complete word boundary match
                    before_ok = (i == 0 or not code_text[i-1].isalnum())
                    after_ok = (i + len(op) >= len(code_text) or not code_text[i+len(op)].isalnum())

                    if before_ok and after_ok:
                        placeholder = f"__MULTIWORD_{op_idx}__"
                        temp_code += placeholder
                        multi_word_map[placeholder] = op
                        i += len(op)
                        found_multiword = True
                        break

            if not found_multiword:
                temp_code += code_text[i]
                i += 1

    # Sort symbols by length (longest first) to match multi-char operators first
    sorted_symbols = sorted(SYMBOLS, key=len, reverse=True)

    # Create regex pattern that matches:
    # 1. f-strings and other prefixed string literals (f"...", r"...", etc.)
    # 2. Regular string literals (double and single quoted)
    # 3. Multi-word operator placeholders
    # 4. Multi-character operators (longest first)
    # 5. Keywords and identifiers
    # 6. Single characters
    multiword_pattern = '|'.join(re.escape(placeholder) for placeholder in multi_word_map.keys())
    symbol_pattern = '|'.join(re.escape(sym) for sym in sorted_symbols)
    keyword_pattern = r'\b(?:' + '|'.join(KEYWORDS) + r')\b'
    identifier_pattern = r'\b\w+\b'

    if multiword_pattern:
        pattern = f'[frbFRB]*"[^"]*"|[frbFRB]*\'[^\']*\'|`[^`]*`|{multiword_pattern}|{symbol_pattern}|{keyword_pattern}|{identifier_pattern}'
    else:
        pattern = f'[frbFRB]*"[^"]*"|[frbFRB]*\'[^\']*\'|`[^`]*`|{symbol_pattern}|{keyword_pattern}|{identifier_pattern}'

    tokens = re.findall(pattern, temp_code)

    # Replace placeholders back with original multi-word operators
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

    # Halstead calculations
    unique_operators = set(tok for tok in tokens if tok in OPERATORS)
    unique_operands = set(tok for tok in tokens if tok not in OPERATORS)
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