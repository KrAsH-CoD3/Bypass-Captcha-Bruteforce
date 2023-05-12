
# -------------------------------------------------------------------------

import itertools

"""  
NOTE:   Generating a password character length more than 3 from 'char' 
        may possibly run out of memory and maybe crash code. 
        
        SIMPLE MATH ;) 
"""
length = 3  # Number of Password Character Length
numbers: str = '1234567890'
lowercase_letters: str = 'abcdefghijklmnopqrstuvwxyz'
uppercase_letters: str = lowercase_letters.upper()
symbols: str = "`~!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/"
chars: str = lowercase_letters + symbols + numbers 
# chars: str = lowercase_letters + uppercase_letters + numbers + symbols
passwords = [''.join(i) for i in itertools.product(chars, repeat=length)]
with open("passwords.txt", "w") as f:
    for password in passwords: 
        f.write(password + "\n")

# -------------------------------------------------------------------------