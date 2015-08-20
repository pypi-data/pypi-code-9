attributes = {
    'city': 50, 'country_code': 2, 'line1': 50, 'line2': 50, 'line3': 50,
    'postal_code': 25, 'sub_postal_code': 25, 'state_code': 2, 'state': 50, 
}

class Address:
    def __init__(self):
        self.address = {}
        self.address['address_type'] = ''

        for attribute in attributes:
            self.address[attribute] = ''
            
    def set_attribute(self, attribute, content):
        global attributes
        if attribute in attributes:
            if len(content) in range(attributes[attribute]+1):
                self.address[attribute] = content
            else:
                raise Exception(attribute+' must have no more than '+str(attributes[attribute])+' characters')
        elif attribute == 'address_type':
            if content in ['PERSONAL', 'BUSINESS']:
                self.address[attribute] = content
            else:
                raise Exception('Acceptable values for address_type are PERSONAL and BUSINESS')
        else: 
            raise NameError('Attribute '+attribute+' not found')
        
    def get_address(self):
        return self.address
