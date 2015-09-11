import re

def get_indentation(content):
    return len(re.match("(^ *)", content).group(0))

class Block:
    def __init__(self, head, parent):
        self._parent = parent
        self.head = head
        if parent:
            self._indentation = get_indentation(head)
        else:
            self._indentation = -1
        self.child_blocks = []

    def _first_child_indentation(self):
        return self.child_blocks[0]._indentation

    def add_content(self, content):
        indentation = get_indentation(content)
        if indentation > self._indentation:
            # If the indentation of the new line is greater than
            # this block, then add the new line below this block.
            if self.child_blocks:
                # If there is content, see if this content has the 
                # same indentation as the very firse line of this block
                # if yes, then add this content to this block or else
                # start a new block. In the former case return this block
                # itself and in the later case, return the new block.
                first_child_indentation = self._first_child_indentation()
                if indentation == first_child_indentation:
                    self.child_blocks.append(Block(content, self))
                    return self
                elif indentation > first_child_indentation:
                    # If the indention shifts to right, then pop the last
                    # line off the children list, (which will be the line
                    # just about this line), and make a new block with this
                    # line as the head. Add the current line as a child of this
                    # new block.
                    child_block = Block(self.child_blocks.pop().head, self)
                    child_block.add_content(content)
                    self.child_blocks.append(child_block)
                    return child_block
                else:
                    raise Exception("Child node with indention greater than parent"
                        " but less than first child found. All child nodes in a block"
                        " must should me indented atleast as much as the first child of"
                        " the block.")
            else:
                # If there are no existing contents, add this content to this
                # block. Also wrap the content in a Block before doing that.
                self.child_blocks.append(Block(content, self))
                return self
        elif self._parent:
            # If the indentation of the new line is less that this block's
            # indentation, then pass the line to parent block
            return self._parent.add_content(content)
        else:
            # If there is no parent, ie this is the root node
            # add the content under this.
            self.child_blocks.append(Block(content, self))
            return self

    def __str__(self):
        return "%s%s" % (self.head if self.head is not None else '',
                ''.join([str(c) for c in self.child_blocks]))

def make_block(lines, escape='"""'):
    gathered_lines = []
    root_block = current_block = None
    gather = False
    root_block = current_block = Block("", None)
    def add_content(content):
        nonlocal root_block, current_block
        if current_block:
            current_block = current_block.add_content(content)
    lc = 1
    for line in lines:
        # If the line starts with the escape word, then
        # gather lines until the escape word appear all
        # by itself in a line
        try:
            striped_line = line.strip()
            if striped_line.endswith(escape) :
                if striped_line == escape:
                    if gather:
                        gather = False
                        add_content(''.join(gathered_lines))
                    else:
                        gather = True
                    continue
                else:
                    line = bytes(line, 'utf-8').decode('unicode-escape')
            if gather:
                gathered_lines.append(line)
                continue
            add_content(line)
        except Exception as e:
            raise Exception("Exception while processing line %s of the input. The line content is \n '%s'" % (lc, line)) from e
        lc += 1

    return root_block
