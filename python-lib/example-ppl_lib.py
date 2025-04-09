# -*- coding: utf-8 -*-
"""
Use example for PythonPatreonList lib
@version: 1.0.0
@author: V. / @Vinus
"""

# IMPORTS
import ppl_lib # import the PythonPatreonList lib

# MAIN
def main():
    creator_id = "" # replace by your own - see https://www.patreon.com/portal/registration/register-clients
    patreonlister = ppl_lib.patreonlister(creator_id) # create a patreonlister object

    print(patreonlister.get_memberships_count()) # return a dict with the number of patrons for each membership
    print(patreonlister.get_patrons()) # return the list of all patrons
    
if __name__ == "__main__":
    main()