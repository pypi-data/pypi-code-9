from fanstatic import Library, Resource
import js.d3

library = Library('d3-tip', 'resources')


d3_tip = Resource(
    library, 'd3_tip.js',
    depends=[
        js.d3.d3
    ])