import re

class GermanTranslator(object):

    mapping = [
        (r'\bA\b', 'EINE'),
        (r'\bOR\b', 'ODER'),
        (r'\bWITH\b', 'MIT'),
        (r'\bFROM\b', 'VON'),
        (r'\bIS NOT\b', 'KEINE'),
        (r'\bAND\b', 'UND'),
        (r'\bTHE\b', 'DIE'),
        (r'\bYOUR\b', 'DEINE'),
        (r'\bDO NOT\b', 'NEIMALS'),
        (r'\bIS\b', 'IST'),
        (r'\bTHIS\b', 'DIESES'),
    ]

    def translate(self, text):
        # Deutsch it inefficiently but hilariously
        for find, replace in self.mapping:
            text = re.sub(find, replace, text)
        return text
