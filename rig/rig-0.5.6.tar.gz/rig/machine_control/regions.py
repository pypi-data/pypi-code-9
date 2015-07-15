"""SpiNNaker machine regions.

Regions are used to specify areas of a SpiNNaker machine for the purposes of
transmitting nearest neighbour packets or for determining which chips should be
included in any flood-fill of data or application loading.

A 32-bit value representing a region uses the top 16 bits (31:16) to represent
the x- and y-coordinates of the region and the level and the lower 16 bits
(15:0) to represent which of the 16 blocks contained within the chunk should be
selected.

A complete introduction and specification of the region system is given in
"Managing Big SpiNNaker Machines" By Steve Temple.
"""
import collections
from six import iteritems


def get_region_for_chip(x, y, level=3):
    """Get the region word for the given chip co-ordinates.

    Parameters
    ----------
    x : int
        x co-ordinate
    y : int
        y co-ordinate
    level : int
        Level of region to build. 0 is the most coarse and 3 is the finest.
        When 3 is used the specified region will ONLY select the given chip,
        for other regions surrounding chips will also be selected.

    Returns
    -------
    int
        A 32-bit value representing the co-ordinates of the chunk of SpiNNaker
        chips that should be selected and the blocks within this chunk that are
        selected.  As long as bits (31:16) are the same these values may be
        OR-ed together to increase the number of sub-blocks selected.
    """
    shift = 6 - 2*level

    bit = ((x >> shift) & 3) + 4*((y >> shift) & 3)  # bit in bits 15:0 to set

    mask = 0xffff ^ ((4 << shift) - 1)  # in {0xfffc, 0xfff0, 0xffc0, 0xff00}
    nx = x & mask  # The mask guarantees that bits 1:0 will be cleared
    ny = y & mask  # The mask guarantees that bits 1:0 will be cleared

    #        sig bits x | sig bits y |  2-bit level  | region select bits
    region = (nx << 24) | (ny << 16) | (level << 16) | (1 << bit)
    return region


def minimise_regions(chips):
    """Create a reduced set of regions by minimising a hierarchy tree.

    Parameters
    ----------
    chips : iterable
        An iterable returning x and y co-ordinate pairs.

    Returns
    -------
    generator
        A generator which yields 32-bit region codes which minimally cover the
        set of given chips.
    """
    t = RegionTree()
    for (x, y) in chips:
        t.add_coordinate(x, y)
    return t.get_regions()


def compress_flood_fill_regions(targets):
    """Generate a reduced set of flood fill parameters.

    Parameters
    ----------
    targets : {(x, y) : set([c, ...]), ...}
        For each used chip a set of core numbers onto which an application
        should be loaded.  E.g., the output of
        :py:func:`~rig.place_and_route.util.build_application_map` when indexed
        by an application.

    Returns
    -------
    generator
        A generator which yields region and core mask pairs indicating
        parameters to use to flood-fill an application.  `region` and
        `core_mask` are both integer representations of bit fields that are
        understood by SCAMP.
    """
    # Build a dictionary mapping core mask -> chips where this should be
    # applied.
    cores_to_targets = collections.defaultdict(set)
    for (x, y), cores in iteritems(targets):
        # Build the core mask
        core_mask = 0x0000
        for c in cores:
            core_mask |= 1 << c

        # Add to the targets dict
        cores_to_targets[core_mask].add((x, y))

    # For each of these cores build the minimal set of regions
    for core_mask, coordinates in iteritems(cores_to_targets):
        regions = minimise_regions(coordinates)
        for r in regions:
            yield (r, core_mask)


class RegionTree(object):
    """A tree structure for use in minimising sets of regions.

    A tree is defined which reflects the definition of SpiNNaker regions like
    so: The tree's root node represents a 256x256 grid of SpiNNaker chips. This
    grid is broken up into 64x64 grids which are represented by the (level 1)
    child nodes of the root.  Each of these level 1 nodes' 64x64 grids are
    broken up into 16x16 grids which are represented by their (level 2)
    children. These level 2 nodes have their 16x16 grids broken up into 4x4
    grids represented by their (level 3) children. Level 3 children explicitly
    list which of their sixteen cores are part of the region.

    If any of a level 2 node's level 3 children have all of their cores
    selected, these level 3 nodes can be removed and replaced by a level 2
    region with the corresponding 4x4 grid selected. If multiple children can
    be replaced with level 2 regions, these can be combined into a single level
    2 region with the corresponding 4x4 grids selected, resulting in a
    reduction in the number of regions required. The same process can be
    repeated at each level of the hierarchy eventually producing a minimal set
    of regions.

    This data structure is specified by supplying a sequence of (x, y)
    coordinates of chips to be represented by a series of regions using
    :py:meth:`.add_coordinate`. This method minimises the tree during insertion
    meaning a minimal set of regions can be extracted by
    :py:meth:`.get_regions` which simply traverses the tree.
    """

    def __init__(self, base_x=0, base_y=0, level=0):
        self.base_x = base_x
        self.base_y = base_y
        self.scale = 4 ** (4 - level)
        self.shift = 6 - 2*level
        self.level = level

        # Each region has locally selected components
        self.locally_selected = set()

        # And possibly contains subregions
        if level < 3:
            self.subregions = [None] * 16

    def get_regions(self):
        """Generate a set of integer region representations.

        Returns
        -------
        generator
            Generator which yields 32-bit region codes as might be generated by
            :py:func:`.get_region_for_chip`.
        """
        region_code = ((self.base_x << 24) | (self.base_y << 16) |
                       (self.level << 16))

        # Build up the returned set of regions
        if self.locally_selected != set():
            elements = 0x0000
            for e in self.locally_selected:
                elements |= 1 << e
            yield (region_code | elements)

        # Include subregions if they exist
        if self.level < 3:
            for i, sr in enumerate(self.subregions):
                if i not in self.locally_selected and sr is not None:
                    for r in sr.get_regions():
                        yield r

    def add_coordinate(self, x, y):
        """Add a new coordinate to the region tree.

        Raises
        ------
        ValueError
            If the co-ordinate is not contained within the region.

        Returns
        -------
        bool
            If all contained subregions are full.
        """
        # Check that the co-ordinate is contained in this region
        if ((x < self.base_x or x >= self.base_x + self.scale) or
                (y < self.base_y or y >= self.base_y + self.scale)):
            raise ValueError((x, y))

        # Determine which subregion this refers to
        subregion = ((x >> self.shift) & 0x3) + 4*((y >> self.shift) & 0x3)

        if self.level == 3:
            # If level-3 then we just add to the locally selected regions
            self.locally_selected.add(subregion)
        else:
            # Otherwise we delegate, if that level is full then we store it as
            # a region that is full.
            if self.subregions[subregion] is None:
                # "Lazy": if the subtree doesn't exist yet then add it
                base_x = int(self.base_x + (self.scale / 4) * (subregion % 4))
                base_y = int(self.base_y + (self.scale / 4) * (subregion // 4))
                self.subregions[subregion] = RegionTree(base_x, base_y,
                                                        self.level + 1)

            if self.subregions[subregion].add_coordinate(x, y):
                self.locally_selected.add(subregion)

        # If "full" then return True (i.e., would be 0x____ffff if converted)
        return self.locally_selected == {i for i in range(16)}
