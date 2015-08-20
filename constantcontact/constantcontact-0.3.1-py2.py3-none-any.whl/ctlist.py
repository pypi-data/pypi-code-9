attributes = {
    'name': 255,
}

class CtList:
    def __init__(self):
        self.CtList = {}
        self.CtList['status'] = 'ACTIVE'

        for attribute in attributes:
            self.CtList[attribute] = ''
            
    def set_attribute(self, attribute, content):
        global attributes
        if attribute in attributes:
            if len(content) in range(attributes[attribute]+1):
                self.CtList[attribute] = content
            else:
                raise Exception(attribute+' must have no more than '+str(attributes[attribute])+' characters')
        elif attribute == 'status':
            if content in ['ACTIVE', 'HIDDEN']:
                self.CtList[attribute] = content
            else:
                raise Exception('Acceptable values for status are ACTIVE and HIDDEN')
        else: 
            raise NameError('Attribute '+attribute+' not found')
        
    def get_ctlist(self):
        return self.CtList
