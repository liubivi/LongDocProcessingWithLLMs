import re

def chunk_text(text, max_chunk_size):
    # Use a regex to split text into sentences.
    # This simple regex looks for a punctuation mark (. ! or ?) followed by whitespace.
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # If adding this sentence would exceed the maximum chunk size...
        if len(current_chunk) + len(sentence) + 1 > max_chunk_size:
            # If we already have some text in the current chunk, save it.
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                # In case a single sentence is longer than max_chunk_size,
                # break the sentence into smaller parts.
                for i in range(0, len(sentence), max_chunk_size):
                    part = sentence[i:i+max_chunk_size].strip()
                    if part:
                        chunks.append(part)
                current_chunk = ""
        else:
            # Otherwise, append the sentence to the current chunk.
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence

    # Append any remaining text.
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
# 'text' is expected to be passed as inputData from a previous step.
text = input_data.get("text", "")
# Process the text into chunks.
chunks = chunk_text(text, max_chunk_size=1500)
# Return the chunks
return {"chunks": chunks}
