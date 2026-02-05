import requests
from langchain.tools import tool
BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"

@tool
def dictionary_lookup(word: str):
    """
    Fetch dictionary definitions for a word using dictionaryapi.dev.

    Args:
        word (str): The English word to look up.

    Returns:
        dict: Word definitions and related info, OR error info.
    """
    url = f"{BASE_URL}/{word}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {
            "word": word,
            "error": str(e)
        }

    data = response.json()

    # If API returns a dict with error info instead of a list
    if isinstance(data, dict) and data.get("title"):
        return {
            "word": word,
            "error": data.get("message", "No definition found")
        }

    # Expected success output is a list
    entry = data[0] if isinstance(data, list) and len(data) > 0 else None

    if not entry:
        return {
            "word": word,
            "error": "No definition found"
        }

    # Gather basic definition info
    definitions = []
    meanings = entry.get("meanings", [])
    for meaning in meanings:
        part_of_speech = meaning.get("partOfSpeech", "")
        for def_item in meaning.get("definitions", []):
            definitions.append({
                "part_of_speech": part_of_speech,
                "definition": def_item.get("definition"),
                "example": def_item.get("example"),
                "synonyms": def_item.get("synonyms", []),
                "antonyms": def_item.get("antonyms", [])
            })

    return {
        "word": entry.get("word"),
        "phonetic": entry.get("phonetic"),
        "definitions": definitions,
        "source_urls": entry.get("sourceUrls", [])
    }
