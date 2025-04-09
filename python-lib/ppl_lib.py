# -*- coding: utf-8 -*-
"""
Python lib to get patrons list from Patreon
@version: 1.0.0
@author: V. / @Vinus
"""

# IMPORTS
import patreon

# PATREON LISTER CLASS
class patreonlister:
    """
    Class initializer
	Input : creator id - see https://www.patreon.com/portal/registration/register-clients
	Require : none
	Output : none
	Causes : the patreonlister object is initialized
    """
    def __init__(self, creator_id):
        self.creator_id = creator_id
        self.api_client = patreon.API(creator_id) # initialize the patreon API client from the official patreon lib

    """
    Class to_string
	Input : none
	Require : none
	Output : str with the patreonlister informations
	Causes : the patreonlister informations are returned
    """
    def __str__(self):
        return f"patreonlister(creator_id={self.creator_id})"
    
    """
    Get the number of patrons for each membership
	Input : none
	Require : none
	Output : dict with the number of patrons for each membership
	Causes : the memberships count is returned
    """
    def get_memberships_count(self):
        memberships_count = {}

        attributes = self.api_client.fetch_campaign().json_data['included'] # get informations from Patreon

        for attribute in attributes:
            try:
                membership = attribute['attributes']
                if(membership['amount']) != 0:
                    memberships_count[membership['title']] = membership['patron_count']
            except:
                pass
        return(memberships_count)
    
    """
    Get the name of all patrons
	Input : none
	Require : none
	Output : list with the nalme of all patrons
	Causes : the patrons list is returned
    """
    def get_patrons(self):
        names = []

        campaign_id = self.api_client.fetch_campaign().data()[0].id() # get campaign_id for the specific account
        pledges_response = self.api_client.fetch_page_of_pledges(campaign_id,25,)  # get informations from Patreon
        all_pledges = pledges_response.data()

        for pledge in all_pledges:
            patron_id = pledge.relationship('patron').id()
            patron = self.api_client.fetch_campaign_and_patrons().find_resource_by_type_and_id('user',patron_id)
            names.append(patron.attribute('full_name'))
        return(names)