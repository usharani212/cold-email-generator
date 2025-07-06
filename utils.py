import re

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>', '', text)

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Remove special characters (except alphanumerics and spaces)
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)

    # Strip leading and trailing whitespace
    text = text.strip()

    return text
