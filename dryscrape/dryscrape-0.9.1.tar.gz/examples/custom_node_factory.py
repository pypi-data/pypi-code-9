import dryscrape
import dryscrape.driver.webkit

class MyNode(dryscrape.driver.webkit.Node):
  """ A Node implementation with custom helper methods. """
  def attributes(self):
    doc = self.client.document()
    lxml_node = doc.xpath(self.path())[0]
    return lxml_node.attrib

class MyNodeFactory(dryscrape.driver.webkit.NodeFactory):
  """ Custom node factory for our Node implementation. """
  def create(self, node_id):
    return MyNode(self.client, node_id)

if __name__ == "__main__":
  driver = dryscrape.driver.webkit.Driver(node_factory_class=MyNodeFactory)
  sess = dryscrape.Session(driver = driver)
  sess.visit("http://google.de")
  print sess.at_css("body").attributes()
  # => { 'onload': "...",
  #      'alink': '#ff0000',
  #      'text': '#000000',
  #      'bgcolor': '#ffffff',
  #      'link': '#0000cc',
  #      'vlink': '#551a8b' }
