from django.conf import settings as SETTINGS


DEFAULT_IMAGE_FORMATS = {
    "1": {
        "folder": "covers",
        "display": "Background image",
        "sizes": {
            "xs": {
                "size": [105, 69],
                "method": "cover"
            },
            "sm": {
                "size": [350, 230],
                "method": "cover"
            },
            "md": {
                "size": [525, 345],
                "method": "cover"
            },
            "lg": {
                "size": [1050, 690],
                "method": "cover"
            }
        }
    },
    "2": {
        "folder": "content",
        "display": "Content image",
        "sizes": {
            "xs": {
                "size": 50,
                "method": "width"
            },
            "sm": {
                "size": 120,
                "method": "width"
            },
            "md": {
                "size": 200,
                "method": "width"
            },
            "lg": {
                "size": 400,
                "method": "width"
            }
        }
    },
    "3": {
        "folder": "pictos",
        "display": "Picto",
        "sizes": {
            "xs": {
                "size": [10, 10],
                "method": "cover"
            },
            "sm": {
                "size": [20, 20],
                "method": "cover"
            },
            "md": {
                "size": [30, 30],
                "method": "cover"
            },
            "lg": {
                "size": [35, 35],
                "method": "cover"
            }
        }
    },
    "4": {
        "folder": "logos",
        "display": "Logo",
        "sizes": {
            "xs": {
                "size": [50, 21],
                "method": "contain"
            },
            "sm": {
                "size": [100, 50],
                "method": "contain"
            },
            "md": {
                "size": [150, 62],
                "method": "contain"
            },
            "lg": {
                "size": [200, 83],
                "method": "contain"
            }
        }
    }
}

IMAGE_FORMATS = getattr(SETTINGS, 'IMAGE_FORMATS', DEFAULT_IMAGE_FORMATS)
