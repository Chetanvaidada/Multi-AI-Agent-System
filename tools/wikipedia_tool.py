import wikipedia
from langchain.tools import tool
@tool
def wikipedia_search(query: str, sentences: int = 3):
    """
    Fetch a short summary from Wikipedia using the wikipedia library.

    Args:
        query (str): Search term (e.g., "Python programming language")
        sentences (int): Number of summary sentences

    Returns:
        dict: Wikipedia summary or error
    """
    try:
        wikipedia.set_lang("en")

        summary = wikipedia.summary(
            query,
            sentences=sentences,
            auto_suggest=True,
            redirect=True
        )

        page = wikipedia.page(query, auto_suggest=True)

        return {
            "title": page.title,
            "summary": summary,
            "url": page.url
        }

    except wikipedia.exceptions.DisambiguationError as e:
        return {
            "query": query,
            "error": "Disambiguation error",
            "options": e.options[:5]
        }

    except wikipedia.exceptions.PageError:
        return {
            "query": query,
            "error": "Page not found"
        }

    except Exception as e:
        return {
            "query": query,
            "error": str(e)
        }