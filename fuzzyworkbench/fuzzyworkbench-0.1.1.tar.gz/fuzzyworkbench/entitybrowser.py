#Abstract class representing an entity browser

class EntityBrowser:
    def __init__(self, editor):
        self._editor = editor
        self._entities = []

    def add(self, entity):
        self._entities.append(entity)
        
    def remove(self, entity):
        self._entities.remove(entity)
        
    def select(self, entity):
        pass
        
    def getSelected(self):
        pass
