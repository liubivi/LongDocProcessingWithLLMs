import re
"""
Explanation:
-------------
Because Python's 're' module does NOT allow variable-length patterns in a lookbehind, our previous approach using:

    (?<!\b(?:<variable-length patterns>))

causes "look-behind requires fixed-width pattern" errors.

Solution:
-------------
We avoid negative lookbehinds with variable-length patterns by:
1) Replacing all "non-splitting" exceptions (abbreviations, year notations, domains, decimals, etc.) with placeholder tokens that do not contain sentence punctuation.
2) Splitting on the normal sentence boundary pattern:
      (?<=[.!?])\s+ | \n
3) Replacing the placeholder tokens back to their original text.

This ensures we never incorrectly split inside exceptions that contain dots.
"""

# Step 1: Define sets/patterns for exceptions that should NOT trigger sentence splitting.

# Common abbreviations in English and Lithuanian.
COMMON_ABBREVIATIONS = {
    "Mr.", "Mrs.", "Dr.", "i.e.", "e.g.", "vs.", "Prof.", "Jr.", "Sr.", "Inc.", "Ltd.", "Co.",
    "U.S.", "U.K.", "Ph.D.", "M.D.", "B.A.", "M.A.", "D.C.", "a.m.", "p.m.", "No.", "vol.", "pp.", "Ch.",
    "pvz.", "p.", "įsk.", "op.cit.", "ibid.", "plg.", "red.", "t.t.", "t.y.", "t. y.", "t. t.", "etc.", "tūkst.", "mln.", "mlrd.", "mlr.",
    "val.", "sav.", " d.", "mėn.", "proc."
}

# General regex patterns that might contain a dot but do not indicate end of sentence.
GENERAL_PATTERNS = [
    # Lithuanian year notation: "2025 m.", "1979 m." etc.
    r"\b\d{4}\sm\.",
    # Multiple uppercase initials: "J.R.R.", etc.
    r"\b[A-Z](?:\.[A-Z])+\.",
    # Single uppercase initial: "A.", "P.", etc.
    r"\b[A-Z]\.(?=\s[A-Z])",
    # Domain or file extension: "example.com", "file.pdf", etc.
    # Very simplified pattern.
    r"\b[A-Za-z0-9_-]+\.(?:com|lt|org|net|pdf|docx|xlsx|txt)\b",
    # Decimal/time patterns: "3.14", "14.45" etc.
    r"\b\d+\.\d+\b",
    # Enumerations: "1.", "10." etc.
    r"\b\d+\.",
]


def _build_exceptions_pattern():
    # Combine literal abbreviations + general patterns into a single pattern.

    # 1) Escape literal abbreviations so their dots don't become special in regex.
    escaped_abbrevs = [re.escape(abbr) for abbr in COMMON_ABBREVIATIONS]

    # 2) Combine into one alternation: (?:...|...)
    # Note: general patterns are already raw regex, so we just keep them.
    combined = escaped_abbrevs + GENERAL_PATTERNS

    # Single giant alternation pattern.
    # We use capturing groups so re.sub can pick the match text.
    return re.compile("(" + "|".join(combined) + ")")


EXCEPTIONS_PATTERN = _build_exceptions_pattern()


def chunk_text_by_sentences(text: str):
    """
    Splits text into individual sentences by splitting on:
        (?<=[.!?])\s+ or newlines (\n)
    But first, replaces certain known exceptions (which contain dots but do not end sentences) with placeholders.
    Then reverts the placeholders after splitting.
    """

    # Step 2: Replace exceptions with placeholders.
    placeholder_map = {}
    placeholder_counter = 0

    def replace_exceptions(m: re.Match):
        nonlocal placeholder_counter
        original = m.group(1)  # matched text
        placeholder = f"__PLACEHOLDER_{placeholder_counter}__"
        placeholder_map[placeholder] = original
        placeholder_counter += 1
        return placeholder

    # Protect exceptions by substituting them with placeholders.
    protected_text = EXCEPTIONS_PATTERN.sub(replace_exceptions, text)

    # Step 3: Split on sentence boundaries.
    # We no longer need a negative lookbehind. We do a simple split on punctuation + whitespace or newlines.
    split_pattern = re.compile(r"(?<=[.!?])\s+|\n")
    raw_sentences = re.split(split_pattern, protected_text)

    # Step 4: Revert placeholders in each piece.
    chunks = []
    for sentence in raw_sentences:
        for placeholder, original in placeholder_map.items():
            sentence = sentence.replace(placeholder, original)
        clean = sentence.strip()
        if clean:
            chunks.append(clean)

    return chunks
iteration = input_data.get("iteration","")
# 'text' is expected to be passed as inputData from a previous step.
textOriginal = input_data.get("textOriginal", "")
textGemini = input_data.get("textGemini", "")
textChatgpt = input_data.get("textChatgpt", "")
# Process the text into single-sentence chunks.
chunksOriginal = chunk_text_by_sentences(textOriginal)
chunksChatgpt = chunk_text_by_sentences(textChatgpt)
chunksGemini = chunk_text_by_sentences(textGemini)
maxlength = max(len(chunksOriginal), len(chunksChatgpt), len(chunksGemini))+1
maxlengths = [str(iteration).zfill(4)+"_"+str(i).zfill(4) for i in range(1,maxlength)]
# Return the chunks
return {"originalSegments": chunksOriginal, "chatgptSegments": chunksChatgpt, "geminiSegments": chunksGemini, "chunkCount": maxlengths}
