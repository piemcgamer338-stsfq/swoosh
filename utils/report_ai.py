import re


BEGGING_PATTERNS = [
    r"\b(send|give|donate|tip)\b.*\b(me|pls|please)\b",
    r"\bfree\b.*\b(points?|coins?|money|cash|tip)\b",
    r"\bcan\s+anyone\b.*\b(send|give|tip)\b",
    r"\bi\s+need\b.*\b(points?|money|cash|coins?)\b",
    r"\bpls\b.*\b(points?|coins?|money|cash)\b",
    r"\bplease\b.*\b(points?|coins?|money|cash)\b",
    r"\btip\s+me\b",
    r"\bgive\s+me\b",
    r"\bsend\s+me\b"
]


def analyse_message(content: str) -> dict:

    text = content.lower().strip()

    for pattern in BEGGING_PATTERNS:

        if re.search(pattern, text):

            return {
                "violation": True,
                "category": "Begging",
                "reason": (
                    "The message requests free money, "
                    "points, tips or gambling currency."
                )
            }

    return {
        "violation": False,
        "category": None,
        "reason": (
            "Analysis determined this message "
            "does not violate moderation policies or rules."
        )
    }
