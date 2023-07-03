import json

from django.test import TestCase

# Create your tests here.
d = {

    'default': {
        'font': 'Arial',
        'size': 0.4,
    },
    'font': 'Arial',
    'size': 0.4,
}
with open('fonts.json', 'w') as f:
    json.dump(d, f)

