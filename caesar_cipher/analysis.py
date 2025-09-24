"""Heuristics for analyzing text, used for brute-force scoring."""

# List of common English words to assist in scoring potential decryptions.
COMMON_WORDS = [
    " the ", " and ", " to ", " of ", " that ", " is ", " in ", " it ",
    " for ", " you ", " with ", " on ", " have ", " be ", " as ", " at "
]

def english_score(text: str) -> int:
    """
    Calculates a score indicating the likelihood of a text being English.

    The score is based on the frequency of common English words and
    the presence of high-frequency letters.

    Args:
        text: The text to score.

    Returns:
        An integer score.
    """
    lower = " " + text.lower() + " "
    score = 0
    # Count common words, giving them a high weight.
    for word in COMMON_WORDS:
        score += lower.count(word) * 10

    # Add points for common letters (quick heuristic).
    freq = {char: lower.count(char) for char in "etaoinshrdlu"}
    score += sum(freq.values())
    return score
