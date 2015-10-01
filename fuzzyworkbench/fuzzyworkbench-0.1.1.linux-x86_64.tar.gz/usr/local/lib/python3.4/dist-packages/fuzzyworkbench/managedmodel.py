class ManagedModel:
    """A model in which changes are monitored"""
    def __init__(self, editor):
        self._editor = editor
        self._changed = False
        
    def _do_changed(self, *args):
        self._changed = True
        if self._editor:
            self._editor.notify(self)
        
    def hasChanged(self):
        return self._changed
        
    def save(self):
        self._changed = False
