# BeatMind Knowledge Base
# This is where YOUR producer expertise lives
# Fill this in as you complete your Google Drive docs

GENRE_KNOWLEDGE = {
    "house_dubstep": {
        "tempo_range": (128, 142),
        "start_with": "melody",
        "time_per_section": "30-45 minutes",
        "production_order": [
            "melody",
            "chords",
            "bass",
            "drums",
            "pad",
            "arrangement",
            "mixdown",
        ],
        "official_touch": [
            # Fill this in from your Google Drive doc
        ],
        "amateur_mistakes": [
            # Fill this in from your Google Drive doc
        ],
        "chord_progressions": [
            # Fill this in from your Google Drive doc
        ],
    },
    # Add more genres here as you complete docs, e.g.
    # "trap": { ... },
}


def validate_knowledge(genre_knowledge: dict) -> None:
    """
    Basic runtime checks to catch missing keys or bad types.
    Raises ValueError with explanation if something's off.
    """
    required_genre_keys = {
        "tempo_range",
        "start_with",
        "time_per_section",
        "production_order",
        "official_touch",
        "amateur_mistakes",
        "chord_progressions",
    }

    if not isinstance(genre_knowledge, dict):
        raise ValueError("GENRE_KNOWLEDGE must be a dict.")

    for genre, data in genre_knowledge.items():
        if not isinstance(data, dict):
            raise ValueError(f"Genre entry for '{genre}' must be a dict.")
        missing = required_genre_keys - set(data.keys())
        if missing:
            raise ValueError(f"Genre '{genre}' is missing keys: {missing}")

        # quick type checks
        if not (isinstance(data["tempo_range"], tuple) and len(data["tempo_range"]) == 2):
            raise ValueError(f"Genre '{genre}' tempo_range must be a tuple (min, max).")
        if not isinstance(data["production_order"], list):
            raise ValueError(f"Genre '{genre}' production_order must be a list.")


if __name__ == "__main__":
    # quick check when running the file directly
    try:
        validate_knowledge(GENRE_KNOWLEDGE)
        print("GENRE_KNOWLEDGE looks good ✅")
    except Exception as e:
        print("Validation error:", e)
