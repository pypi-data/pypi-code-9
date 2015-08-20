attributes = {
    'first_name': 50, 'prefix_name': 4, 'last_name': 50, 'cell_phone': 50, 
    'work_phone': 50, 'home_phone': 50, 'fax': 50, 'job_title': 50,
}

class Contact:
    def __init__(self):
        global attributes
        self.contact = {}
        self.contact['addresses'] = []
        self.contact['email_addresses'] = []
        self.contact['lists'] = []

        for attribute in attributes:
            self.contact[attribute] = ''

    def set_attribute(self, attribute, content):
        global attributes
        if attribute in attributes:
            if len(content) in range(attributes[attribute]+1):
                self.contact[attribute] = content
            else:
                raise Exception(attribute+' must have no more than '+str(attributes[attribute])+' characters')
        else: 
            raise NameError('Attribute '+attribute+' not found')

    def add_address(self, address):
        self.contact['addresses'] = []
        self.contact['addresses'].append(address.get_address())

    # The API ignores any additional email addresses beyond the first
    def add_email(self, email):
        if len(email) in range(6, 81):
            self.contact['email_addresses'] = []
            self.contact['email_addresses'].append({'email_address':email})
        else:
            raise Exception('email_address must have no more than 80 and at least 6 characters')
    
    def add_list(self, list_id, list_of_list_ids):
        if list_id in list_of_list_ids:
            self.contact['lists'].append({'id': list_id})
        else:
            raise NameError('List doesn\'t exist')
    
    def get_contact(self):
        return self.contact

    def set_contact(self, contact):
        self.contact = contact
