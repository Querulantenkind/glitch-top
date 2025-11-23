"""
Configuration and themes for GlitchTop.
"""

THEMES = {
    "standard": {
        "low": "·",
        "med": "+",
        "high": "#",
        "critical": "█"
    },
    "runes": {
        "low": "᚛",
        "med": "᚜",
        "high": "ᚠ",
        "critical": "ᛸ"
    },
    "matrix": {
        "low": "0",
        "med": "1",
        "high": "Ӝ",
        "critical": "▓"
    },
    "braille": {
        "low": "⠀",
        "med": "⠶",
        "high": "⣿",
        "critical": "█"
    }
}

# Current configuration
CONFIG = {
    "theme": "standard",
    "glitch_enabled": True,
    "glitch_threshold": 80.0,  # CPU percentage to start glitching heavily
}

