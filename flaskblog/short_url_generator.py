"""
This file contain business logic for generating random string of length 10 combining abcd....., ABCD........ and 123...
Author: Akshaya Revaskar
Date: 12/04/2020
"""
import random
import string


class ShortUrlGenerator:

    def short_url(self, string_length):
        """Generate a random string of letters and digits """
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(string_length))
