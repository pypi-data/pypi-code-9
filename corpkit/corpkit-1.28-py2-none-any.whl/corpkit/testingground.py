from nltk import Tree
from nltk import tree_to_treesegment
from nltk.draw.util import CanvasFrame, CanvasWidget, BoxWidget, TextWidget, OvalWidget, ParenWidget
from nltk.draw import TreeWidget
from nltk.tree import ParentedTree


def demo():
    import random
    def fill(cw):
        cw['fill'] = '#%06d' % random.randint(0,999999)

    cf = CanvasFrame(width=550, height=450, closeenough=2)

    t = Tree.fromstring('''
    (S (NP the very big cat)
       (VP (Adv sorta) (V saw) (NP (Det the) (N dog))))''')

    tc = TreeWidget(cf.canvas(), t, draggable=1,
                    node_font=('helvetica', -14, 'bold'),
                    leaf_font=('helvetica', -12, 'italic'),
                    roof_fill='white', roof_color='black',
                    leaf_color='green4', node_color='blue2')
    cf.add_widget(tc,10,10)

    def boxit(canvas, text):
        big = ('helvetica', -16, 'bold')
        return BoxWidget(canvas, TextWidget(canvas, text,
                                            font=big), fill='green')
    def ovalit(canvas, text):
        return OvalWidget(canvas, TextWidget(canvas, text),
                          fill='cyan')

    treetok = Tree.fromstring('(S (NP this tree) (VP (V is) (AdjP shapeable)))')
    tc2 = TreeWidget(cf.canvas(), treetok, boxit, ovalit, shapeable=1)

    def color(node):
        node['color'] = '#%04d00' % random.randint(0,9999)
    def color2(treeseg):
        treeseg.label()['fill'] = '#%06d' % random.randint(0,9999)
        treeseg.label().child()['color'] = 'white'

    tc.bind_click_trees(tc.toggle_collapsed)
    tc2.bind_click_trees(tc2.toggle_collapsed)
    tc.bind_click_nodes(color, 3)
    tc2.expanded_tree(1).bind_click(color2, 3)
    tc2.expanded_tree().bind_click(color2, 3)

    paren = ParenWidget(cf.canvas(), tc2)
    cf.add_widget(paren, tc.bbox()[2]+10, 10)

    tree3 = Tree.fromstring('''
    (S (NP this tree) (AUX was)
       (VP (V built) (PP (P with) (NP (N tree_to_treesegment)))))''')
    tc3 = tree_to_treesegment(cf.canvas(), tree3, tree_color='green4',
                              tree_xspace=2, tree_width=2)
    tc3['draggable'] = 1
    cf.add_widget(tc3, 10, tc.bbox()[3]+10)

    def orientswitch(treewidget):
        if treewidget['orientation'] == 'horizontal':
            treewidget.expanded_tree(1,1).subtrees()[0].set_text('vertical')
            treewidget.collapsed_tree(1,1).subtrees()[0].set_text('vertical')
            treewidget.collapsed_tree(1).subtrees()[1].set_text('vertical')
            treewidget.collapsed_tree().subtrees()[3].set_text('vertical')
            treewidget['orientation'] = 'vertical'
        else:
            treewidget.expanded_tree(1,1).subtrees()[0].set_text('horizontal')
            treewidget.collapsed_tree(1,1).subtrees()[0].set_text('horizontal')
            treewidget.collapsed_tree(1).subtrees()[1].set_text('horizontal')
            treewidget.collapsed_tree().subtrees()[3].set_text('horizontal')
            treewidget['orientation'] = 'horizontal'

    text = """
Try clicking, right clicking, and dragging
different elements of each of the trees.
The top-left tree is a TreeWidget built from
a Tree.  The top-right is a TreeWidget built
from a Tree, using non-default widget
constructors for the nodes & leaves (BoxWidget
and OvalWidget).  The bottom-left tree is
built from tree_to_treesegment."""
    twidget = TextWidget(cf.canvas(), text.strip())
    textbox = BoxWidget(cf.canvas(), twidget, fill='white', draggable=1)
    cf.add_widget(textbox, tc3.bbox()[2]+10, tc2.bbox()[3]+10)

    tree4 = Tree.fromstring('(S (NP this tree) (VP (V is) (Adj horizontal)))')
    tc4 = TreeWidget(cf.canvas(), tree4, draggable=1,
                     line_color='brown2', roof_color='brown2',
                     node_font=('helvetica', -12, 'bold'),
                     node_color='brown4', orientation='horizontal')
    tc4.manage()
    cf.add_widget(tc4, tc3.bbox()[2]+10, textbox.bbox()[3]+10)
    tc4.bind_click(orientswitch)
    tc4.bind_click_trees(tc4.toggle_collapsed, 3)

    # Run mainloop
    cf.mainloop()

if __name__ == '__main__':
    demo()