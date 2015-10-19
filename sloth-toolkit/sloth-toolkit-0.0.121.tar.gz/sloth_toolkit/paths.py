import os
from .urls import LazyUrl, is_lazyurl
from . import verify


TEXT_EXTENSIONS = ['html', 'txt', 'md', ]
IMAGE_EXTENSIONS = ['jpg', 'png', 'bmp', ]
COMPRESSED_EXTENSIONS = ['tar.gz', 'zip', 'rar']

VALID_EXTENSIONS = []
VALID_EXTENSIONS += [ext for ext in TEXT_EXTENSIONS]
VALID_EXTENSIONS += [ext for ext in IMAGE_EXTENSIONS]
VALID_EXTENSIONS += [ext for ext in COMPRESSED_EXTENSIONS]



def is_lazypath(obj):
    return verify.is_type_of(obj, LazyPath)




def save_file(lazypath, data):
    def write(file, data):
        file.write(data)
        file.close()
        
    if (lazypath.extension in TEXT_EXTENSIONS):
        ## Check if file exists (remove it)
        f = open(lazypath.destination, 'w')
        wirte(f, data)
    elif (lazypath.extension in IMAGE_EXTENSIONS):
        f = open(lazypath.destination, 'wb')
        wirte(f, data)
    elif (lazypath.extension in COMPRESSED_EXTENSIONS):
        f = open(lazypath.destination, 'wb')
        wirte(f, data)



class LazyPath(object):
    """ 
    Create a file path from a url.
    
    self.cur_dir - Current directory
    self.path - Formed from the url (Excluded the filename)
    self.filename - The name of a file which can be created
    self.extension - Used to determine how to save to file
    """
    def __repr__(self): 
        return str(self.destination)
    def __str__(self): 
        return str(self.destination)
    def __unicode__(self): 
        return unicode(self.destination)

    def display_object(self):
        return '<LazyPath: %s>' % self.destination
    
    def __init__(self, url):
        self.new_path(url)
    
    def new_path(self, url):
        url = LazyUrl(url)        
        self.cur_dir = os.getcwd()        
        
        self.path = '/'.join([url.host, url.path])
        self._remove_duplicated_url_seperators()        
        self.path = os.sep.join(self.path.split('/'))
        
        self._extract_filename(url)

        self.full_path = os.path.join(self.cur_dir, self.path)
        self.destination = os.path.join(self.full_path, self.filename)




    def _extract_filename(self, url):
        # 'somesite.com/store/' becomes 'store/'
        self.filename = self.path.replace(url.host+os.sep, "")
        self.filename = self.filename.split('/')
        
        if (self.filename == []):
            self.filename = 'home.html'
            
        # 'store/' becomes 'store'
        elif (len(self.filename) > 1):
            if (self.filename[-1] == ''):
                self.filename = self.filename[-2]
            else:
                self.filename = self.filename[-1]
        else:
            self.filename = self.filename[-1]
            
        if (self.filename == ''):
            self.filename = 'home.html'
        
        self.path = self.path.replace(self.filename, "")
        
        # 'store' becomes 'store.html' - Default extension to .html
        if (len(self.filename.split('.')) == 0):
            self.filename += '.html'

        self._extract_extension()
            

                
    def _extract_extension(self):
        self.extension = self.filename.split('.')
        if (len(self.extension) == 0):
            self.filename += '.html'
            self._extract_extension()

        elif (len(self.extension) == 1):
            self.extension = self.extension[0]        
            if (self.extension not in VALID_EXTENSIONS):
                self.filename += '.html'
                self._extract_extension() # Restart (Recursive Condition)
        
        elif (len(self.extension) > 1):
            if (self.extension[-1] in VALID_EXTENSIONS):
                self.extension = self.extension[-1]
            elif ('.'.join(self.extension[-2:]) in VALID_EXTENSIONS):
                self.extension = '.'.join(self.extension[-2:])
            # Look for Vaild Double Extensions
            else:
                self.filename += '.html'
                self._extract_extension()
                    


    def _remove_duplicated_url_seperators(self):
        last_char = ''
        new_path = ''
        for i, char in enumerate(self.path):
            if (char == '/') and (char == last_char):
                new_path += ''
                continue
            new_path += char
            last_char = char
    
        self.path = new_path



def unix_path(url):
    url = LazyUrl(url)
    path = LazyPath(url)
    return path

def windows_path(url):
    url = LazyUrl(url)
    path = LazyPath(url)
    path.convert_to_windows()
    return path



if __name__ == '__main__':
    url = "stackoverflow.com/users/1886/details.r"
    url = LazyUrl(url)
    
    path = LazyPath(url)
    
    print url
    print path
    print path.extension
