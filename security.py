"""
    Security.py

    * programmed by Guillaume Simler
    * this program contains the main security features

"""

"""
    I. Import modules
"""

import bleach
import random
import string

"""
    II. Program
"""

def escape(value):
    """
        extends the classic escaping also to the apostrophe

        @Reviewer: Do you please have a better way?
    """
    value = bleach.clean(value)

    value = value.replace("'", "&#39;")

    return value

def generate_token():

    """
        generate a tokken against man in the middle attacks
    """

    result = ''.join(random.choice(string.ascii_letters + string.digits) for x in xrange(32))

    return result