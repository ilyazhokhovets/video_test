import json
import os

from django.core.management.base import BaseCommand
FONTS = {
    'arial': {'command': '--arial',
              'short': '-a',
              },
    'calibri': {'command': '--calibri',
              'short': '-c',
              },
    'georgia': {'command': '--georgia',
              'short': '-g',
              },
    'timesnewroman': {'command': '--timesnewroman',
              'short': '-t',
              },
    'rubikbeastly':{'command': '--rubikbeastly',
              'short': '-r',
              },
}



class Command(BaseCommand):
    help = 'Chose font from given list'

    def handle(self, *args, **options):
        if not 0<=options['size'] <= 1:
            raise ValueError(f'Font size must be in range(0,1)')
        font_arguments_count = 0
        for font in FONTS:
            font_arguments_count += options[font]
        if font_arguments_count > 1:
            raise ValueError(f'Expected not more than 1 font, but {font_arguments_count} were found')

        for font in FONTS:
            if options[font]:
                self.change_font(font, options['size'])

    def add_arguments(self, parser):
        for font in FONTS:
            parser.add_argument(
                FONTS[font]['short'],
                FONTS[font]['command'],
                default=False,
                action="store_true",
            )
        parser.add_argument(
            '-s',
            '--size',
            default=False,
            type=float,
            help='Change font size. It has to be a number from 0 to 1, '
                 'which is the ratio of the text size relative to the size of entire frame'
        )

    def change_font(self, font, size):
        with open('videoTestCase/fonts.json', 'r') as f:
            font_settings = json.load(f)
        font_settings['font'] = font.capitalize()
        if size: font_settings['size'] = size
        with open('videoTestCase/fonts.json', 'w') as f:
            json.dump(font_settings, f)
