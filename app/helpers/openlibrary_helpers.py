import requests

# Show 10 results per page
def search_open_library(query, page=1, limit=10):
    url = "https://openlibrary.org/search.json"

    params = {
        "q": query,
        "page": page,
        "limit": limit
    }

    response = requests.get(url, params=params)

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        return []

    books = []

    for doc in data.get("docs", []):
        cover_id = doc.get("cover_i")
        edition_key = doc.get("edition_key", [])

        books.append({
            "title": doc.get("title", "Unknown Title"),
            "author": ", ".join(doc.get("author_name", ["Unknown"])),
            "cover_url": f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None,
            "openlibrary_id": doc.get("key"),
            "edition_key": doc.get("edition_key", [None])[0] if doc.get("edition_key") else None,
            "publish_year": doc.get("first_publish_year")
        })
    return books


def fetch_openlibrary_description(olid):
    if not olid:
        return "Not available for this title."

    url = f"https://openlibrary.org{olid}.json"

    try:
        res = requests.get(url, timeout=8)
    except requests.RequestException:
        return "Not available for this title."

    if res.status_code != 200:
        return "Not available for this title."

    data = res.json()

    description = data.get("description")

    if isinstance(description, dict):
        return description.get("value")

    return description or "Not available for this title."


def fetch_page_count(openlibrary_id, edition_key=None):
    if edition_key:
        url = f"https://openlibrary.org/books/{edition_key}.json"
        try:
            res = requests.get(url, timeout=8)
        except requests.RequestException:
            res = None

        if res and res.status_code == 200:
            data = res.json()
            if data.get("number_of_pages"):
                return data["number_of_pages"]

    if openlibrary_id:
        url = f"https://openlibrary.org{openlibrary_id}.json"
        try:
            res = requests.get(url, timeout=8)
        except requests.RequestException:
            res = None

        if res and res.status_code == 200:
            data = res.json()

            if "latest_revision" in data:
                editions_url = f"https://openlibrary.org{openlibrary_id}/editions.json"
                try:
                    r = requests.get(editions_url, timeout=8)
                except requests.RequestException:
                    r = None

                if r and r.status_code == 200:
                    ed_data = r.json()
                    entries = ed_data.get("entries", [])

                    for e in entries:
                        if e.get("number_of_pages"):
                            return e["number_of_pages"]
    return None


def normalize_openlibrary_id(raw_openlibrary_id):
    if not raw_openlibrary_id:
        return None

    normalized = raw_openlibrary_id.strip()

    if normalized.lower() in {"undefined", "null", "none", ""}:
        return None

    if normalized.startswith("http://") or normalized.startswith("https://"):
        normalized = normalized.replace("https://openlibrary.org", "").replace("http://openlibrary.org", "")

    if not normalized.startswith("/"):
        normalized = f"/{normalized}"

    return normalized