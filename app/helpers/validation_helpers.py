ALLOWED_SHELF_STATUSES = [
    "Read",
    "Currently Reading",
    "To Be Read",
    "Did Not Finish",
    "remove"
]


def is_valid_rating(stars, allow_zero=False):
    if stars is None:
        return False

    minimum = 0 if allow_zero else 1
    return minimum <= stars <= 5


def is_valid_review_text(text):
    return bool(text and text.strip())


def is_valid_shelf_status(status):
    return status in ALLOWED_SHELF_STATUSES