# -*- coding: utf-8 -*-
"""
Python script to get patrons list from Patreon
@version: 1.0.0
@author: V. / @Vinus
"""

# IMPORTS
import patreon

# PATREON ID & KEYS
# creator id - see https://www.patreon.com/portal/registration/register-clients
creator_id = ''

# MAIN
def main():
    api_client = patreon.API(creator_id) # initialize the patreon API client from the official patreon lib

    names = []
    campaign_id = api_client.fetch_campaign().data()[0].id() # get campaign_id for the specific account
    pledges_response = api_client.fetch_page_of_pledges(campaign_id,25,) # get informations from Patreon
    all_pledges = pledges_response.data()
    for pledge in all_pledges:
        patron_id = pledge.relationship('patron').id()
        patron = api_client.fetch_campaign_and_patrons().find_resource_by_type_and_id('user',patron_id)
        names.append(patron.attribute('full_name'))
    print(names)

    memberships_count = {}
    attributes = api_client.fetch_campaign().json_data['included'] # get informations from Patreon
    for attribute in attributes:
        try:
            membership = attribute['attributes']
            if(membership['amount']) != 0:
                memberships_count[membership['title']] = membership['patron_count']
        except:
            pass
    print(memberships_count)

if __name__ == "__main__":
    main()