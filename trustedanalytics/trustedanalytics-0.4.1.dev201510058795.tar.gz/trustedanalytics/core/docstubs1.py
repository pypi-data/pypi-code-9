#
# Copyright (c) 2015 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Auto-generated file for API static documentation stubs (2015-10-05T23:49:05.362218)
#
# **DO NOT EDIT**

from trustedanalytics.meta.docstub import doc_stub, DocStubCalledError



@doc_stub
class _DocStubsEdgeFrame(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, graph=None, label=None, src_vertex_label=None, dest_vertex_label=None, directed=None):
        """
            Examples

        --------
        Given a data file */movie.csv*, create a frame to match this data and move
        the data to the frame.
        Create an empty graph and define some vertex and edge types.

        .. code::

            >>> my_csv = ta.CsvFile("/movie.csv", schema= [('user_id', int32),
            ...                                     ('user_name', str),
            ...                                     ('movie_id', int32),
            ...                                     ('movie_title', str),
            ...                                     ('rating', str)])

            >>> my_frame = ta.Frame(my_csv)
            >>> my_graph = ta.Graph()
            >>> my_graph.define_vertex_type('users')
            >>> my_graph.define_vertex_type('movies')
            >>> my_graph.define_edge_type('ratings','users','movies',directed=True)

        Add data to the graph from the frame:

        .. only:: html

            .. code::

                >>> my_graph.vertices['users'].add_vertices(my_frame, 'user_id', ['user_name'])
                >>> my_graph.vertices['movies].add_vertices(my_frame, 'movie_id', ['movie_title])

        .. only:: latex

            .. code::

                >>> my_graph.vertices['users'].add_vertices(my_frame, 'user_id',
                ... ['user_name'])
                >>> my_graph.vertices['movies'].add_vertices(my_frame, 'movie_id', ['movie_title'])

        Create an edge frame from the graph, and add edge data from the frame.

        .. code::

            >>> my_edge_frame = graph.edges['ratings']
            >>> my_edge_frame.add_edges(my_frame, 'user_id', 'movie_id', ['rating']

        Retrieve a previously defined graph and retrieve an EdgeFrame from it:

        .. code::

            >>> my_old_graph = ta.get_graph("your_graph")
            >>> my_new_edge_frame = my_old_graph.edges["your_label"]

        Calling methods on an EdgeFrame:

        .. code::

            >>> my_new_edge_frame.inspect(20)

        Copy an EdgeFrame to a frame using the copy method:

        .. code::

            >>> my_new_frame = my_new_edge_frame.copy()
            

        :param graph: (default=None)  
        :type graph: 
        :param label: (default=None)  
        :type label: 
        :param src_vertex_label: (default=None)  
        :type src_vertex_label: 
        :param dest_vertex_label: (default=None)  
        :type dest_vertex_label: 
        :param directed: (default=None)  
        :type directed: 
        """
        raise DocStubCalledError("frame:edge/__init__")


    @doc_stub
    def add_columns(self, func, schema, columns_accessed=None):
        """
        Add columns to current frame.

        Assigns data to column based on evaluating a function for each row.

        Notes
        -----
        1)  The row |UDF| ('func') must return a value in the same format as
            specified by the schema.
            See :doc:`/ds_apir`.
        2)  Unicode in column names is not supported and will likely cause the
            drop_frames() method (and others) to fail!

        Examples
        --------
        Given a Frame *my_frame* identifying a data frame with two int32
        columns *column1* and *column2*.
        Add a third column *column3* as an int32 and fill it with the
        contents of *column1* and *column2* multiplied together:

        .. code::

            >>> my_frame.add_columns(lambda row: row.column1*row.column2,
            ... ('column3', int32))

        The frame now has three columns, *column1*, *column2* and *column3*.
        The type of *column3* is an int32, and the value is the product of
        *column1* and *column2*.

        Add a string column *column4* that is empty:

        .. code::

            >>> my_frame.add_columns(lambda row: '', ('column4', str))

        The Frame object *my_frame* now has four columns *column1*, *column2*,
        *column3*, and *column4*.
        The first three columns are int32 and the fourth column is str.
        Column *column4* has an empty string ('') in every row.

        Multiple columns can be added at the same time.
        Add a column *a_times_b* and fill it with the contents of column *a*
        multiplied by the contents of column *b*.
        At the same time, add a column *a_plus_b* and fill it with the contents
        of column *a* plus the contents of column *b*:

        .. only:: html

            .. code::

                >>> my_frame.add_columns(lambda row: [row.a * row.b, row.a + row.b], [("a_times_b", float32), ("a_plus_b", float32))

        .. only:: latex

            .. code::

                >>> my_frame.add_columns(lambda row: [row.a * row.b, row.a +
                ... row.b], [("a_times_b", float32), ("a_plus_b", float32))

        Two new columns are created, "a_times_b" and "a_plus_b", with the
        appropriate contents.

        Given a frame of data and Frame *my_frame* points to it.
        In addition we have defined a |UDF| *func*.
        Run *func* on each row of the frame and put the result in a new int
        column *calculated_a*:

        .. code::

            >>> my_frame.add_columns( func, ("calculated_a", int))

        Now the frame has a column *calculated_a* which has been filled with
        the results of the |UDF| *func*.

        A |UDF| must return a value in the same format as the column is
        defined.
        In most cases this is automatically the case, but sometimes it is less
        obvious.
        Given a |UDF| *function_b* which returns a value in a list, store
        the result in a new column *calculated_b*:

        .. code::

            >>> my_frame.add_columns(function_b, ("calculated_b", float32))

        This would result in an error because function_b is returning a value
        as a single element list like [2.4], but our column is defined as a
        tuple.
        The column must be defined as a list:

        .. code::

            >>> my_frame.add_columns(function_b, [("calculated_b", float32)])

        To run an optimized version of add_columns, columns_accessed parameter can
        be populated with the column names which are being accessed in |UDF|. This
        speeds up the execution by working on only the limited feature set than the
        entire row.

        Let's say a frame has 4 columns named *a*,*b*,*c* and *d* and we want to add a new column
        with value from column *a* multiplied by value in column *b* and call it *a_times_b*.
        In the example below, columns_accessed is a list with column names *a* and *b*.

        .. code::

            >>> my_frame.add_columns(lambda row: row.a * row.b, ("a_times_b", float32), columns_accessed=["a", "b"])

        add_columns would fail if columns_accessed parameter is not populated with the correct list of accessed
        columns. If not specified, columns_accessed defaults to None which implies that all columns might be accessed
        by the |UDF|.

        More information on a row |UDF| can be found at :doc:`/ds_apir`



        :param func: User-Defined Function (|UDF|) which takes the values in the row and produces a value, or collection of values, for the new cell(s).
        :type func: UDF
        :param schema: The schema for the results of the |UDF|, indicating the new column(s) to add.  Each tuple provides the column name and data type, and is of the form (str, type).
        :type schema: tuple | list of tuples
        :param columns_accessed: (default=None)  List of columns which the |UDF| will access.  This adds significant performance benefit if we know which column(s) will be needed to execute the |UDF|, especially when the frame has significantly more columns than those being used to evaluate the |UDF|.
        :type columns_accessed: list
        """
        return None


    @doc_stub
    def add_edges(self, source_frame, column_name_for_source_vertex_id, column_name_for_dest_vertex_id, column_names=None, create_missing_vertices=False):
        """
        Add edges to a graph.

        Includes appending to a list of existing edges.

        Examples
        --------
        Create a frame and add edges:

        .. only:: html

            .. code::

                >>> graph = ta.Graph()
                >>> graph.define_vertex_type('users')
                >>> graph.define_vertex_type('movie')
                >>> graph.define_edge_type('ratings', 'users', 'movies', directed=True)
                >>> graph.add_edges(frame, 'user_id', 'movie_id', ['rating'], create_missing_vertices=True)

        .. only:: latex

            .. code::

                >>> graph = ta.Graph()
                >>> graph.define_vertex_type('users')
                >>> graph.define_vertex_type('movie')
                >>> graph.define_edge_type('ratings', 'users', 'movies', directed=True)
                >>> graph.add_edges(frame, 'user_id', 'movie_id', ['rating'],
                ...     create_missing_vertices=True)




        :param source_frame: Frame that will be the source of
            the edge data.
        :type source_frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        :param column_name_for_source_vertex_id: column name for a unique id for
            each source vertex (this is not the system defined _vid).
        :type column_name_for_source_vertex_id: unicode
        :param column_name_for_dest_vertex_id: column name for a unique id for
            each destination vertex (this is not the system defined _vid).
        :type column_name_for_dest_vertex_id: unicode
        :param column_names: (default=None)  Column names to be used as properties for each vertex,
            None means use all columns,
            empty list means use none.
        :type column_names: list
        :param create_missing_vertices: (default=False)  True to create missing vertices for edge (slightly slower),
            False to drop edges pointing to missing vertices.
            Defaults to False.
        :type create_missing_vertices: bool

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def assign_sample(self, sample_percentages, sample_labels=None, output_column=None, random_seed=None):
        """
        Randomly group rows into user-defined classes.

        Randomly assign classes to rows given a vector of percentages.
        The table receives an additional column that contains a random label.
        The random label is generated by a probability distribution function.
        The distribution function is specified by the sample_percentages, a list of
        floating point values, which add up to 1.
        The labels are non-negative integers drawn from the range
        :math:`[ 0, len(S) - 1]` where :math:`S` is the sample_percentages.

        **Notes**

        The sample percentages provided by the user are preserved to at least eight
        decimal places, but beyond this there may be small changes due to floating
        point imprecision.

        In particular:

        #)  The engine validates that the sum of probabilities sums to 1.0 within
            eight decimal places and returns an error if the sum falls outside of this
            range.
        #)  The probability of the final class is clamped so that each row receives a
            valid label with probability one.

        Examples
        --------
        Given a frame accessed via Frame *my_frame*:

        .. code::

            >>> my_frame.inspect()
              col_nc:str  col_wk:str
            /------------------------/
              abc         zzz
              def         yyy
              ghi         xxx
              jkl         www
              mno         vvv
              pqr         uuu
              stu         ttt
              vwx         sss
              yza         rrr
              bcd         qqq

        To append a new column *sample_bin* to the frame and assign the value in the
        new column to "train", "test", or "validate":

        .. code::

            >>> my_frame.assign_sample([0.3, 0.3, 0.4], ["train", "test", "validate"])
            >>> my_frame.inspect()
              col_nc:str  col_wk:str  sample_bin:str
            /----------------------------------------/
              abc         zzz         validate
              def         yyy         test
              ghi         xxx         test
              jkl         www         test
              mno         vvv         train
              pqr         uuu         validate
              stu         ttt         validate
              vwx         sss         train
              yza         rrr         validate
              bcd         qqq         train

        Now, the frame accessed by the Frame, *my_frame*, has a new column named
        "sample_bin" and each row contains one of the values "train", "test", or
        "validate".
        Values in the other columns are unaffected.



        :param sample_percentages: Entries are non-negative and sum to 1. (See the note below.)
            If the *i*'th entry of the  list is *p*,
            then then each row receives label *i* with independent probability *p*.
        :type sample_percentages: list
        :param sample_labels: (default=None)  Names to be used for the split classes.
            Defaults to "TR", "TE", "VA" when the length of *sample_percentages* is 3,
            and defaults to Sample_0, Sample_1, ... otherwise.
        :type sample_labels: list
        :param output_column: (default=None)  Name of the new column which holds the labels generated by the
            function.
        :type output_column: unicode
        :param random_seed: (default=None)  Random seed used to generate the labels.
            Defaults to 0.
        :type random_seed: int32

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def bin_column(self, column_name, cutoffs, include_lowest=None, strict_binning=None, bin_column_name=None):
        """
        Classify data into user-defined groups.

        Summarize rows of data based on the value in a single column by sorting them
        into bins, or groups, based on a list of bin cutoff points.

        **Notes**

        #)  Unicode in column names is not supported and will likely cause the
            drop_frames() method (and others) to fail!
        #)  Bins IDs are 0-index, in other words, the lowest bin number is 0.
        #)  The first and last cutoffs are always included in the bins.
            When *include_lowest* is ``True``, the last bin includes both cutoffs.
            When *include_lowest* is ``False``, the first bin (bin 0) includes both
            cutoffs.

        Examples
        --------
        For this example, we will use a frame with column *a* accessed by a Frame
        object *my_frame*:

        .. code::

            >>> my_frame.inspect( n=11 )

              a:int32
            /---------/
                1
                1
                2
                3
                5
                8
               13
               21
               34
               55
               89

        Modify the frame with a column showing what bin the data is in.
        The data values should use strict_binning:

        .. code::

            >>> my_frame.bin_column('a', [5,12,25,60], include_lowest=True,
            ... strict_binning=True, bin_column_name='binned')
            >>> my_frame.inspect( n=11 )

              a:int32     binned:int32
            /---------------------------/
                  1               -1
                  1               -1
                  2               -1
                  3               -1
                  5                0
                  8                0
                 13                1
                 21                1
                 34                2
                 55                2
                 89               -1

        Modify the frame with a column showing what bin the data is in.
        The data value should not use strict_binning:

        .. code::

            >>> my_frame.bin_column('a', [5,12,25,60], include_lowest=True,
            ... strict_binning=False, bin_column_name='binned')
            >>> my_frame.inspect( n=11 )

              a:int32     binned:int32
            /---------------------------/
                  1                0
                  1                0
                  2                0
                  3                0
                  5                0
                  8                0
                 13                1
                 21                1
                 34                2
                 55                2
                 89                2


        Modify the frame with a column showing what bin the data is in.
        The bins should be lower inclusive:

        .. code::

            >>> my_frame.bin_column('a', [1,5,34,55,89], include_lowest=True,
            ... strict_binning=False, bin_column_name='binned')
            >>> my_frame.inspect( n=11 )

              a:int32     binned:int32
            /---------------------------/
                  1                0
                  1                0
                  2                0
                  3                0
                  5                1
                  8                1
                 13                1
                 21                1
                 34                2
                 55                3
                 89                3

        Modify the frame with a column showing what bin the data is in.
        The bins should be upper inclusive:

        .. code::

            >>> my_frame.bin_column('a', [1,5,34,55,89], include_lowest=False,
            ... strict_binning=True, bin_column_name='binned')
            >>> my_frame.inspect( n=11 )

              a:int32     binned:int32
            /---------------------------/
               1                   0
               1                   0
               2                   0
               3                   0
               5                   0
               8                   1
              13                   1
              21                   1
              34                   1
              55                   2
              89                   3


        :param column_name: Name of the column to bin.
        :type column_name: unicode
        :param cutoffs: Array of values containing bin cutoff points.
            Array can be list or tuple.
            Array values must be progressively increasing.
            All bin boundaries must be included, so, with N bins, you need N+1 values.
        :type cutoffs: list
        :param include_lowest: (default=None)  Specify how the boundary conditions are handled.
            ``True`` indicates that the lower bound of the bin is inclusive.
            ``False`` indicates that the upper bound is inclusive.
            Default is ``True``.
        :type include_lowest: bool
        :param strict_binning: (default=None)  Specify how values outside of the cutoffs array should be binned.
            If set to ``True``, each value less than cutoffs[0] or greater than
            cutoffs[-1] will be assigned a bin value of -1.
            If set to ``False``, values less than cutoffs[0] will be included in the first
            bin while values greater than cutoffs[-1] will be included in the final
            bin.
        :type strict_binning: bool
        :param bin_column_name: (default=None)  The name for the new binned column.
            Default is ``<column_name>_binned``.
        :type bin_column_name: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def bin_column_equal_depth(self, column_name, num_bins=None, bin_column_name=None):
        """
        Classify column into groups with the same frequency.

        Group rows of data based on the value in a single column and add a label
        to identify grouping.

        Equal depth binning attempts to label rows such that each bin contains the
        same number of elements.
        For :math:`n` bins of a column :math:`C` of length :math:`m`, the bin
        number is determined by:

        .. math::

            \lceil n * \frac { f(C) }{ m } \rceil

        where :math:`f` is a tie-adjusted ranking function over values of
        :math:`C`.
        If there are multiples of the same value in :math:`C`, then their
        tie-adjusted rank is the average of their ordered rank values.

        **Notes**

        #)  Unicode in column names is not supported and will likely cause the
            drop_frames() method (and others) to fail!
        #)  The num_bins parameter is considered to be the maximum permissible number
            of bins because the data may dictate fewer bins.
            For example, if the column to be binned has a quantity of :math"`X`
            elements with only 2 distinct values and the *num_bins* parameter is
            greater than 2, then the actual number of bins will only be 2.
            This is due to a restriction that elements with an identical value must
            belong to the same bin.

        Examples
        --------
        Given a frame with column *a* accessed by a Frame object *my_frame*:

        .. code::

            >>> my_frame.inspect( n=11 )

              a:int32
            /---------/
                1
                1
                2
                3
                5
                8
               13
               21
               34
               55
               89

        Modify the frame, adding a column showing what bin the data is in.
        The data should be grouped into a maximum of five bins.
        Note that each bin will have the same quantity of members (as much as
        possible):

        .. code::

            >>> cutoffs = my_frame.bin_column_equal_depth('a', 5, 'aEDBinned')
            >>> my_frame.inspect( n=11 )

              a:int32     aEDBinned:int32
            /-----------------------------/
                  1                   0
                  1                   0
                  2                   1
                  3                   1
                  5                   2
                  8                   2
                 13                   3
                 21                   3
                 34                   4
                 55                   4
                 89                   4

            >>> print cutoffs
            [1.0, 2.0, 5.0, 13.0, 34.0, 89.0]


        :param column_name: The column whose values are to be binned.
        :type column_name: unicode
        :param num_bins: (default=None)  The maximum number of bins.
            Default is the Square-root choice
            :math:`\lfloor \sqrt{m} \rfloor`, where :math:`m` is the number of rows.
        :type num_bins: int32
        :param bin_column_name: (default=None)  The name for the new column holding the grouping labels.
            Default is ``<column_name>_binned``.
        :type bin_column_name: unicode

        :returns: A list containing the edges of each bin.
        :rtype: dict
        """
        return None


    @doc_stub
    def bin_column_equal_width(self, column_name, num_bins=None, bin_column_name=None):
        """
        Classify column into same-width groups.

        Group rows of data based on the value in a single column and add a label
        to identify grouping.

        Equal width binning places column values into groups such that the values
        in each group fall within the same interval and the interval width for each
        group is equal.

        **Notes**

        #)  Unicode in column names is not supported and will likely cause the
            drop_frames() method (and others) to fail!
        #)  The num_bins parameter is considered to be the maximum permissible number
            of bins because the data may dictate fewer bins.
            For example, if the column to be binned has 10
            elements with only 2 distinct values and the *num_bins* parameter is
            greater than 2, then the number of actual number of bins will only be 2.
            This is due to a restriction that elements with an identical value must
            belong to the same bin.

        Examples
        --------
        Given a frame with column *a* accessed by a Frame object *my_frame*:

        .. code::

            >>> my_frame.inspect( n=11 )

              a:int32
            /---------/
                1
                1
                2
                3
                5
                8
               13
               21
               34
               55
               89

        Modify the frame, adding a column showing what bin the data is in.
        The data should be separated into a maximum of five bins and the bin cutoffs
        should be evenly spaced.
        Note that there may be bins with no members:

        .. code::

            >>> cutoffs = my_frame.bin_column_equal_width('a', 5, 'aEWBinned')
            >>> my_frame.inspect( n=11 )

              a:int32     aEWBinned:int32
            /-----------------------------/
                1                 0
                1                 0
                2                 0
                3                 0
                5                 0
                8                 0
               13                 0
               21                 1
               34                 1
               55                 3
               89                 4

        The method returns a list of 6 cutoff values that define the edges of each bin.
        Note that difference between the cutoff values is constant:

        .. code::

            >>> print cutoffs
            [1.0, 18.6, 36.2, 53.8, 71.4, 89.0]


        :param column_name: The column whose values are to be binned.
        :type column_name: unicode
        :param num_bins: (default=None)  The maximum number of bins.
            Default is the Square-root choice
            :math:`\lfloor \sqrt{m} \rfloor`, where :math:`m` is the number of rows.
        :type num_bins: int32
        :param bin_column_name: (default=None)  The name for the new column holding the grouping labels.
            Default is ``<column_name>_binned``.
        :type bin_column_name: unicode

        :returns: A list of the edges of each bin.
        :rtype: dict
        """
        return None


    @doc_stub
    def categorical_summary(self, column_inputs=None):
        """
        Compute a summary of the data in a column(s) for categorical or numerical data types.

        The returned value is a Map containing categorical summary for each specified column.

        For each column, levels which satisfy the top k and/or threshold cutoffs are displayed along
        with their frequency and percentage occurrence with respect to the total rows in the dataset.

        Missing data is reported when a column value is empty ("") or null.

        All remaining data is grouped together in the Other category and its frequency and percentage are reported as well.

        User must specify the column name and can optionally specify top_k and/or threshold.

        Optional parameters:

            top_k
                Displays levels which are in the top k most frequently occurring values for that column.

            threshold
                Displays levels which are above the threshold percentage with respect to the total row count.

            top_k and threshold
                Performs level pruning first based on top k and then filters out levels which satisfy the threshold criterion.

            defaults
                Displays all levels which are in Top 10.


        Examples
        --------

        .. code::

            >>> frame.categorical_summary('source','target')
            >>> frame.categorical_summary(('source', {'top_k' : 2}))
            >>> frame.categorical_summary(('source', {'threshold' : 0.5}))
            >>> frame.categorical_summary(('source', {'top_k' : 2}), ('target',
            ... {'threshold' : 0.5}))

        Sample output (for last example above):

            >>> {u'categorical_summary': [{u'column': u'source', u'levels': [
            ... {u'percentage': 0.32142857142857145, u'frequency': 9, u'level': u'thing'},
            ... {u'percentage': 0.32142857142857145, u'frequency': 9, u'level': u'abstraction'},
            ... {u'percentage': 0.25, u'frequency': 7, u'level': u'physical_entity'},
            ... {u'percentage': 0.10714285714285714, u'frequency': 3, u'level': u'entity'},
            ... {u'percentage': 0.0, u'frequency': 0, u'level': u'Missing'},
            ... {u'percentage': 0.0, u'frequency': 0, u'level': u'Other'}]},
            ... {u'column': u'target', u'levels': [
            ... {u'percentage': 0.07142857142857142, u'frequency': 2, u'level': u'thing'},
            ... {u'percentage': 0.07142857142857142, u'frequency': 2,
            ...  u'level': u'physical_entity'},
            ... {u'percentage': 0.07142857142857142, u'frequency': 2, u'level': u'entity'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'variable'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'unit'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'substance'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'subject'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'set'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'reservoir'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'relation'},
            ... {u'percentage': 0.0, u'frequency': 0, u'level': u'Missing'},
            ... {u'percentage': 0.5357142857142857, u'frequency': 15, u'level': u'Other'}]}]}



        :param column_inputs: (default=None)  Comma-separated column names to summarize or tuple containing column name and dictionary of optional parameters. Optional parameters (see below for details): top_k (default = 10), threshold (default = 0.0)
        :type column_inputs: str | tuple(str, dict)

        :returns: Summary for specified column(s) consisting of levels with their frequency and percentage
        :rtype: dict
        """
        return None


    @doc_stub
    def classification_metrics(self, label_column, pred_column, pos_label=None, beta=None, frequency_column=None):
        """
        Model statistics of accuracy, precision, and others.

        Calculate the accuracy, precision, confusion_matrix, recall and
        :math:`F_{ \beta}` measure for a classification model.

        *   The **f_measure** result is the :math:`F_{ \beta}` measure for a
            classification model.
            The :math:`F_{ \beta}` measure of a binary classification model is the
            harmonic mean of precision and recall.
            If we let:

            * beta :math:`\equiv \beta`,
            * :math:`T_{P}` denotes the number of true positives,
            * :math:`F_{P}` denotes the number of false positives, and
            * :math:`F_{N}` denotes the number of false negatives

            then:

            .. math::

                F_{ \beta} = (1 + \beta ^ 2) * \frac{ \frac{T_{P}}{T_{P} + F_{P}} * \
                \frac{T_{P}}{T_{P} + F_{N}}}{ \beta ^ 2 * \frac{T_{P}}{T_{P} + \
                F_{P}}  + \frac{T_{P}}{T_{P} + F_{N}}}

            The :math:`F_{ \beta}` measure for a multi-class classification model is
            computed as the weighted average of the :math:`F_{ \beta}` measure for
            each label, where the weight is the number of instances of each label.
            The determination of binary vs. multi-class is automatically inferred
            from the data.

        *   The **recall** result of a binary classification model is the proportion
            of positive instances that are correctly identified.
            If we let :math:`T_{P}` denote the number of true positives and
            :math:`F_{N}` denote the number of false negatives, then the model
            recall is given by :math:`\frac {T_{P}} {T_{P} + F_{N}}`.

            For multi-class classification models, the recall measure is computed as
            the weighted average of the recall for each label, where the weight is
            the number of instances of each label.
            The determination of binary vs. multi-class is automatically inferred
            from the data.

        *   The **precision** of a binary classification model is the proportion of
            predicted positive instances that are correctly identified.
            If we let :math:`T_{P}` denote the number of true positives and
            :math:`F_{P}` denote the number of false positives, then the model
            precision is given by: :math:`\frac {T_{P}} {T_{P} + F_{P}}`.

            For multi-class classification models, the precision measure is computed
            as the weighted average of the precision for each label, where the
            weight is the number of instances of each label.
            The determination of binary vs. multi-class is automatically inferred
            from the data.

        *   The **accuracy** of a classification model is the proportion of
            predictions that are correctly identified.
            If we let :math:`T_{P}` denote the number of true positives,
            :math:`T_{N}` denote the number of true negatives, and :math:`K` denote
            the total number of classified instances, then the model accuracy is
            given by: :math:`\frac{T_{P} + T_{N}}{K}`.

            This measure applies to binary and multi-class classifiers.

        *   The **confusion_matrix** result is a confusion matrix for a
            binary classifier model, formatted for human readability.

        Notes
        -----
        The **confusion_matrix** is not yet implemented for multi-class classifiers.

        Examples
        --------
        Consider the following sample data set in *frame* with actual data
        labels specified in the *labels* column and the predicted labels in the
        *predictions* column:

        .. code::

            >>> frame.inspect()

              a:unicode   b:int32   labels:int32  predictions:int32
            /-------------------------------------------------------/
                red         1              0                  0
                blue        3              1                  0
                blue        1              0                  0
                green       0              1                  1

            >>> cm = frame.classification_metrics(label_column='labels',
            ... pred_column='predictions', pos_label=1, beta=1)

            >>> cm.f_measure

            0.66666666666666663

            >>> cm.recall

            0.5

            >>> cm.accuracy

            0.75

            >>> cm.precision

            1.0

            >>> cm.confusion_matrix

                          Predicted
                         _pos_ _neg__
            Actual  pos |  1     1
                    neg |  0     2



        :param label_column: The name of the column containing the
            correct label for each instance.
        :type label_column: unicode
        :param pred_column: The name of the column containing the
            predicted label for each instance.
        :type pred_column: unicode
        :param pos_label: (default=None)  
        :type pos_label: None
        :param beta: (default=None)  This is the beta value to use for
            :math:`F_{ \beta}` measure (default F1 measure is computed); must be greater than zero.
            Defaults is 1.
        :type beta: float64
        :param frequency_column: (default=None)  The name of an optional column containing the
            frequency of observations.
        :type frequency_column: unicode

        :returns: The data returned is composed of multiple components\:

            |   <object>.accuracy : double
            |   <object>.confusion_matrix : table
            |   <object>.f_measure : double
            |   <object>.precision : double
            |   <object>.recall : double
        :rtype: dict
        """
        return None


    @doc_stub
    def column_median(self, data_column, weights_column=None):
        """
        Calculate the (weighted) median of a column.

        The median is the least value X in the range of the distribution so that
        the cumulative weight of values strictly below X is strictly less than half
        of the total weight and the cumulative weight of values up to and including X
        is greater than or equal to one-half of the total weight.

        All data elements of weight less than or equal to 0 are excluded from the
        calculation, as are all data elements whose weight is NaN or infinite.
        If a weight column is provided and no weights are finite numbers greater
        than 0, None is returned.

        Examples
        --------
        .. code::

            >>> median = frame.column_median('middling column')


        :param data_column: The column whose median is to be calculated.
        :type data_column: unicode
        :param weights_column: (default=None)  The column that provides weights (frequencies)
            for the median calculation.
            Must contain numerical data.
            Default is all items have a weight of 1.
        :type weights_column: unicode

        :returns: varies
                The median of the values.
                If a weight column is provided and no weights are finite numbers greater
                than 0, None is returned.
                The type of the median returned is the same as the contents of the data
                column, so a column of Longs will result in a Long median and a column of
                Floats will result in a Float median.
        :rtype: dict
        """
        return None


    @doc_stub
    def column_mode(self, data_column, weights_column=None, max_modes_returned=None):
        """
        Evaluate the weights assigned to rows.

        Calculate the modes of a column.
        A mode is a data element of maximum weight.
        All data elements of weight less than or equal to 0 are excluded from the
        calculation, as are all data elements whose weight is NaN or infinite.
        If there are no data elements of finite weight greater than 0,
        no mode is returned.

        Because data distributions often have multiple modes, it is possible for a
        set of modes to be returned.
        By default, only one is returned, but by setting the optional parameter
        max_modes_returned, a larger number of modes can be returned.

        Examples
        --------
        .. code::

            >>> mode = frame.column_mode('modum columpne')


        :param data_column: Name of the column supplying the data.
        :type data_column: unicode
        :param weights_column: (default=None)  Name of the column supplying the weights.
            Default is all items have weight of 1.
        :type weights_column: unicode
        :param max_modes_returned: (default=None)  Maximum number of modes returned.
            Default is 1.
        :type max_modes_returned: int32

        :returns: Dictionary containing summary statistics.
                The data returned is composed of multiple components\:

            mode : A mode is a data element of maximum net weight.
                A set of modes is returned.
                The empty set is returned when the sum of the weights is 0.
                If the number of modes is less than or equal to the parameter
                max_modes_returned, then all modes of the data are
                returned.
                If the number of modes is greater than the max_modes_returned
                parameter, only the first max_modes_returned many modes (per a
                canonical ordering) are returned.
            weight_of_mode : Weight of a mode.
                If there are no data elements of finite weight greater than 0,
                the weight of the mode is 0.
                If no weights column is given, this is the number of appearances
                of each mode.
            total_weight : Sum of all weights in the weight column.
                This is the row count if no weights are given.
                If no weights column is given, this is the number of rows in
                the table with non-zero weight.
            mode_count : The number of distinct modes in the data.
                In the case that the data is very multimodal, this number may
                exceed max_modes_returned.


        :rtype: dict
        """
        return None


    @property
    @doc_stub
    def column_names(self):
        """
        Column identifications in the current frame.

        Returns the names of the columns of the current frame.

        Examples
        --------
        Given a Frame object, *my_frame* accessing a frame.
        To get the column names:

        .. code::

            >>> my_columns = my_frame.column_names
            >>> print my_columns

        Now, given there are three columns *col1*,
        *col2*, and *col3*, the result is:

        .. code::

            ["col1", "col2", "col3"]





        :returns: list of names of all the frame's columns
        :rtype: list
        """
        return None


    @doc_stub
    def column_summary_statistics(self, data_column, weights_column=None, use_population_variance=None):
        """
        Calculate multiple statistics for a column.

        Notes
        -----
        Sample Variance
            Sample Variance is computed by the following formula:

            .. math::

                \left( \frac{1}{W - 1} \right) * sum_{i} \
                \left(x_{i} - M \right) ^{2}

            where :math:`W` is sum of weights over valid elements of positive
            weight, and :math:`M` is the weighted mean.

        Population Variance
            Population Variance is computed by the following formula:

            .. math::

                \left( \frac{1}{W} \right) * sum_{i} \
                \left(x_{i} - M \right) ^{2}

            where :math:`W` is sum of weights over valid elements of positive
            weight, and :math:`M` is the weighted mean.

        Standard Deviation
            The square root of the variance.

        Logging Invalid Data
            A row is bad when it contains a NaN or infinite value in either
            its data or weights column.
            In this case, it contributes to bad_row_count; otherwise it
            contributes to good row count.

            A good row can be skipped because the value in its weight
            column is less than or equal to 0.
            In this case, it contributes to non_positive_weight_count, otherwise
            (when the weight is greater than 0) it contributes to
            valid_data_weight_pair_count.

        **Equations**

            .. code::

                bad_row_count + good_row_count = # rows in the frame
                positive_weight_count + non_positive_weight_count = good_row_count

            In particular, when no weights column is provided and all weights are 1.0:

            .. code::

                non_positive_weight_count = 0 and
                positive_weight_count = good_row_count

        Examples
        --------
        .. code::

            >>> stats = frame.column_summary_statistics('data column', 'weight column')



        :param data_column: The column to be statistically summarized.
            Must contain numerical data; all NaNs and infinite values are excluded
            from the calculation.
        :type data_column: unicode
        :param weights_column: (default=None)  Name of column holding weights of
            column values.
        :type weights_column: unicode
        :param use_population_variance: (default=None)  If true, the variance is calculated
            as the population variance.
            If false, the variance calculated as the sample variance.
            Because this option affects the variance, it affects the standard
            deviation and the confidence intervals as well.
            Default is false.
        :type use_population_variance: bool

        :returns: Dictionary containing summary statistics.
            The data returned is composed of multiple components\:

            |   mean : [ double | None ]
            |       Arithmetic mean of the data.
            |   geometric_mean : [ double | None ]
            |       Geometric mean of the data. None when there is a data element <= 0, 1.0 when there are no data elements.
            |   variance : [ double | None ]
            |       None when there are <= 1 many data elements. Sample variance is the weighted sum of the squared distance of each data element from the weighted mean, divided by the total weight minus 1. None when the sum of the weights is <= 1. Population variance is the weighted sum of the squared distance of each data element from the weighted mean, divided by the total weight.
            |   standard_deviation : [ double | None ]
            |       The square root of the variance. None when  sample variance is being used and the sum of weights is <= 1.
            |   total_weight : long
            |       The count of all data elements that are finite numbers. In other words, after excluding NaNs and infinite values.
            |   minimum : [ double | None ]
            |       Minimum value in the data. None when there are no data elements.
            |   maximum : [ double | None ]
            |       Maximum value in the data. None when there are no data elements.
            |   mean_confidence_lower : [ double | None ]
            |       Lower limit of the 95% confidence interval about the mean. Assumes a Gaussian distribution. None when there are no elements of positive weight.
            |   mean_confidence_upper : [ double | None ]
            |       Upper limit of the 95% confidence interval about the mean. Assumes a Gaussian distribution. None when there are no elements of positive weight.
            |   bad_row_count : [ double | None ]
            |       The number of rows containing a NaN or infinite value in either the data or weights column.
            |   good_row_count : [ double | None ]
            |       The number of rows not containing a NaN or infinite value in either the data or weights column.
            |   positive_weight_count : [ double | None ]
            |       The number of valid data elements with weight > 0. This is the number of entries used in the statistical calculation.
            |   non_positive_weight_count : [ double | None ]
            |       The number valid data elements with finite weight <= 0.
        :rtype: dict
        """
        return None


    @doc_stub
    def compute_misplaced_score(self, gravity):
        """


        :param gravity: Similarity measure for computing tension between 2 connected items
        :type gravity: float64

        :returns: 
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def copy(self, columns=None, where=None, name=None):
        """
        Create new frame from current frame.

        Copy frame or certain frame columns entirely or filtered.
        Useful for frame query.

        Examples
        --------
        Build a Frame from a csv file with 5 million rows of data; call the
        frame "cust":

        .. code::

            >>> my_frame = ta.Frame(source="my_data.csv")
            >>> my_frame.name("cust")

        Given the frame has columns *id*, *name*, *hair*, and *shoe*.
        Copy it to a new frame:

        .. code::

            >>> your_frame = my_frame.copy()

        Now we have two frames of data, each with 5 million rows.
        Checking the names:

        .. code::

            >>> print my_frame.name()
            >>> print your_frame.name()

        Gives the results:

        .. code::

            "cust"
            "frame_75401b7435d7132f5470ba35..."

        Now, let's copy *some* of the columns from the original frame:

        .. code::

            >>> our_frame = my_frame.copy(['id', 'hair'])

        Our new frame now has two columns, *id* and *hair*, and has 5 million
        rows.
        Let's try that again, but this time change the name of the *hair*
        column to *color*:

        .. code::

            >>> last_frame = my_frame.copy(('id': 'id', 'hair': 'color'))



        :param columns: (default=None)  If not None, the copy will only include the columns specified. If dict, the string pairs represent a column renaming, {source_column_name: destination_column_name}
        :type columns: str | list of str | dict
        :param where: (default=None)  If not None, only those rows for which the UDF evaluates to True will be copied.
        :type where: function
        :param name: (default=None)  Name of the copied frame
        :type name: str

        :returns: A new Frame of the copied data.
        :rtype: Frame
        """
        return None


    @doc_stub
    def correlation(self, data_column_names):
        """
        Calculate correlation for two columns of current frame.

        Notes
        -----
        This method applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame*, which contains the data

        .. code::

            >>> my_frame.inspect()

             idnum:int32   x1:float32   x2:float32   x3:float32   x4:float32  
           /-------------------------------------------------------------------/
                       0          1.0          4.0          0.0         -1.0  
                       1          2.0          3.0          0.0         -1.0  
                       2          3.0          2.0          1.0         -1.0  
                       3          4.0          1.0          2.0         -1.0  
                       4          5.0          0.0          2.0         -1.0  

        my_frame.correlation computes the common correlation coefficient (Pearson's) on the pair
        of columns provided.
        In this example, the *idnum* and most of the columns have trivial correlations: -1, 0, or +1.
        Column *x3* provides a contrasting coefficient of 3 / sqrt(3) = 0.948683298051 .

        .. code::

            >>> my_frame.correlation(["x1", "x2"])
               -1.0
            >>> my_frame.correlation(["x1", "x4"])
                0.0
            >>> my_frame.correlation(["x2", "x3"])
                -0.948683298051


        :param data_column_names: The names of 2 columns from which
            to compute the correlation.
        :type data_column_names: list

        :returns: Pearson correlation coefficient of the two columns.
        :rtype: dict
        """
        return None


    @doc_stub
    def correlation_matrix(self, data_column_names, matrix_name=None):
        """
        Calculate correlation matrix for two or more columns.

        Notes
        -----
        This method applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame*, which contains the data

        .. code::

            >>> my_frame.inspect()

             idnum:int32   x1:float32   x2:float32   x3:float32   x4:float32  
           /-------------------------------------------------------------------/
                       0          1.0          4.0          0.0         -1.0  
                       1          2.0          3.0          0.0         -1.0  
                       2          3.0          2.0          1.0         -1.0  
                       3          4.0          1.0          2.0         -1.0  
                       4          5.0          0.0          2.0         -1.0  

        my_frame.correlation_matrix computes the common correlation coefficient (Pearson's) on each pair
        of columns in the user-provided list.
        In this example, the *idnum* and most of the columns have trivial correlations: -1, 0, or +1.
        Column *x3* provides a contrasting coefficient of 3 / sqrt(3) = 0.948683298051 .
        The resulting table (specifying all columns) is

        .. code::

            >>> corr_matrix = my_frame.correlation_matrix(my_frame.column_names)
            >>> corr_matrix.inspect()

              idnum:float64       x1:float64        x2:float64        x3:float64   x4:float64  
           ------------------------------------------------------------------------------------
                        1.0              1.0              -1.0    0.948683298051          0.0  
                        1.0              1.0              -1.0    0.948683298051          0.0  
                       -1.0             -1.0               1.0   -0.948683298051          0.0  
             0.948683298051   0.948683298051   -0.948683298051               1.0          0.0  
                        0.0              0.0               0.0               0.0          1.0  



        :param data_column_names: The names of the columns from
            which to compute the matrix.
        :type data_column_names: list
        :param matrix_name: (default=None)  The name for the returned
            matrix Frame.
        :type matrix_name: unicode

        :returns: A Frame with the matrix of the correlation values for the columns.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def count(self, where):
        """
        Counts the number of rows which meet given criteria.

        :param where: |UDF| which evaluates a row to a boolean
        :type where: function

        :returns: number of rows for which the where |UDF| evaluated to True.
        :rtype: int
        """
        return None


    @doc_stub
    def covariance(self, data_column_names):
        """
        Calculate covariance for exactly two columns.

        Notes
        -----
        This method applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column named *obs*:

        .. code::

            >>> cov = my_frame.covariance(['col_0', 'col_1'])
            >>> print(cov)



        :param data_column_names: The names of two columns from which
            to compute the covariance.
        :type data_column_names: list

        :returns: Covariance of the two columns.
        :rtype: dict
        """
        return None


    @doc_stub
    def covariance_matrix(self, data_column_names, matrix_name=None):
        """
        Calculate covariance matrix for two or more columns.

        Notes
        -----
        This function applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame1*, which computes the covariance matrix for three
        numeric columns:

        .. code::

            >>> my_frame1.inspect()

              col_0:int64    col_1:int64   col_3:float64
            \--------------------------------------------\
                1            4             33.4
                2            5             43.7
                3            6             20.1

            >>> cov_matrix = my_frame1.covariance_matrix(['col_0', 'col_1', 'col_2'])
            >>> cov_matrix.inspect()

              col_0:float64    col_1:float64   col_3:float64
            \------------------------------------------------\
                 1.00             1.00            -6.65
                 1.00             1.00            -6.65
                 -6.65           -6.65            139.99

        Consider Frame *my_frame2*, which computes the covariance matrix for a single
        vector column:

        .. code::

            >>> my_frame2.inspect()

              State:unicode             Population_HISTOGRAM:vector
            \-------------------------------------------------------\
                Louisiana               [0.0, 1.0, 0.0, 0.0]
                Georgia                 [0.0, 1.0, 0.0, 0.0]
                Texas                   [0.0, 0.54, 0.46, 0.0]
                Florida                 [0.0, 0.83, 0.17, 0.0]

            >>> cov_matrix = my_frame2.covariance_matrix(['Population_HISTOGRAM'])
            >>> cov_matrix.inspect()

              Population_HISTOGRAM:vector
            \-------------------------------------\
              [0,  0.00000000,  0.00000000,    0]
              [0,  0.04709167, -0.04709167,    0]
              [0, -0.04709167,  0.04709167,    0]
              [0,  0.00000000,  0.00000000,    0]




        :param data_column_names: The names of the column from which to compute the matrix.
            Names should refer to a single column of type vector, or two or more
            columns of numeric scalars.
        :type data_column_names: list
        :param matrix_name: (default=None)  The name of the new
            matrix.
        :type matrix_name: unicode

        :returns: A matrix with the covariance values for the columns.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def cumulative_percent(self, sample_col):
        """
        Add column to frame with cumulative percent sum.

        A cumulative percent sum is computed by sequentially stepping through the
        rows, observing the column values and keeping track of the current percentage of the total sum
        accounted for at the current value.


        Notes
        -----
        This method applies only to columns containing numerical data.
        Although this method will execute for columns containing negative
        values, the interpretation of the result will change (for example,
        negative percentages).

        Examples
        --------
        Consider Frame *my_frame* accessing a frame that contains a single
        column named *obs*:

        .. code::

            >>> my_frame.inspect()

              obs:int32
            /-----------/
                 0
                 1
                 2
                 0
                 1
                 2

        The cumulative percent sum for column *obs* is obtained by:

        .. code::

            >>> my_frame.cumulative_percent('obs')

        The Frame *my_frame* now contains two columns *obs* and
        *obsCumulativePercentSum*.
        They contain the original data and the cumulative percent sum,
        respectively:

        .. code::

            >>> my_frame.inspect()

              obs:int32   obs_cumulative_percent:float64
            /--------------------------------------------/
                 0                             0.0
                 1                             0.16666666
                 2                             0.5
                 0                             0.5
                 1                             0.66666666
                 2                             1.0



        :param sample_col: The name of the column from which to compute
            the cumulative percent sum.
        :type sample_col: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def cumulative_sum(self, sample_col):
        """
        Add column to frame with cumulative percent sum.

        A cumulative sum is computed by sequentially stepping through the rows,
        observing the column values and keeping track of the cumulative sum for each value.

        Notes
        -----
        This method applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column named *obs*:

        .. code::

             >>> my_frame.inspect()

               obs:int32
             /-----------/
                  0
                  1
                  2
                  0
                  1
                  2

        The cumulative sum for column *obs* is obtained by:

        .. code::

            >>> my_frame.cumulative_sum('obs')

        The Frame *my_frame* accesses the original frame that now contains two
        columns, *obs* that contains the original column values, and
        *obsCumulativeSum* that contains the cumulative percent count:

        .. code::

            >>> my_frame.inspect()

              obs:int32   obs_cumulative_sum:int32
            /--------------------------------------/
                 0                          0
                 1                          1
                 2                          3
                 0                          3
                 1                          4
                 2                          6



        :param sample_col: The name of the column from which to compute
            the cumulative sum.
        :type sample_col: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def dot_product(self, left_column_names, right_column_names, dot_product_column_name, default_left_values=None, default_right_values=None):
        """
        Calculate dot product for each row in current frame.

        Calculate the dot product for each row in a frame using values from two
        equal-length sequences of columns.

        Dot product is computed by the following formula:

        The dot product of two vectors :math:`A=[a_1, a_2, ..., a_n]` and
        :math:`B =[b_1, b_2, ..., b_n]` is :math:`a_1*b_1 + a_2*b_2 + ...+ a_n*b_n`.
        The dot product for each row is stored in a new column in the existing frame.

        Notes
        -----
        If default_left_values or default_right_values are not specified, any null
        values will be replaced by zeros.

        Examples
        --------
        Calculate the dot product for a sequence of columns in Frame object *my_frame*:

        .. code::

             >>> my_frame.inspect()

               col_0:int32  col_1:float64  col_2:int32  col3:int32
             /-----------------------------------------------------/
               1            0.2            -2           5
               2            0.4            -1           6
               3            0.6             0           7
               4            0.8             1           8
               5            None            2           None

        Modify the frame by computing the dot product for a sequence of columns:

        .. code::

             >>> my_frame.dot_product(['col_0','col_1'], ['col_2', 'col_3'], 'dot_product')
             >>> my_frame.inspect()

               col_0:int32  col_1:float64 col_2:int32 col3:int32  dot_product:float64
             /------------------------------------------------------------------------/
               1            0.2           -2          5            -1.0
               2            0.4           -1          6             0.4
               3            0.6            0          7             4.2
               4            0.8            1          8            10.4
               5            None           2          None         10.0

        Modify the frame by computing the dot product with default values for nulls:

        .. only:: html

            .. code::

                 >>> my_frame.dot_product(['col_0','col_1'], ['col_2', 'col_3'], 'dot_product_2', [0.1, 0.2], [0.3, 0.4])
                 >>> my_frame.inspect()

                   col_0:int32  col_1:float64 col_2:int32 col3:int32  dot_product:float64  dot_product_2:float64
                 /--------------------------------------------------------------------------------------------/
                    1            0.2           -2          5            -1.0               -1.0
                    2            0.4           -1          6             0.4                0.4
                    3            0.6            0          7             4.2                4.2
                    4            0.8            1          8            10.4                10.4
                    5            None           2          None         10.0                10.08

        .. only:: latex

            .. code::

                 >>> my_frame.dot_product(['col_0','col_1'], ['col_2', 'col_3'],
                 ... 'dot_product_2', [0.1, 0.2], [0.3, 0.4])
                 >>> my_frame.inspect()

                   col_0  col_1    col_2  col3   dot_product  dot_product_2
                   int32  float64  int32  int32  float64      float64
                 /----------------------------------------------------------/
                    1     0.2      -2     5         -1.0         -1.0
                    2     0.4      -1     6          0.4          0.4
                    3     0.6       0     7          4.2          4.2
                    4     0.8       1     8         10.4          10.4
                    5     None      2     None      10.0          10.08

        Calculate the dot product for columns of vectors in Frame object *my_frame*:

        .. code::

             >>> my_frame.dot_product('col_4', 'col_5, 'dot_product')

             col_4:vector  col_5:vector  dot_product:float64
             /----------------------------------------------/
              [1, 0.2]     [-2, 5]       -1.0
              [2, 0.4]     [-1, 6]        0.4
              [3, 0.6]     [0,  7]        4.2
              [4, 0.8]     [1,  8]       10.4


        :param left_column_names: Names of columns used to create the left vector (A) for each row.
            Names should refer to a single column of type vector, or two or more
            columns of numeric scalars.
        :type left_column_names: list
        :param right_column_names: Names of columns used to create right vector (B) for each row.
            Names should refer to a single column of type vector, or two or more
            columns of numeric scalars.
        :type right_column_names: list
        :param dot_product_column_name: Name of column used to store the
            dot product.
        :type dot_product_column_name: unicode
        :param default_left_values: (default=None)  Default values used to substitute null values in left vector.
            Default is None.
        :type default_left_values: list
        :param default_right_values: (default=None)  Default values used to substitute null values in right vector.
            Default is None.
        :type default_right_values: list

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def download(self, n=100, offset=0, columns=None):
        """
        Download a frame from the server into client workspace.

        Copies an trustedanalytics Frame into a Pandas DataFrame.


        Examples
        --------
        Frame *my_frame* accesses a frame with millions of rows of data.
        Get a sample of 500 rows:

        .. code::

            >>> pandas_frame = my_frame.download( 500 )

        We now have a new frame accessed by a pandas DataFrame *pandas_frame*
        with a copy of the first 500 rows of the original frame.

        If we use the method with an offset like:

        .. code::

            >>> pandas_frame = my_frame.take( 500, 100 )

        We end up with a new frame accessed by the pandas DataFrame
        *pandas_frame* again, but this time it has a copy of rows 101 to 600 of
        the original frame.



        :param n: (default=100)  The number of rows to download to the client
        :type n: int
        :param offset: (default=0)  The number of rows to skip before copying
        :type offset: int
        :param columns: (default=None)  Column filter, the names of columns to be included (default is all columns)
        :type columns: list

        :returns: A new pandas dataframe object containing the downloaded frame data
        :rtype: pandas.DataFrame
        """
        return None


    @doc_stub
    def drop_columns(self, columns):
        """
        Remove columns from the frame.

        The data from the columns is lost.

        Notes
        -----
        It is not possible to delete all columns from a frame.
        At least one column needs to remain.
        If it is necessary to delete all columns, then delete the frame.

        Examples
        --------
        For this example, Frame object *my_frame* accesses a frame with
        columns *column_a*, *column_b*, *column_c* and *column_d*.

        .. only:: html

            .. code::

                >>> print my_frame.schema
                [("column_a", str), ("column_b", ta.int32), ("column_c", str), ("column_d", ta.int32)]

        .. only:: latex

            .. code::

                >>> print my_frame.schema
                [("column_a", str), ("column_b", ta.int32), ("column_c", str),
                ("column_d", ta.int32)]

        Eliminate columns *column_b* and *column_d*:

        .. code::

            >>> my_frame.drop_columns(["column_b", "column_d"])
            >>> print my_frame.schema
            [("column_a", str), ("column_c", str)]


        Now the frame only has the columns *column_a* and *column_c*.
        For further examples, see: ref:`example_frame.drop_columns`.




        :param columns: Column name OR list of column names to be removed from the frame.
        :type columns: list

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def drop_duplicates(self, unique_columns=None):
        """
        Modify the current frame, removing duplicate rows.

        Remove data rows which are the same as other rows.
        The entire row can be checked for duplication, or the search for duplicates
        can be limited to one or more columns.
        This modifies the current frame.

        Examples
        --------
        Given a Frame *my_frame* with data:

        .. code::

            >>> my_frame.inspect(11)
              a:int32   b:int32   c:int32
            /-------------------------------/
                  200         4        25
                  200         5        25
                  200         4        25
                  200         5        35
                  200         6        25
                  200         8        35
                  200         4        45
                  200         4        25
                  200         5        25
                  200         5        35
                  201         4        25

        Remove any rows that are identical to a previous row.
        The result is a frame of unique rows.
        Note that row order may change.

        .. code::

            >>> my_frame.drop_duplicates()
            >>> my_frame.inspect(11)
              a:int32   b:int32   c:int32
            /-------------------------------/
                  200         4        25
                  200         6        25
                  200         4        45
                  201         4        25
                  200         5        35
                  200         5        25
                  200         8        35

        Instead of that, remove any rows that have the same data in columns *a* and 
        *c* as a previously checked row:

        .. code::

           >>> my_frame.drop_duplicates([ "a", "c"])

        The result is a frame with unique values for the combination of columns *a*
        and *c*.

        .. code::

            >>>my_frame.inspect(11)
              a:int32   b:int32   c:int32
            /-------------------------------/
                  200         4        45
                  200         4        25
                  200         8        35
                  201         4        25

        Remove any rows that have the same data in column *b* as a previously
        checked row:

        .. code::

            >>> my_frame.drop_duplicates("b")

        The result is a frame with unique values in column *b*.

        .. code::

              a:int32   b:int32   c:int32
            /-------------------------------/
                  200         8        35  
                  200         4        45  


        :param unique_columns: (default=None)  
        :type unique_columns: None

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def drop_rows(self, predicate):
        """
        Erase any row in the current frame which qualifies.

        Examples
        --------
        For this example, my_frame is a Frame object accessing a frame with
        lots of data for the attributes of ``lions``, ``tigers``, and
        ``ligers``.
        Get rid of the ``lions`` and ``tigers``:

        .. code::

            >>> my_frame.drop_rows(lambda row: row.animal_type == "lion" or
            ...    row.animal_type == "tiger")

        Now the frame only has information about ``ligers``.

        More information on a |UDF| can be found at :doc:`/ds_apir`.




        :param predicate: |UDF| which evaluates a row to a boolean; rows that answer True are dropped from the Frame
        :type predicate: function
        """
        return None


    @doc_stub
    def ecdf(self, column, result_frame_name=None):
        """
        Builds new frame with columns for data and distribution.

        Generates the empirical cumulative distribution for the input column.

        Examples
        --------
        Consider the following sample data set in *frame* with actual data labels
        specified in the *labels* column and the predicted labels in the
        *predictions* column:

        .. code::

            >>> import trustedanalytics as ta
            >>> import pandas as p
            >>> f = ta.Frame(ta.Pandas(p.DataFrame([1, 3, 1, 0]), [('numbers', ta.int32)]))

            [==Job Progress...]

            >>> f.take(5)
            [[1], [3], [1], [0]]

            [==Job Progress...]

            >>> result = f.ecdf('numbers')
            >>> result.inspect()

              b:int32   b_ECDF:float64
            /--------------------------/
               1             0.2
               2             0.5
               3             0.8
               4             1.0



        :param column: The name of the input column containing sample.
        :type column: unicode
        :param result_frame_name: (default=None)  A name for the resulting frame which is created
            by this operation.
        :type result_frame_name: unicode

        :returns: A new Frame containing each distinct value in the sample and its corresponding ECDF value.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def entropy(self, data_column, weights_column=None):
        """
        Calculate the Shannon entropy of a column.

        The data column is weighted via the weights column.
        All data elements of weight <= 0 are excluded from the calculation, as are
        all data elements whose weight is NaN or infinite.
        If there are no data elements with a finite weight greater than 0,
        the entropy is zero.

        Examples
        --------
        Given a frame of coin flips, half heads and half tails, the entropy is simply ln(2):
        .. code::

            >>> print frame.inspect()

                      data:unicode  
                    /----------------/
                      H             
                      T             
                      H             
                      T             
                      H             
                      T             
                      H             
                      T             
                      H             
                      T             

            >>> print "Computed entropy:", frame.entropy("data")

                    Computed entropy: 0.69314718056

        If we have more choices and weights, the computation is not as simple.
        An on-line search for "Shannon Entropy" will provide more detail.

        .. code::

           >>> print frame.inspect()
                      data:int32   weight:int32  
                    -----------------------------
                               0              1  
                               1              2  
                               2              4  
                               4              8  

           >>> print "Computed entropy:", frame.entropy("data", "weight")

                    Computed entropy: 1.13691659183



        :param data_column: The column whose entropy is to be calculated.
        :type data_column: unicode
        :param weights_column: (default=None)  The column that provides weights (frequencies) for the entropy calculation.
            Must contain numerical data.
            Default is using uniform weights of 1 for all items.
        :type weights_column: unicode

        :returns: Entropy.
        :rtype: dict
        """
        return None


    @doc_stub
    def export_to_csv(self, folder_name, separator=None, count=None, offset=None):
        """
        Write current frame to HDFS in csv format.

        Export the frame to a file in csv format as a Hadoop file.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_csv('covarianceresults')



        :param folder_name: The HDFS folder path where the files
            will be created.
        :type folder_name: unicode
        :param separator: (default=None)  
        :type separator: None
        :param count: (default=None)  The number of records you want.
            Default, or a non-positive value, is the whole frame.
        :type count: int32
        :param offset: (default=None)  The number of rows to skip before exporting to the file.
            Default is zero (0).
        :type offset: int32

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def export_to_hbase(self, table_name, key_column_name=None, family_name=None):
        """
        Write current frame to HBase table.

        Table must exist in HBase.
        Export of Vectors is not currently supported.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_hbase('covarianceresults')



        :param table_name: The name of the HBase table that will contain the exported frame
        :type table_name: unicode
        :param key_column_name: (default=None)  The name of the column to be used as row key in hbase table
        :type key_column_name: unicode
        :param family_name: (default=None)  The family name of the HBase table that will contain the exported frame
        :type family_name: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def export_to_hive(self, table_name):
        """
        Write current frame to Hive table.

        Table must not exist in Hive.
        Export of Vectors is not currently supported.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_hive('covarianceresults')

        :param table_name: The name of the Hive table that will contain the exported frame
        :type table_name: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def export_to_jdbc(self, table_name, connector_type=None, url=None, driver_name=None, query=None):
        """
        Write current frame to JDBC table.

        Table will be created or appended to.
        Export of Vectors is not currently supported.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_jdbc('covarianceresults')



        :param table_name: JDBC table name
        :type table_name: unicode
        :param connector_type: (default=None)  (optional) JDBC connector type
        :type connector_type: unicode
        :param url: (default=None)  (optional) connection url (includes server name, database name, user acct and password
        :type url: unicode
        :param driver_name: (default=None)  (optional) driver name
        :type driver_name: unicode
        :param query: (default=None)  (optional) query for filtering. Not supported yet.
        :type query: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def export_to_json(self, folder_name, count=None, offset=None):
        """
        Write current frame to HDFS in JSON format.

        Export the frame to a file in JSON format as a Hadoop file.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_json('covarianceresults')



        :param folder_name: The HDFS folder path where the files
            will be created.
        :type folder_name: unicode
        :param count: (default=None)  The number of records you want.
            Default, or a non-positive value, is the whole frame.
        :type count: int32
        :param offset: (default=None)  The number of rows to skip before exporting to the file.
            Default is zero (0).
        :type offset: int32

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def filter(self, predicate):
        """
        Select all rows which satisfy a predicate.

        Modifies the current frame to save defined rows and delete everything
        else.

        Examples
        --------
        For this example, *my_frame* is a Frame object with lots of data for
        the attributes of ``lizards``, ``frogs``, and ``snakes``.
        Get rid of everything, except information about ``lizards`` and
        ``frogs``:

        .. code::

            >>> def my_filter(row):
            ... return row['animal_type'] == 'lizard' or
            ... row['animal_type'] == "frog"

            >>> my_frame.filter(my_filter)

        The frame now only has data about ``lizards`` and ``frogs``.

        More information on a |UDF| can be found at :doc:`/ds_apir`.



        :param predicate: |UDF| which evaluates a row to a boolean; rows that answer False are dropped from the Frame
        :type predicate: function
        """
        return None


    @doc_stub
    def flatten_column(self, column, delimiter=None):
        """
        Spread data to multiple rows based on cell data.

        Splits cells in the specified column into multiple rows according to a string
        delimiter.
        New rows are a full copy of the original row, but the specified column only
        contains one value.
        The original row is deleted.

        Examples
        --------
        Given a data file::

            1-"solo,mono,single"
            2-"duo,double"

        The commands to bring the data into a frame, where it can be worked on:

        .. only:: html

            .. code::

                >>> my_csv = CsvFile("original_data.csv", schema=[('a', int32), ('b', str)], delimiter='-')
                >>> my_frame = Frame(source=my_csv)

        .. only:: latex

            .. code::

                >>> my_csv = CsvFile("original_data.csv", schema=[('a', int32),
                ... ('b', str)], delimiter='-')
                >>> my_frame = Frame(source=my_csv)

        Looking at it:

        .. code::

            >>> my_frame.inspect()

              a:int32   b:str
            /-------------------------------/
                1       solo, mono, single
                2       duo, double

        Now, spread out those sub-strings in column *b*:

        .. code::

            >>> my_frame.flatten_column('b')

        Check again:

        .. code::

            >>> my_frame.inspect()

              a:int32   b:str
            /------------------/
                1       solo
                1       mono
                1       single
                2       duo
                2       double



        :param column: The column to be flattened.
        :type column: unicode
        :param delimiter: (default=None)  The delimiter string.
            Default is comma (,).
        :type delimiter: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def get_error_frame(self):
        """
        Get a frame with error recordings.

        When a frame is created, another frame is transparently
        created to capture parse errors.

        Returns
        -------
        Frame : error frame object
            A new object accessing a frame that contains the parse errors of
            the currently active Frame or None if no error frame exists.



        """
        return None


    @doc_stub
    def group_by(self, group_by_columns, aggregation_arguments=None):
        """
        Create summarized frame.

        Creates a new frame and returns a Frame object to access it.
        Takes a column or group of columns, finds the unique combination of
        values, and creates unique rows with these column values.
        The other columns are combined according to the aggregation
        argument(s).

        Notes
        -----
        *   Column order is not guaranteed when columns are added
        *   The column names created by aggregation functions in the new frame
            are the original column name appended with the '_' character and
            the aggregation function.
            For example, if the original field is *a* and the function is
            *avg*, the resultant column is named *a_avg*.
        *   An aggregation argument of *count* results in a column named
            *count*.
        *   The aggregation function *agg.count* is the only full row
            aggregation function supported at this time.
        *   Aggregation currently supports using the following functions:

            *   avg
            *   count
            *   count_distinct
            *   max
            *   min
            *   stdev
            *   sum
            *   var (see glossary Bias vs Variance)

        Examples
        --------
        For setup, we will use a Frame *my_frame* accessing a frame with a
        column *a*:

        .. code::

            >>> my_frame.inspect()

              a:str
            /-------/
              cat
              apple
              bat
              cat
              bat
              cat

        Create a new frame, combining similar values of column *a*,
        and count how many of each value is in the original frame:

        .. code::

            >>> new_frame = my_frame.group_by('a', agg.count)
            >>> new_frame.inspect()

              a:str       count:int
            /-----------------------/
              cat             3
              apple           1
              bat             2

        In this example, 'my_frame' is accessing a frame with three columns,
        *a*, *b*, and *c*:

        .. code::

            >>> my_frame.inspect()

              a:int   b:str   c:float
            /-------------------------/
              1       alpha     3.0
              1       bravo     5.0
              1       alpha     5.0
              2       bravo     8.0
              2       bravo    12.0

        Create a new frame from this data, grouping the rows by unique
        combinations of column *a* and *b*.
        Average the value in *c* for each group:

        .. code::

            >>> new_frame = my_frame.group_by(['a', 'b'], {'c' : agg.avg})
            >>> new_frame.inspect()

              a:int   b:str   c_avg:float
            /-----------------------------/
              1       alpha     4.0
              1       bravo     5.0
              2       bravo    10.0

        For this example, we use *my_frame* with columns *a*, *c*, *d*,
        and *e*:

        .. code::

            >>> my_frame.inspect()

              a:str   c:int   d:float e:int
            /-------------------------------/
              ape     1       4.0     9
              ape     1       8.0     8
              big     1       5.0     7
              big     1       6.0     6
              big     1       8.0     5

        Create a new frame from this data, grouping the rows by unique
        combinations of column *a* and *c*.
        Count each group; for column *d* calculate the average, sum and minimum
        value.
        For column *e*, save the maximum value:

        .. only:: html

            .. code::

                >>> new_frame = my_frame.group_by(['a', 'c'], agg.count, {'d': [agg.avg, agg.sum, agg.min], 'e': agg.max})

                  a:str   c:int   count:int  d_avg:float  d_sum:float   d_min:float   e_max:int
                /-------------------------------------------------------------------------------/
                  ape     1       2          6.0          12.0          4.0           9
                  big     1       3          6.333333     19.0          5.0           7

        .. only:: latex

            .. code::

                >>> new_frame = my_frame.group_by(['a', 'c'], agg.count,
                ... {'d': [agg.avg, agg.sum, agg.min], 'e': agg.max})

                  a    c    count  d_avg  d_sum  d_min  e_max
                  str  int  int    float  float  float  int
                /---------------------------------------------/
                  ape  1    2      6.0    12.0   4.0    9
                  big  1    3      6.333  19.0   5.0    7


        For further examples, see :ref:`example_frame.group_by`.


        :param group_by_columns: Column name or list of column names
        :type group_by_columns: list
        :param aggregation_arguments: (default=None)  Aggregation function based on entire row, and/or dictionaries (one or more) of { column name str : aggregation function(s) }.
        :type aggregation_arguments: dict

        :returns: A new frame with the results of the group_by
        :rtype: Frame
        """
        return None


    @doc_stub
    def histogram(self, column_name, num_bins=None, weight_column_name=None, bin_type='equalwidth'):
        """
        Compute the histogram for a column in a frame.

        Compute the histogram of the data in a column.
        The returned value is a Histogram object containing 3 lists one each for:
        the cutoff points of the bins, size of each bin, and density of each bin.

        **Notes**

        The num_bins parameter is considered to be the maximum permissible number
        of bins because the data may dictate fewer bins.
        With equal depth binning, for example, if the column to be binned has 10
        elements with only 2 distinct values and the *num_bins* parameter is
        greater than 2, then the number of actual number of bins will only be 2.
        This is due to a restriction that elements with an identical value must
        belong to the same bin.

        Examples
        --------
        Consider the following sample data set\:

        .. code::

            >>> frame.inspect()

              a:unicode  b:int32
            /--------------------/
                a          2
                b          7
                c          3
                d          9
                e          1

        A simple call for 3 equal-width bins gives\:

        .. code::

            >>> hist = frame.histogram("b", num_bins=3)
            >>> print hist

            Histogram:
                cutoffs: cutoffs: [1.0, 3.6666666666666665, 6.333333333333333, 9.0],
                hist: [3, 0, 2],
                density: [0.6, 0.0, 0.4]


        Switching to equal depth gives\:

        .. code::

            >>> hist = frame.histogram("b", num_bins=3, bin_type='equaldepth')
            >>> print hist

            Histogram:
                cutoffs: [1, 2, 7, 9],
                hist: [1, 2, 2],
                density: [0.2, 0.4, 0.4]


        .. only:: html

               Plot hist as a bar chart using matplotlib\:

            .. code::

                >>> import matplotlib.pyplot as plt

                >>> plt.bar(hist.cutoffs[:1], hist.hist, width=hist.cutoffs[1] - hist.cutoffs[0])

        .. only:: latex

               Plot hist as a bar chart using matplotlib\:

            .. code::

                >>> import matplotlib.pyplot as plt

                >>> plt.bar(hist.cutoffs[:1], hist.hist, width=hist.cutoffs[1] - 
                ... hist.cutoffs[0])



        :param column_name: Name of column to be evaluated.
        :type column_name: unicode
        :param num_bins: (default=None)  Number of bins in histogram.
            Default is Square-root choice will be used
            (in other words math.floor(math.sqrt(frame.row_count)).
        :type num_bins: int32
        :param weight_column_name: (default=None)  Name of column containing weights.
            Default is all observations are weighted equally.
        :type weight_column_name: unicode
        :param bin_type: (default=equalwidth)  The type of binning algorithm to use: ["equalwidth"|"equaldepth"]
            Defaults is "equalwidth".
        :type bin_type: unicode

        :returns: histogram
                A Histogram object containing the result set.
                The data returned is composed of multiple components:
            cutoffs : array of float
                A list containing the edges of each bin.
            hist : array of float
                A list containing count of the weighted observations found in each bin.
            density : array of float
                A list containing a decimal containing the percentage of
                observations found in the total set per bin.
        :rtype: dict
        """
        return None


    @doc_stub
    def inspect(self, n=10, offset=0, columns=None, wrap='inspect_settings', truncate='inspect_settings', round='inspect_settings', width='inspect_settings', margin='inspect_settings', with_types='inspect_settings'):
        """
        Pretty-print of the frame data

        Essentially returns a string, but technically returns a RowInspection object which renders a string.
        The RowInspection object naturally converts to a str when needed, like when printed or when displayed
        by python REPL (i.e. using the object's __repr__).  If running in a script and want the inspect output
        to be printed, then it must be explicitly printed, then `print frame.inspect()`

        Examples
        --------
        Given a frame of data and a Frame to access it.
        To look at the first 4 rows of data:

        .. code::

            >>> my_frame.inspect(4)
           [#]    animal      name    age     weight
           =========================================
           [0]  human       George      8      542.5
           [1]  human       Ursula      6      495.0
           [2]  ape         Ape        41      400.0
           [3]  elephant    Shep        5     8630.0

        # For other examples, see :ref:`example_frame.inspect`.

        **Global Settings**

        If not specified, the arguments that control formatting receive default values from
        'trustedanalytics.inspect_settings'.  Make changes there to affect all calls to inspect.

        .. code::

            >>> import trustedanalytics as ta
            >>> ta.inspect_settings
            wrap             20
            truncate       None
            round          None
            width            80
            margin         None
            with_types    False
            >>> ta.inspect_settings.width = 120  # changes inspect to use 120 width globally
            >>> ta.inspect_settings.truncate = 16  # changes inspect to always truncate strings to 16 chars
            >>> ta.inspect_settings
            wrap             20
            truncate         16
            round          None
            width           120
            margin         None
            with_types    False
            >>> ta.inspect_settings.width = None  # return value back to default
            >>> ta.inspect_settings
            wrap             20
            truncate         16
            round          None
            width            80
            margin         None
            with_types    False
            >>> ta.inspect_settings.reset()  # set everything back to default
            >>> ta.inspect_settings
            wrap             20
            truncate       None
            round          None
            width            80
            margin         None
            with_types    False

        ..


        :param n: (default=10)  The number of rows to print.
        :type n: int
        :param offset: (default=0)  The number of rows to skip before printing.
        :type offset: int
        :param columns: (default=None)  Filter columns to be included.  By default, all columns are included
        :type columns: int
        :param wrap: (default=inspect_settings)  If set to 'stripes' then inspect prints rows in stripes; if set to an integer N, rows will be printed in clumps of N columns, where the columns are wrapped
        :type wrap: int or 'stripes'
        :param truncate: (default=inspect_settings)  If set to integer N, all strings will be truncated to length N, including a tagged ellipses
        :type truncate: int
        :param round: (default=inspect_settings)  If set to integer N, all floating point numbers will be rounded and truncated to N digits
        :type round: int
        :param width: (default=inspect_settings)  If set to integer N, the print out will try to honor a max line width of N
        :type width: int
        :param margin: (default=inspect_settings)  ('stripes' mode only) If set to integer N, the margin for printing names in a stripe will be limited to N characters
        :type margin: int
        :param with_types: (default=inspect_settings)  If set to True, header will include the data_type of each column
        :type with_types: bool

        :returns: An object which naturally converts to a pretty-print string
        :rtype: RowsInspection
        """
        return None


    @doc_stub
    def join(self, right, left_on, right_on=None, how='inner', name=None):
        """
        Join operation on one or two frames, creating a new frame.

        Create a new frame from a SQL JOIN operation with another frame.
        The frame on the 'left' is the currently active frame.
        The frame on the 'right' is another frame.
        This method takes a column in the left frame and matches its values
        with a column in the right frame.
        Using the default 'how' option ['inner'] will only allow data in the
        resultant frame if both the left and right frames have the same value
        in the matching column.
        Using the 'left' 'how' option will allow any data in the resultant
        frame if it exists in the left frame, but will allow any data from the
        right frame if it has a value in its column which matches the value in
        the left frame column.
        Using the 'right' option works similarly, except it keeps all the data
        from the right frame and only the data from the left frame when it
        matches.
        The 'outer' option provides a frame with data from both frames where
        the left and right frames did not have the same value in the matching
        column.

        Notes
        -----
        When a column is named the same in both frames, it will result in two
        columns in the new frame.
        The column from the *left* frame (originally the current frame) will be
        copied and the column name will have the string "_L" added to it.
        The same thing will happen with the column from the *right* frame,
        except its name has the string "_R" appended. The order of columns
        after this method is called is not guaranteed.

        It is recommended that you rename the columns to meaningful terms prior
        to using the ``join`` method.
        Keep in mind that unicode in column names will likely cause the
        drop_frames() method (and others) to fail!

        Examples
        --------
        For this example, we will use a Frame *my_frame* accessing a frame with
        columns *a*, *b*, *c*, and a Frame *your_frame* accessing a frame with
        columns *a*, *d*, *e*.
        Join the two frames keeping only those rows having the same value in
        column *a*:

        .. code::

            >>> print my_frame.inspect()

              a:unicode   b:unicode   c:unicode
            /--------------------------------------/
              alligator   bear        cat
              apple       berry       cantaloupe
              auto        bus         car
              mirror      frog        ball

            >>> print your_frame.inspect()

              b:unicode   c:int   d:unicode
            /-------------------------------------/
              berry        5218   frog
              blue            0   log
              bus           871   dog

            >>> joined_frame = my_frame.join(your_frame, 'b', how='inner')

        Now, joined_frame is a Frame accessing a frame with the columns *a*,
        *b*, *c_L*, *ci_R*, and *d*.
        The data in the new frame will be from the rows where column 'a' was
        the same in both frames.

        .. code::

            >>> print joined_frame.inspect()

              a:unicode   b:unicode     c_L:unicode   c_R:int64   d:unicode
            /-------------------------------------------------------------------/
              apple       berry         cantaloupe         5218   frog
              auto        bus           car                 871   dog

        More examples can be found in the :ref:`user manual
        <example_frame.join>`.



        :param right: Another frame to join with
        :type right: Frame
        :param left_on: Name of the column in the left frame used to match up the two frames.
        :type left_on: str
        :param right_on: (default=None)  Name of the column in the right frame used to match up the two frames. Default is the same as the left frame.
        :type right_on: str
        :param how: (default=inner)  How to qualify the data to be joined together.  Must be one of the following:  'left', 'right', 'inner', 'outer'.  Default is 'inner'
        :type how: str
        :param name: (default=None)  Name of the result grouped frame
        :type name: str

        :returns: A new frame with the results of the join
        :rtype: Frame
        """
        return None


    @property
    @doc_stub
    def last_read_date(self):
        """
        Last time this frame's data was accessed.



        :returns: Date string of the last time this frame's data was accessed
        :rtype: str
        """
        return None


    @doc_stub
    def loadhbase(self, table_name, schema, start_tag=None, end_tag=None):
        """
        Append data from an HBase table into an existing (possibly empty) FrameRDD

        Append data from an HBase table into an existing (possibly empty) FrameRDD

        :param table_name: hbase table name
        :type table_name: unicode
        :param schema: hbase schema as a list of tuples (columnFamily, columnName, dataType for cell value)
        :type schema: list
        :param start_tag: (default=None)  optional start tag for filtering
        :type start_tag: unicode
        :param end_tag: (default=None)  optional end tag for filtering
        :type end_tag: unicode

        :returns: the initial FrameRDD with the HBase data appended
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def loadhive(self, query):
        """
        Append data from a hive table into an existing (possibly empty) frame

        Append data from a hive table into an existing (possibly empty) frame

        :param query: Initial query to run at load time
        :type query: unicode

        :returns: the initial frame with the hive data appended
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def loadjdbc(self, table_name, connector_type=None, url=None, driver_name=None, query=None):
        """
        Append data from a JDBC table into an existing (possibly empty) frame

        Append data from a JDBC table into an existing (possibly empty) frame

        :param table_name: table name
        :type table_name: unicode
        :param connector_type: (default=None)  (optional) connector type
        :type connector_type: unicode
        :param url: (default=None)  (optional) connection url (includes server name, database name, user acct and password
        :type url: unicode
        :param driver_name: (default=None)  (optional) driver name
        :type driver_name: unicode
        :param query: (default=None)  (optional) query for filtering. Not supported yet.
        :type query: unicode

        :returns: the initial frame with the JDBC data appended
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the frame object.

        Change or retrieve frame object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_frame.name

            "csv_data"

            >>> my_frame.name = "cleaned_data"
            >>> my_frame.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def quantiles(self, column_name, quantiles):
        """
        New frame with Quantiles and their values.

        Calculate quantiles on the given column.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column *final_sale_price*:

        .. code::

            >>> my_frame.inspect()

              final_sale_price:int32
            /------------------------/
                        100
                        250
                         95
                        179
                        315
                        660
                        540
                        420
                        250
                        335

        To calculate 10th, 50th, and 100th quantile:

        .. code::

            >>> quantiles_frame = my_frame.quantiles('final_sale_price', [10, 50, 100])

        A new Frame containing the requested Quantiles and their respective values
        will be returned :

        .. code::

           >>> quantiles_frame.inspect()

             Quantiles:float64   final_sale_price_QuantileValue:float64
           /------------------------------------------------------------/
                    10.0                                     95.0
                    50.0                                    250.0
                   100.0                                    660.0




        :param column_name: The column to calculate quantiles.
        :type column_name: unicode
        :param quantiles: What is being requested.
        :type quantiles: list

        :returns: A new frame with two columns (float64): requested Quantiles and their respective values.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def rename_columns(self, names):
        """
        Rename columns for edge frame.

        :param names: 
        :type names: None

        :returns: 
        :rtype: _Unit
        """
        return None


    @property
    @doc_stub
    def row_count(self):
        """
        Number of rows in the current frame.

        Counts all of the rows in the frame.

        Examples
        --------
        Get the number of rows:

        .. code::

            >>> my_frame.row_count

        The result given is:

        .. code::

            81734





        :returns: The number of rows in the frame
        :rtype: int
        """
        return None


    @property
    @doc_stub
    def schema(self):
        """
        Current frame column names and types.

        The schema of the current frame is a list of column names and
        associated data types.
        It is retrieved as a list of tuples.
        Each tuple has the name and data type of one of the frame's columns.

        Examples
        --------
        Given that we have an existing data frame *my_data*, create a Frame,
        then show the frame schema:

        .. code::

            >>> BF = ta.get_frame('my_data')
            >>> print BF.schema

        The result is:

        .. code::

            [("col1", str), ("col2", numpy.int32)]





        :returns: list of tuples of the form (<column name>, <data type>)
        :rtype: list
        """
        return None


    @doc_stub
    def sort(self, columns, ascending=True):
        """
        Sort the data in a frame.

        Sort a frame by column values either ascending or descending.

        Examples
        --------
        Sort a single column:

        .. code::

            >>> frame.sort('column_name')

        Sort a single column ascending:

        .. code::

            >>> frame.sort('column_name', True)

        Sort a single column descending:

        .. code::

            >>> frame.sort('column_name', False)

        Sort multiple columns:

        .. code::

            >>> frame.sort(['col1', 'col2'])

        Sort multiple columns ascending:

        .. code::

            >>> frame.sort(['col1', 'col2'], True)

        Sort multiple columns descending:

        .. code::

            >>> frame.sort(['col1', 'col2'], False)

        Sort multiple columns: 'col1' ascending and 'col2' descending:

        .. code::

            >>> frame.sort([ ('col1', True), ('col2', False) ])



        :param columns: Either a column name, a list of column names, or a list of tuples where each tuple is a name and an ascending bool value.
        :type columns: str | list of str | list of tuples
        :param ascending: (default=True)  True for ascending, False for descending.
        :type ascending: bool
        """
        return None


    @doc_stub
    def sorted_k(self, k, column_names_and_ascending, reduce_tree_depth=None):
        """
        Get a sorted subset of the data.

        Take a number of rows and return them
        sorted in either ascending or descending order.

        Sorting a subset of rows is more efficient than sorting the entire frame when
        the number of sorted rows is much less than the total number of rows in the frame.

        Notes
        -----
        The number of sorted rows should be much smaller than the number of rows
        in the original frame.

        In particular:

        #)  The number of sorted rows returned should fit in Spark driver memory.
            The maximum size of serialized results that can fit in the Spark driver is
            set by the Spark configuration parameter *spark.driver.maxResultSize*.
        #)  If you encounter a Kryo buffer overflow exception, increase the Spark
            configuration parameter *spark.kryoserializer.buffer.max.mb*.
        #)  Use Frame.sort() instead if the number of sorted rows is very large (in
            other words, it cannot fit in Spark driver memory).

        Examples
        --------
        These examples deal with the most recently-released movies in a private collection.
        Consider the movie collection already stored in the frame below:

        .. code::

            >>> big_frame.inspect(10)

              genre:str  year:int32   title:str
            /-----------------------------------/
              Drama        1957       12 Angry Men
              Crime        1946       The Big Sleep
              Western      1969       Butch Cassidy and the Sundance Kid
              Drama        1971       A Clockwork Orange
              Drama        2008       The Dark Knight
              Animation    2013       Frozen
              Drama        1972       The Godfather
              Animation    1994       The Lion King
              Animation    2010       Tangled
              Fantasy      1939       The Wonderful Wizard of Oz


        This example returns the top 3 rows sorted by a single column: 'year' descending:

        .. code::

            >>> topk_frame = big_frame.sorted_k(3, [ ('year', False) ])
            >>> topk_frame.inspect()

              genre:str  year:int32   title:str
            /-----------------------------------/
              Animation    2013       Frozen
              Animation    2010       Tangled
              Drama        2008       The Dark Knight


        This example returns the top 5 rows sorted by multiple columns: 'genre' ascending, then 'year' descending:

        .. code::

            >>> topk_frame = big_frame.sorted_k(5, [ ('genre', True), ('year', False) ])
            >>> topk_frame.inspect()

              genre:str  year:int32   title:str
            /-----------------------------------/
              Animation    2013       Frozen
              Animation    2010       Tangled
              Animation    1994       The Lion King
              Crime        1946       The Big Sleep
              Drama        2008       The Dark Knight

        This example returns the top 5 rows sorted by multiple columns: 'genre'
        ascending, then 'year' ascending.
        It also illustrates the optional tuning parameter for reduce-tree depth
        (which does not affect the final result).

        .. code::

            >>> topk_frame = big_frame.sorted_k(5, [ ('genre', True), ('year', True) ], reduce_tree_depth=1)
            >>> topk_frame.inspect()

              genre:str  year:int32   title:str
            /-----------------------------------/
              Animation    1994       The Lion King
              Animation    2010       Tangled
              Animation    2013       Frozen
              Crime        1946       The Big Sleep
              Drama        1972       The Godfather



        :param k: Number of sorted records to return.
        :type k: int32
        :param column_names_and_ascending: Column names to sort by, and true to sort column by ascending order,
            or false for descending order.
        :type column_names_and_ascending: list
        :param reduce_tree_depth: (default=None)  Advanced tuning parameter which determines the depth of the
            reduce-tree (uses Spark's treeReduce() for scalability.)
            Default is 2.
        :type reduce_tree_depth: int32

        :returns: A new frame with a subset of sorted rows from the original frame.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @property
    @doc_stub
    def status(self):
        """
        Current frame life cycle status.

        One of three statuses: Active, Dropped, Finalized
           Active:    Entity is available for use
           Dropped:   Entity has been dropped by user or by garbage collection which found it stale
           Finalized: Entity's data has been deleted

        Examples
        --------
        Given that we have an existing data frame *my_data*, create a Frame,
        then show the frame schema:

        .. code::

            >>> BF = ta.get_frame('my_data')
            >>> print BF.status

        The result is:

        .. code::

            u'Active'




        :returns: Status of the frame
        :rtype: str
        """
        return None


    @doc_stub
    def take(self, n, offset=0, columns=None):
        """
        Get data subset.

        Take a subset of the currently active Frame.

        Notes
        -----
        The data is considered 'unstructured', therefore taking a certain
        number of rows, the rows obtained may be different every time the
        command is executed, even if the parameters do not change.

        Examples
        --------
        Frame *my_frame* accesses a frame with millions of rows of data.
        Get a sample of 5000 rows:

        .. code::

            >>> my_data_list = my_frame.take( 5000 )

        We now have a list of data from the original frame.

        .. code::

            >>> print my_data_list

            [[ 1, "text", 3.1415962 ]
             [ 2, "bob", 25.0 ]
             [ 3, "weave", .001 ]
             ...]

        If we use the method with an offset like:

        .. code::

            >>> my_data_list = my_frame.take( 5000, 1000 )

        We end up with a new list, but this time it has a copy of the data from
        rows 1001 to 5000 of the original frame.



        :param n: The number of rows to copy to the client from the frame.
        :type n: int
        :param offset: (default=0)  The number of rows to skip before starting to copy
        :type offset: int
        :param columns: (default=None)  If not None, only the given columns' data will be provided.  By default, all columns are included
        :type columns: str | iterable of str

        :returns: A list of lists, where each contained list is the data for one row.
        :rtype: list
        """
        return None


    @doc_stub
    def tally(self, sample_col, count_val):
        """
        Count number of times a value is seen.

        A cumulative count is computed by sequentially stepping through the rows,
        observing the column values and keeping track of the number of times the specified
        *count_value* has been seen.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column *obs*:

        .. code::

            >>> my_frame.inspect()

              obs:int32
            /-----------/
                0
                1
                2
                0
                1
                2

        The cumulative count for column *obs* using *count_value = 1* is obtained by:

        .. code::

            >>> my_frame.tally('obs', '1')

        The Frame *my_frame* accesses a frame which now contains two columns *obs*
        and *obsCumulativeCount*.
        Column *obs* still has the same data and *obsCumulativeCount* contains the
        cumulative counts:

        .. code::

            >>> my_frame.inspect()

              obs:int32        obs_tally:int32
            /----------------------------------/
                 0                      0
                 1                      1
                 2                      1
                 0                      1
                 1                      2
                 2                      2



        :param sample_col: The name of the column from which to compute the cumulative count.
        :type sample_col: unicode
        :param count_val: The column value to be used for the counts.
        :type count_val: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def tally_percent(self, sample_col, count_val):
        """
        Compute a cumulative percent count.

        A cumulative percent count is computed by sequentially stepping through
        the rows, observing the column values and keeping track of the percentage of the
        total number of times the specified *count_value* has been seen up to
        the current value.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column named *obs*:

        .. code::

            >>> my_frame.inspect()

              obs:int32
            /-----------/
                 0
                 1
                 2
                 0
                 1
                 2

        The cumulative percent count for column *obs* is obtained by:

        .. code::

            >>> my_frame.tally_percent('obs', 1)

        The Frame *my_frame* accesses the original frame that now contains two
        columns, *obs* that contains the original column values, and
        *obsCumulativePercentCount* that contains the cumulative percent count:

        .. code::

            >>> my_frame.inspect()

              obs:int32    obs_tally_percent:float64
            /----------------------------------------/
                 0                         0.0
                 1                         0.5
                 2                         0.5
                 0                         0.5
                 1                         1.0
                 2                         1.0



        :param sample_col: The name of the column from which to compute
            the cumulative sum.
        :type sample_col: unicode
        :param count_val: The column value to be used for the counts.
        :type count_val: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def top_k(self, column_name, k, weights_column=None):
        """
        Most or least frequent column values.

        Calculate the top (or bottom) K distinct values by count of a column.
        The column can be weighted.
        All data elements of weight <= 0 are excluded from the calculation, as are
        all data elements whose weight is NaN or infinite.
        If there are no data elements of finite weight > 0, then topK is empty.

        Examples
        --------
        For this example, we calculate the top 5 movie genres in a data frame:

        .. code::

            >>> top5 = frame.top_k('genre', 5)
            >>> top5.inspect()

              genre:str   count:float64
            /---------------------------/
              Drama        738278
              Comedy       671398
              Short        455728
              Documentary  323150
              Talk-Show    265180

        This example calculates the top 3 movies weighted by rating:

        .. code::

            >>> top3 = frame.top_k('genre', 3, weights_column='rating')
            >>> top3.inspect()

              movie:str      count:float64
            /------------------------------/
              The Godfather         7689.0
              Shawshank Redemption  6358.0
              The Dark Knight       5426.0

        This example calculates the bottom 3 movie genres in a data frame:

        .. code::

            >>> bottom3 = frame.top_k('genre', -3)
            >>> bottom3.inspect()

              genre:str   count:float64
            /---------------------------/
              Musical       26
              War           47
              Film-Noir    595




        :param column_name: The column whose top (or bottom) K distinct values are
            to be calculated.
        :type column_name: unicode
        :param k: Number of entries to return (If k is negative, return bottom k).
        :type k: int32
        :param weights_column: (default=None)  The column that provides weights (frequencies) for the topK calculation.
            Must contain numerical data.
            Default is 1 for all items.
        :type weights_column: unicode

        :returns: An object with access to the frame of data.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def unflatten_column(self, composite_key_column_names, delimiter=None):
        """
        Compacts data from multiple rows based on cell data.

        Groups together cells in all columns (less the composite key) using "," as string delimiter.
        The original rows are deleted.
        The grouping takes place based on a composite key created from cell values.
        The column datatypes are changed to string.

        Examples
        --------
        Given a data file::

            user1 1/1/2015 1 70
            user1 1/1/2015 2 60
            user2 1/1/2015 1 65

        The commands to bring the data into a frame, where it can be worked on:

        .. only:: html

            .. code::

                >>> my_csv = ta.CsvFile("original_data.csv", schema=[('a', str), ('b', str),('c', int32) ,('d', int32]))
                >>> my_frame = ta.Frame(source=my_csv)

        .. only:: latex

            .. code::

                >>> my_csv = ta.CsvFile("unflatten_column.csv", schema=[('a', str), ('b', str),('c', int32) ,('d', int32)])
                >>> my_frame = ta.Frame(source=my_csv)

        Looking at it:

        .. code::

            >>> my_frame.inspect()

              a:str        b:str       c:int32       d:int32
            /------------------------------------------------/
               user1       1/1/12015   1             70
               user1       1/1/12015   2             60
               user2       1/1/2015    1             65

        Unflatten the data using columns a & b:

        .. code::

            >>> my_frame.unflatten_column({'a','b'})

        Check again:

        .. code::

            >>> my_frame.inspect()

              a:str        b:str       c:str     d:str
            /-------------------------------------------/
               user1       1/1/12015   1,2       70,60
               user2       1/1/2015    1         65



        :param composite_key_column_names: Name of the column(s) to be used as keys
            for unflattening.
        :type composite_key_column_names: list
        :param delimiter: (default=None)  Separator for the data in the result columns.
            Default is comma (,).
        :type delimiter: unicode

        :returns: 
        :rtype: _Unit
        """
        return None



@doc_stub
class _DocStubsFrame(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, source=None, name=None):
        """
            Create a Frame/frame.

        Notes
        -----
        A frame with no name is subject to garbage collection.

        If a string in the CSV file starts and ends with a double-quote (")
        character, the character is stripped off of the data before it is put into
        the field.
        Anything, including delimiters, between the double-quote characters is
        considered part of the str.
        If the first character after the delimiter is anything other than a
        double-quote character, the string will be composed of all the characters
        between the delimiters, including double-quotes.
        If the first field type is str, leading spaces on each row are
        considered part of the str.
        If the last field type is str, trailing spaces on each row are
        considered part of the str.

        Examples
        --------
        Create a new frame based upon the data described in the CsvFile object
        *my_csv_schema*.
        Name the frame "myframe".
        Create a Frame *my_frame* to access the data:

        .. code::

            >>> my_frame = ta.Frame(my_csv_schema, "myframe")

        A Frame object has been created and *my_frame* is its proxy.
        It brought in the data described by *my_csv_schema*.
        It is named *myframe*.

        Create an empty frame; name it "yourframe":

        .. code::

            >>> your_frame = ta.Frame(name='yourframe')

        A frame has been created and Frame *your_frame* is its proxy.
        It has no data yet, but it does have the name *yourframe*.
            

        :param source: (default=None)  A source of initial data.
        :type source: CsvFile | Frame
        :param name: (default=None)  The name of the newly created frame.
            Default is None.
        :type name: str
        """
        raise DocStubCalledError("frame:/__init__")


    @doc_stub
    def add_columns(self, func, schema, columns_accessed=None):
        """
        Add columns to current frame.

        Assigns data to column based on evaluating a function for each row.

        Notes
        -----
        1)  The row |UDF| ('func') must return a value in the same format as
            specified by the schema.
            See :doc:`/ds_apir`.
        2)  Unicode in column names is not supported and will likely cause the
            drop_frames() method (and others) to fail!

        Examples
        --------
        Given a Frame *my_frame* identifying a data frame with two int32
        columns *column1* and *column2*.
        Add a third column *column3* as an int32 and fill it with the
        contents of *column1* and *column2* multiplied together:

        .. code::

            >>> my_frame.add_columns(lambda row: row.column1*row.column2,
            ... ('column3', int32))

        The frame now has three columns, *column1*, *column2* and *column3*.
        The type of *column3* is an int32, and the value is the product of
        *column1* and *column2*.

        Add a string column *column4* that is empty:

        .. code::

            >>> my_frame.add_columns(lambda row: '', ('column4', str))

        The Frame object *my_frame* now has four columns *column1*, *column2*,
        *column3*, and *column4*.
        The first three columns are int32 and the fourth column is str.
        Column *column4* has an empty string ('') in every row.

        Multiple columns can be added at the same time.
        Add a column *a_times_b* and fill it with the contents of column *a*
        multiplied by the contents of column *b*.
        At the same time, add a column *a_plus_b* and fill it with the contents
        of column *a* plus the contents of column *b*:

        .. only:: html

            .. code::

                >>> my_frame.add_columns(lambda row: [row.a * row.b, row.a + row.b], [("a_times_b", float32), ("a_plus_b", float32))

        .. only:: latex

            .. code::

                >>> my_frame.add_columns(lambda row: [row.a * row.b, row.a +
                ... row.b], [("a_times_b", float32), ("a_plus_b", float32))

        Two new columns are created, "a_times_b" and "a_plus_b", with the
        appropriate contents.

        Given a frame of data and Frame *my_frame* points to it.
        In addition we have defined a |UDF| *func*.
        Run *func* on each row of the frame and put the result in a new int
        column *calculated_a*:

        .. code::

            >>> my_frame.add_columns( func, ("calculated_a", int))

        Now the frame has a column *calculated_a* which has been filled with
        the results of the |UDF| *func*.

        A |UDF| must return a value in the same format as the column is
        defined.
        In most cases this is automatically the case, but sometimes it is less
        obvious.
        Given a |UDF| *function_b* which returns a value in a list, store
        the result in a new column *calculated_b*:

        .. code::

            >>> my_frame.add_columns(function_b, ("calculated_b", float32))

        This would result in an error because function_b is returning a value
        as a single element list like [2.4], but our column is defined as a
        tuple.
        The column must be defined as a list:

        .. code::

            >>> my_frame.add_columns(function_b, [("calculated_b", float32)])

        To run an optimized version of add_columns, columns_accessed parameter can
        be populated with the column names which are being accessed in |UDF|. This
        speeds up the execution by working on only the limited feature set than the
        entire row.

        Let's say a frame has 4 columns named *a*,*b*,*c* and *d* and we want to add a new column
        with value from column *a* multiplied by value in column *b* and call it *a_times_b*.
        In the example below, columns_accessed is a list with column names *a* and *b*.

        .. code::

            >>> my_frame.add_columns(lambda row: row.a * row.b, ("a_times_b", float32), columns_accessed=["a", "b"])

        add_columns would fail if columns_accessed parameter is not populated with the correct list of accessed
        columns. If not specified, columns_accessed defaults to None which implies that all columns might be accessed
        by the |UDF|.

        More information on a row |UDF| can be found at :doc:`/ds_apir`



        :param func: User-Defined Function (|UDF|) which takes the values in the row and produces a value, or collection of values, for the new cell(s).
        :type func: UDF
        :param schema: The schema for the results of the |UDF|, indicating the new column(s) to add.  Each tuple provides the column name and data type, and is of the form (str, type).
        :type schema: tuple | list of tuples
        :param columns_accessed: (default=None)  List of columns which the |UDF| will access.  This adds significant performance benefit if we know which column(s) will be needed to execute the |UDF|, especially when the frame has significantly more columns than those being used to evaluate the |UDF|.
        :type columns_accessed: list
        """
        return None


    @doc_stub
    def append(self, data):
        """
        Adds more data to the current frame.

        Examples
        --------
        Given a frame with a single column, *col_1*:

        .. code::

                >>> my_frame.inspect(4)
                  col_1:str
                /-----------/
                  dog
                  cat
                  bear
                  donkey

          and a frame with two columns, *col_1* and *col_2*:

          ..code::

                >>> your_frame.inspect(4)
                  col_1:str  col_qty:int32
                /--------------------------/
                  bear          15
                  cat            2
                  snake          8
                  horse          5

        Column *col_1* means the same thing in both frames.
        The Frame *my_frame* points to the first frame and *your_frame* points
        to the second.
        To add the contents of *your_frame* to *my_frame*:

        .. code::

            >>> my_frame.append(your_frame)
            >>> my_frame.inspect(8)
              col_1:str  col_2:int32
            /------------------------/
              dog           None
              bear            15
              bear          None
              horse            5
              cat           None
              cat              2
              donkey        None
              snake            5

        Now the first frame has two columns, *col_1* and *col_2*.
        Column *col_1* has the data from *col_1* in both original frames.
        Column *col_2* has None (undefined) in all of the rows in the original
        first frame, and has the value of the second frame column, *col_2*, in
        the rows matching the new data in *col_1*.

        Breaking it down differently, the original rows referred to by
        *my_frame* have a new column, *col_2*, and this new column is filled
        with non-defined data.
        The frame referred to by *your_frame*, is then added to the bottom.



        :param data: Data source, see :doc:`Data Sources </python_api/datasources/index>`
        :type data: Data source
        """
        return None


    @doc_stub
    def assign_sample(self, sample_percentages, sample_labels=None, output_column=None, random_seed=None):
        """
        Randomly group rows into user-defined classes.

        Randomly assign classes to rows given a vector of percentages.
        The table receives an additional column that contains a random label.
        The random label is generated by a probability distribution function.
        The distribution function is specified by the sample_percentages, a list of
        floating point values, which add up to 1.
        The labels are non-negative integers drawn from the range
        :math:`[ 0, len(S) - 1]` where :math:`S` is the sample_percentages.

        **Notes**

        The sample percentages provided by the user are preserved to at least eight
        decimal places, but beyond this there may be small changes due to floating
        point imprecision.

        In particular:

        #)  The engine validates that the sum of probabilities sums to 1.0 within
            eight decimal places and returns an error if the sum falls outside of this
            range.
        #)  The probability of the final class is clamped so that each row receives a
            valid label with probability one.

        Examples
        --------
        Given a frame accessed via Frame *my_frame*:

        .. code::

            >>> my_frame.inspect()
              col_nc:str  col_wk:str
            /------------------------/
              abc         zzz
              def         yyy
              ghi         xxx
              jkl         www
              mno         vvv
              pqr         uuu
              stu         ttt
              vwx         sss
              yza         rrr
              bcd         qqq

        To append a new column *sample_bin* to the frame and assign the value in the
        new column to "train", "test", or "validate":

        .. code::

            >>> my_frame.assign_sample([0.3, 0.3, 0.4], ["train", "test", "validate"])
            >>> my_frame.inspect()
              col_nc:str  col_wk:str  sample_bin:str
            /----------------------------------------/
              abc         zzz         validate
              def         yyy         test
              ghi         xxx         test
              jkl         www         test
              mno         vvv         train
              pqr         uuu         validate
              stu         ttt         validate
              vwx         sss         train
              yza         rrr         validate
              bcd         qqq         train

        Now, the frame accessed by the Frame, *my_frame*, has a new column named
        "sample_bin" and each row contains one of the values "train", "test", or
        "validate".
        Values in the other columns are unaffected.



        :param sample_percentages: Entries are non-negative and sum to 1. (See the note below.)
            If the *i*'th entry of the  list is *p*,
            then then each row receives label *i* with independent probability *p*.
        :type sample_percentages: list
        :param sample_labels: (default=None)  Names to be used for the split classes.
            Defaults to "TR", "TE", "VA" when the length of *sample_percentages* is 3,
            and defaults to Sample_0, Sample_1, ... otherwise.
        :type sample_labels: list
        :param output_column: (default=None)  Name of the new column which holds the labels generated by the
            function.
        :type output_column: unicode
        :param random_seed: (default=None)  Random seed used to generate the labels.
            Defaults to 0.
        :type random_seed: int32

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def bin_column(self, column_name, cutoffs, include_lowest=None, strict_binning=None, bin_column_name=None):
        """
        Classify data into user-defined groups.

        Summarize rows of data based on the value in a single column by sorting them
        into bins, or groups, based on a list of bin cutoff points.

        **Notes**

        #)  Unicode in column names is not supported and will likely cause the
            drop_frames() method (and others) to fail!
        #)  Bins IDs are 0-index, in other words, the lowest bin number is 0.
        #)  The first and last cutoffs are always included in the bins.
            When *include_lowest* is ``True``, the last bin includes both cutoffs.
            When *include_lowest* is ``False``, the first bin (bin 0) includes both
            cutoffs.

        Examples
        --------
        For this example, we will use a frame with column *a* accessed by a Frame
        object *my_frame*:

        .. code::

            >>> my_frame.inspect( n=11 )

              a:int32
            /---------/
                1
                1
                2
                3
                5
                8
               13
               21
               34
               55
               89

        Modify the frame with a column showing what bin the data is in.
        The data values should use strict_binning:

        .. code::

            >>> my_frame.bin_column('a', [5,12,25,60], include_lowest=True,
            ... strict_binning=True, bin_column_name='binned')
            >>> my_frame.inspect( n=11 )

              a:int32     binned:int32
            /---------------------------/
                  1               -1
                  1               -1
                  2               -1
                  3               -1
                  5                0
                  8                0
                 13                1
                 21                1
                 34                2
                 55                2
                 89               -1

        Modify the frame with a column showing what bin the data is in.
        The data value should not use strict_binning:

        .. code::

            >>> my_frame.bin_column('a', [5,12,25,60], include_lowest=True,
            ... strict_binning=False, bin_column_name='binned')
            >>> my_frame.inspect( n=11 )

              a:int32     binned:int32
            /---------------------------/
                  1                0
                  1                0
                  2                0
                  3                0
                  5                0
                  8                0
                 13                1
                 21                1
                 34                2
                 55                2
                 89                2


        Modify the frame with a column showing what bin the data is in.
        The bins should be lower inclusive:

        .. code::

            >>> my_frame.bin_column('a', [1,5,34,55,89], include_lowest=True,
            ... strict_binning=False, bin_column_name='binned')
            >>> my_frame.inspect( n=11 )

              a:int32     binned:int32
            /---------------------------/
                  1                0
                  1                0
                  2                0
                  3                0
                  5                1
                  8                1
                 13                1
                 21                1
                 34                2
                 55                3
                 89                3

        Modify the frame with a column showing what bin the data is in.
        The bins should be upper inclusive:

        .. code::

            >>> my_frame.bin_column('a', [1,5,34,55,89], include_lowest=False,
            ... strict_binning=True, bin_column_name='binned')
            >>> my_frame.inspect( n=11 )

              a:int32     binned:int32
            /---------------------------/
               1                   0
               1                   0
               2                   0
               3                   0
               5                   0
               8                   1
              13                   1
              21                   1
              34                   1
              55                   2
              89                   3


        :param column_name: Name of the column to bin.
        :type column_name: unicode
        :param cutoffs: Array of values containing bin cutoff points.
            Array can be list or tuple.
            Array values must be progressively increasing.
            All bin boundaries must be included, so, with N bins, you need N+1 values.
        :type cutoffs: list
        :param include_lowest: (default=None)  Specify how the boundary conditions are handled.
            ``True`` indicates that the lower bound of the bin is inclusive.
            ``False`` indicates that the upper bound is inclusive.
            Default is ``True``.
        :type include_lowest: bool
        :param strict_binning: (default=None)  Specify how values outside of the cutoffs array should be binned.
            If set to ``True``, each value less than cutoffs[0] or greater than
            cutoffs[-1] will be assigned a bin value of -1.
            If set to ``False``, values less than cutoffs[0] will be included in the first
            bin while values greater than cutoffs[-1] will be included in the final
            bin.
        :type strict_binning: bool
        :param bin_column_name: (default=None)  The name for the new binned column.
            Default is ``<column_name>_binned``.
        :type bin_column_name: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def bin_column_equal_depth(self, column_name, num_bins=None, bin_column_name=None):
        """
        Classify column into groups with the same frequency.

        Group rows of data based on the value in a single column and add a label
        to identify grouping.

        Equal depth binning attempts to label rows such that each bin contains the
        same number of elements.
        For :math:`n` bins of a column :math:`C` of length :math:`m`, the bin
        number is determined by:

        .. math::

            \lceil n * \frac { f(C) }{ m } \rceil

        where :math:`f` is a tie-adjusted ranking function over values of
        :math:`C`.
        If there are multiples of the same value in :math:`C`, then their
        tie-adjusted rank is the average of their ordered rank values.

        **Notes**

        #)  Unicode in column names is not supported and will likely cause the
            drop_frames() method (and others) to fail!
        #)  The num_bins parameter is considered to be the maximum permissible number
            of bins because the data may dictate fewer bins.
            For example, if the column to be binned has a quantity of :math"`X`
            elements with only 2 distinct values and the *num_bins* parameter is
            greater than 2, then the actual number of bins will only be 2.
            This is due to a restriction that elements with an identical value must
            belong to the same bin.

        Examples
        --------
        Given a frame with column *a* accessed by a Frame object *my_frame*:

        .. code::

            >>> my_frame.inspect( n=11 )

              a:int32
            /---------/
                1
                1
                2
                3
                5
                8
               13
               21
               34
               55
               89

        Modify the frame, adding a column showing what bin the data is in.
        The data should be grouped into a maximum of five bins.
        Note that each bin will have the same quantity of members (as much as
        possible):

        .. code::

            >>> cutoffs = my_frame.bin_column_equal_depth('a', 5, 'aEDBinned')
            >>> my_frame.inspect( n=11 )

              a:int32     aEDBinned:int32
            /-----------------------------/
                  1                   0
                  1                   0
                  2                   1
                  3                   1
                  5                   2
                  8                   2
                 13                   3
                 21                   3
                 34                   4
                 55                   4
                 89                   4

            >>> print cutoffs
            [1.0, 2.0, 5.0, 13.0, 34.0, 89.0]


        :param column_name: The column whose values are to be binned.
        :type column_name: unicode
        :param num_bins: (default=None)  The maximum number of bins.
            Default is the Square-root choice
            :math:`\lfloor \sqrt{m} \rfloor`, where :math:`m` is the number of rows.
        :type num_bins: int32
        :param bin_column_name: (default=None)  The name for the new column holding the grouping labels.
            Default is ``<column_name>_binned``.
        :type bin_column_name: unicode

        :returns: A list containing the edges of each bin.
        :rtype: dict
        """
        return None


    @doc_stub
    def bin_column_equal_width(self, column_name, num_bins=None, bin_column_name=None):
        """
        Classify column into same-width groups.

        Group rows of data based on the value in a single column and add a label
        to identify grouping.

        Equal width binning places column values into groups such that the values
        in each group fall within the same interval and the interval width for each
        group is equal.

        **Notes**

        #)  Unicode in column names is not supported and will likely cause the
            drop_frames() method (and others) to fail!
        #)  The num_bins parameter is considered to be the maximum permissible number
            of bins because the data may dictate fewer bins.
            For example, if the column to be binned has 10
            elements with only 2 distinct values and the *num_bins* parameter is
            greater than 2, then the number of actual number of bins will only be 2.
            This is due to a restriction that elements with an identical value must
            belong to the same bin.

        Examples
        --------
        Given a frame with column *a* accessed by a Frame object *my_frame*:

        .. code::

            >>> my_frame.inspect( n=11 )

              a:int32
            /---------/
                1
                1
                2
                3
                5
                8
               13
               21
               34
               55
               89

        Modify the frame, adding a column showing what bin the data is in.
        The data should be separated into a maximum of five bins and the bin cutoffs
        should be evenly spaced.
        Note that there may be bins with no members:

        .. code::

            >>> cutoffs = my_frame.bin_column_equal_width('a', 5, 'aEWBinned')
            >>> my_frame.inspect( n=11 )

              a:int32     aEWBinned:int32
            /-----------------------------/
                1                 0
                1                 0
                2                 0
                3                 0
                5                 0
                8                 0
               13                 0
               21                 1
               34                 1
               55                 3
               89                 4

        The method returns a list of 6 cutoff values that define the edges of each bin.
        Note that difference between the cutoff values is constant:

        .. code::

            >>> print cutoffs
            [1.0, 18.6, 36.2, 53.8, 71.4, 89.0]


        :param column_name: The column whose values are to be binned.
        :type column_name: unicode
        :param num_bins: (default=None)  The maximum number of bins.
            Default is the Square-root choice
            :math:`\lfloor \sqrt{m} \rfloor`, where :math:`m` is the number of rows.
        :type num_bins: int32
        :param bin_column_name: (default=None)  The name for the new column holding the grouping labels.
            Default is ``<column_name>_binned``.
        :type bin_column_name: unicode

        :returns: A list of the edges of each bin.
        :rtype: dict
        """
        return None


    @doc_stub
    def categorical_summary(self, column_inputs=None):
        """
        Compute a summary of the data in a column(s) for categorical or numerical data types.

        The returned value is a Map containing categorical summary for each specified column.

        For each column, levels which satisfy the top k and/or threshold cutoffs are displayed along
        with their frequency and percentage occurrence with respect to the total rows in the dataset.

        Missing data is reported when a column value is empty ("") or null.

        All remaining data is grouped together in the Other category and its frequency and percentage are reported as well.

        User must specify the column name and can optionally specify top_k and/or threshold.

        Optional parameters:

            top_k
                Displays levels which are in the top k most frequently occurring values for that column.

            threshold
                Displays levels which are above the threshold percentage with respect to the total row count.

            top_k and threshold
                Performs level pruning first based on top k and then filters out levels which satisfy the threshold criterion.

            defaults
                Displays all levels which are in Top 10.


        Examples
        --------

        .. code::

            >>> frame.categorical_summary('source','target')
            >>> frame.categorical_summary(('source', {'top_k' : 2}))
            >>> frame.categorical_summary(('source', {'threshold' : 0.5}))
            >>> frame.categorical_summary(('source', {'top_k' : 2}), ('target',
            ... {'threshold' : 0.5}))

        Sample output (for last example above):

            >>> {u'categorical_summary': [{u'column': u'source', u'levels': [
            ... {u'percentage': 0.32142857142857145, u'frequency': 9, u'level': u'thing'},
            ... {u'percentage': 0.32142857142857145, u'frequency': 9, u'level': u'abstraction'},
            ... {u'percentage': 0.25, u'frequency': 7, u'level': u'physical_entity'},
            ... {u'percentage': 0.10714285714285714, u'frequency': 3, u'level': u'entity'},
            ... {u'percentage': 0.0, u'frequency': 0, u'level': u'Missing'},
            ... {u'percentage': 0.0, u'frequency': 0, u'level': u'Other'}]},
            ... {u'column': u'target', u'levels': [
            ... {u'percentage': 0.07142857142857142, u'frequency': 2, u'level': u'thing'},
            ... {u'percentage': 0.07142857142857142, u'frequency': 2,
            ...  u'level': u'physical_entity'},
            ... {u'percentage': 0.07142857142857142, u'frequency': 2, u'level': u'entity'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'variable'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'unit'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'substance'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'subject'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'set'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'reservoir'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'relation'},
            ... {u'percentage': 0.0, u'frequency': 0, u'level': u'Missing'},
            ... {u'percentage': 0.5357142857142857, u'frequency': 15, u'level': u'Other'}]}]}



        :param column_inputs: (default=None)  Comma-separated column names to summarize or tuple containing column name and dictionary of optional parameters. Optional parameters (see below for details): top_k (default = 10), threshold (default = 0.0)
        :type column_inputs: str | tuple(str, dict)

        :returns: Summary for specified column(s) consisting of levels with their frequency and percentage
        :rtype: dict
        """
        return None


    @doc_stub
    def classification_metrics(self, label_column, pred_column, pos_label=None, beta=None, frequency_column=None):
        """
        Model statistics of accuracy, precision, and others.

        Calculate the accuracy, precision, confusion_matrix, recall and
        :math:`F_{ \beta}` measure for a classification model.

        *   The **f_measure** result is the :math:`F_{ \beta}` measure for a
            classification model.
            The :math:`F_{ \beta}` measure of a binary classification model is the
            harmonic mean of precision and recall.
            If we let:

            * beta :math:`\equiv \beta`,
            * :math:`T_{P}` denotes the number of true positives,
            * :math:`F_{P}` denotes the number of false positives, and
            * :math:`F_{N}` denotes the number of false negatives

            then:

            .. math::

                F_{ \beta} = (1 + \beta ^ 2) * \frac{ \frac{T_{P}}{T_{P} + F_{P}} * \
                \frac{T_{P}}{T_{P} + F_{N}}}{ \beta ^ 2 * \frac{T_{P}}{T_{P} + \
                F_{P}}  + \frac{T_{P}}{T_{P} + F_{N}}}

            The :math:`F_{ \beta}` measure for a multi-class classification model is
            computed as the weighted average of the :math:`F_{ \beta}` measure for
            each label, where the weight is the number of instances of each label.
            The determination of binary vs. multi-class is automatically inferred
            from the data.

        *   The **recall** result of a binary classification model is the proportion
            of positive instances that are correctly identified.
            If we let :math:`T_{P}` denote the number of true positives and
            :math:`F_{N}` denote the number of false negatives, then the model
            recall is given by :math:`\frac {T_{P}} {T_{P} + F_{N}}`.

            For multi-class classification models, the recall measure is computed as
            the weighted average of the recall for each label, where the weight is
            the number of instances of each label.
            The determination of binary vs. multi-class is automatically inferred
            from the data.

        *   The **precision** of a binary classification model is the proportion of
            predicted positive instances that are correctly identified.
            If we let :math:`T_{P}` denote the number of true positives and
            :math:`F_{P}` denote the number of false positives, then the model
            precision is given by: :math:`\frac {T_{P}} {T_{P} + F_{P}}`.

            For multi-class classification models, the precision measure is computed
            as the weighted average of the precision for each label, where the
            weight is the number of instances of each label.
            The determination of binary vs. multi-class is automatically inferred
            from the data.

        *   The **accuracy** of a classification model is the proportion of
            predictions that are correctly identified.
            If we let :math:`T_{P}` denote the number of true positives,
            :math:`T_{N}` denote the number of true negatives, and :math:`K` denote
            the total number of classified instances, then the model accuracy is
            given by: :math:`\frac{T_{P} + T_{N}}{K}`.

            This measure applies to binary and multi-class classifiers.

        *   The **confusion_matrix** result is a confusion matrix for a
            binary classifier model, formatted for human readability.

        Notes
        -----
        The **confusion_matrix** is not yet implemented for multi-class classifiers.

        Examples
        --------
        Consider the following sample data set in *frame* with actual data
        labels specified in the *labels* column and the predicted labels in the
        *predictions* column:

        .. code::

            >>> frame.inspect()

              a:unicode   b:int32   labels:int32  predictions:int32
            /-------------------------------------------------------/
                red         1              0                  0
                blue        3              1                  0
                blue        1              0                  0
                green       0              1                  1

            >>> cm = frame.classification_metrics(label_column='labels',
            ... pred_column='predictions', pos_label=1, beta=1)

            >>> cm.f_measure

            0.66666666666666663

            >>> cm.recall

            0.5

            >>> cm.accuracy

            0.75

            >>> cm.precision

            1.0

            >>> cm.confusion_matrix

                          Predicted
                         _pos_ _neg__
            Actual  pos |  1     1
                    neg |  0     2



        :param label_column: The name of the column containing the
            correct label for each instance.
        :type label_column: unicode
        :param pred_column: The name of the column containing the
            predicted label for each instance.
        :type pred_column: unicode
        :param pos_label: (default=None)  
        :type pos_label: None
        :param beta: (default=None)  This is the beta value to use for
            :math:`F_{ \beta}` measure (default F1 measure is computed); must be greater than zero.
            Defaults is 1.
        :type beta: float64
        :param frequency_column: (default=None)  The name of an optional column containing the
            frequency of observations.
        :type frequency_column: unicode

        :returns: The data returned is composed of multiple components\:

            |   <object>.accuracy : double
            |   <object>.confusion_matrix : table
            |   <object>.f_measure : double
            |   <object>.precision : double
            |   <object>.recall : double
        :rtype: dict
        """
        return None


    @doc_stub
    def column_median(self, data_column, weights_column=None):
        """
        Calculate the (weighted) median of a column.

        The median is the least value X in the range of the distribution so that
        the cumulative weight of values strictly below X is strictly less than half
        of the total weight and the cumulative weight of values up to and including X
        is greater than or equal to one-half of the total weight.

        All data elements of weight less than or equal to 0 are excluded from the
        calculation, as are all data elements whose weight is NaN or infinite.
        If a weight column is provided and no weights are finite numbers greater
        than 0, None is returned.

        Examples
        --------
        .. code::

            >>> median = frame.column_median('middling column')


        :param data_column: The column whose median is to be calculated.
        :type data_column: unicode
        :param weights_column: (default=None)  The column that provides weights (frequencies)
            for the median calculation.
            Must contain numerical data.
            Default is all items have a weight of 1.
        :type weights_column: unicode

        :returns: varies
                The median of the values.
                If a weight column is provided and no weights are finite numbers greater
                than 0, None is returned.
                The type of the median returned is the same as the contents of the data
                column, so a column of Longs will result in a Long median and a column of
                Floats will result in a Float median.
        :rtype: dict
        """
        return None


    @doc_stub
    def column_mode(self, data_column, weights_column=None, max_modes_returned=None):
        """
        Evaluate the weights assigned to rows.

        Calculate the modes of a column.
        A mode is a data element of maximum weight.
        All data elements of weight less than or equal to 0 are excluded from the
        calculation, as are all data elements whose weight is NaN or infinite.
        If there are no data elements of finite weight greater than 0,
        no mode is returned.

        Because data distributions often have multiple modes, it is possible for a
        set of modes to be returned.
        By default, only one is returned, but by setting the optional parameter
        max_modes_returned, a larger number of modes can be returned.

        Examples
        --------
        .. code::

            >>> mode = frame.column_mode('modum columpne')


        :param data_column: Name of the column supplying the data.
        :type data_column: unicode
        :param weights_column: (default=None)  Name of the column supplying the weights.
            Default is all items have weight of 1.
        :type weights_column: unicode
        :param max_modes_returned: (default=None)  Maximum number of modes returned.
            Default is 1.
        :type max_modes_returned: int32

        :returns: Dictionary containing summary statistics.
                The data returned is composed of multiple components\:

            mode : A mode is a data element of maximum net weight.
                A set of modes is returned.
                The empty set is returned when the sum of the weights is 0.
                If the number of modes is less than or equal to the parameter
                max_modes_returned, then all modes of the data are
                returned.
                If the number of modes is greater than the max_modes_returned
                parameter, only the first max_modes_returned many modes (per a
                canonical ordering) are returned.
            weight_of_mode : Weight of a mode.
                If there are no data elements of finite weight greater than 0,
                the weight of the mode is 0.
                If no weights column is given, this is the number of appearances
                of each mode.
            total_weight : Sum of all weights in the weight column.
                This is the row count if no weights are given.
                If no weights column is given, this is the number of rows in
                the table with non-zero weight.
            mode_count : The number of distinct modes in the data.
                In the case that the data is very multimodal, this number may
                exceed max_modes_returned.


        :rtype: dict
        """
        return None


    @property
    @doc_stub
    def column_names(self):
        """
        Column identifications in the current frame.

        Returns the names of the columns of the current frame.

        Examples
        --------
        Given a Frame object, *my_frame* accessing a frame.
        To get the column names:

        .. code::

            >>> my_columns = my_frame.column_names
            >>> print my_columns

        Now, given there are three columns *col1*,
        *col2*, and *col3*, the result is:

        .. code::

            ["col1", "col2", "col3"]





        :returns: list of names of all the frame's columns
        :rtype: list
        """
        return None


    @doc_stub
    def column_summary_statistics(self, data_column, weights_column=None, use_population_variance=None):
        """
        Calculate multiple statistics for a column.

        Notes
        -----
        Sample Variance
            Sample Variance is computed by the following formula:

            .. math::

                \left( \frac{1}{W - 1} \right) * sum_{i} \
                \left(x_{i} - M \right) ^{2}

            where :math:`W` is sum of weights over valid elements of positive
            weight, and :math:`M` is the weighted mean.

        Population Variance
            Population Variance is computed by the following formula:

            .. math::

                \left( \frac{1}{W} \right) * sum_{i} \
                \left(x_{i} - M \right) ^{2}

            where :math:`W` is sum of weights over valid elements of positive
            weight, and :math:`M` is the weighted mean.

        Standard Deviation
            The square root of the variance.

        Logging Invalid Data
            A row is bad when it contains a NaN or infinite value in either
            its data or weights column.
            In this case, it contributes to bad_row_count; otherwise it
            contributes to good row count.

            A good row can be skipped because the value in its weight
            column is less than or equal to 0.
            In this case, it contributes to non_positive_weight_count, otherwise
            (when the weight is greater than 0) it contributes to
            valid_data_weight_pair_count.

        **Equations**

            .. code::

                bad_row_count + good_row_count = # rows in the frame
                positive_weight_count + non_positive_weight_count = good_row_count

            In particular, when no weights column is provided and all weights are 1.0:

            .. code::

                non_positive_weight_count = 0 and
                positive_weight_count = good_row_count

        Examples
        --------
        .. code::

            >>> stats = frame.column_summary_statistics('data column', 'weight column')



        :param data_column: The column to be statistically summarized.
            Must contain numerical data; all NaNs and infinite values are excluded
            from the calculation.
        :type data_column: unicode
        :param weights_column: (default=None)  Name of column holding weights of
            column values.
        :type weights_column: unicode
        :param use_population_variance: (default=None)  If true, the variance is calculated
            as the population variance.
            If false, the variance calculated as the sample variance.
            Because this option affects the variance, it affects the standard
            deviation and the confidence intervals as well.
            Default is false.
        :type use_population_variance: bool

        :returns: Dictionary containing summary statistics.
            The data returned is composed of multiple components\:

            |   mean : [ double | None ]
            |       Arithmetic mean of the data.
            |   geometric_mean : [ double | None ]
            |       Geometric mean of the data. None when there is a data element <= 0, 1.0 when there are no data elements.
            |   variance : [ double | None ]
            |       None when there are <= 1 many data elements. Sample variance is the weighted sum of the squared distance of each data element from the weighted mean, divided by the total weight minus 1. None when the sum of the weights is <= 1. Population variance is the weighted sum of the squared distance of each data element from the weighted mean, divided by the total weight.
            |   standard_deviation : [ double | None ]
            |       The square root of the variance. None when  sample variance is being used and the sum of weights is <= 1.
            |   total_weight : long
            |       The count of all data elements that are finite numbers. In other words, after excluding NaNs and infinite values.
            |   minimum : [ double | None ]
            |       Minimum value in the data. None when there are no data elements.
            |   maximum : [ double | None ]
            |       Maximum value in the data. None when there are no data elements.
            |   mean_confidence_lower : [ double | None ]
            |       Lower limit of the 95% confidence interval about the mean. Assumes a Gaussian distribution. None when there are no elements of positive weight.
            |   mean_confidence_upper : [ double | None ]
            |       Upper limit of the 95% confidence interval about the mean. Assumes a Gaussian distribution. None when there are no elements of positive weight.
            |   bad_row_count : [ double | None ]
            |       The number of rows containing a NaN or infinite value in either the data or weights column.
            |   good_row_count : [ double | None ]
            |       The number of rows not containing a NaN or infinite value in either the data or weights column.
            |   positive_weight_count : [ double | None ]
            |       The number of valid data elements with weight > 0. This is the number of entries used in the statistical calculation.
            |   non_positive_weight_count : [ double | None ]
            |       The number valid data elements with finite weight <= 0.
        :rtype: dict
        """
        return None


    @doc_stub
    def compute_misplaced_score(self, gravity):
        """


        :param gravity: Similarity measure for computing tension between 2 connected items
        :type gravity: float64

        :returns: 
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def copy(self, columns=None, where=None, name=None):
        """
        Create new frame from current frame.

        Copy frame or certain frame columns entirely or filtered.
        Useful for frame query.

        Examples
        --------
        Build a Frame from a csv file with 5 million rows of data; call the
        frame "cust":

        .. code::

            >>> my_frame = ta.Frame(source="my_data.csv")
            >>> my_frame.name("cust")

        Given the frame has columns *id*, *name*, *hair*, and *shoe*.
        Copy it to a new frame:

        .. code::

            >>> your_frame = my_frame.copy()

        Now we have two frames of data, each with 5 million rows.
        Checking the names:

        .. code::

            >>> print my_frame.name()
            >>> print your_frame.name()

        Gives the results:

        .. code::

            "cust"
            "frame_75401b7435d7132f5470ba35..."

        Now, let's copy *some* of the columns from the original frame:

        .. code::

            >>> our_frame = my_frame.copy(['id', 'hair'])

        Our new frame now has two columns, *id* and *hair*, and has 5 million
        rows.
        Let's try that again, but this time change the name of the *hair*
        column to *color*:

        .. code::

            >>> last_frame = my_frame.copy(('id': 'id', 'hair': 'color'))



        :param columns: (default=None)  If not None, the copy will only include the columns specified. If dict, the string pairs represent a column renaming, {source_column_name: destination_column_name}
        :type columns: str | list of str | dict
        :param where: (default=None)  If not None, only those rows for which the UDF evaluates to True will be copied.
        :type where: function
        :param name: (default=None)  Name of the copied frame
        :type name: str

        :returns: A new Frame of the copied data.
        :rtype: Frame
        """
        return None


    @doc_stub
    def correlation(self, data_column_names):
        """
        Calculate correlation for two columns of current frame.

        Notes
        -----
        This method applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame*, which contains the data

        .. code::

            >>> my_frame.inspect()

             idnum:int32   x1:float32   x2:float32   x3:float32   x4:float32  
           /-------------------------------------------------------------------/
                       0          1.0          4.0          0.0         -1.0  
                       1          2.0          3.0          0.0         -1.0  
                       2          3.0          2.0          1.0         -1.0  
                       3          4.0          1.0          2.0         -1.0  
                       4          5.0          0.0          2.0         -1.0  

        my_frame.correlation computes the common correlation coefficient (Pearson's) on the pair
        of columns provided.
        In this example, the *idnum* and most of the columns have trivial correlations: -1, 0, or +1.
        Column *x3* provides a contrasting coefficient of 3 / sqrt(3) = 0.948683298051 .

        .. code::

            >>> my_frame.correlation(["x1", "x2"])
               -1.0
            >>> my_frame.correlation(["x1", "x4"])
                0.0
            >>> my_frame.correlation(["x2", "x3"])
                -0.948683298051


        :param data_column_names: The names of 2 columns from which
            to compute the correlation.
        :type data_column_names: list

        :returns: Pearson correlation coefficient of the two columns.
        :rtype: dict
        """
        return None


    @doc_stub
    def correlation_matrix(self, data_column_names, matrix_name=None):
        """
        Calculate correlation matrix for two or more columns.

        Notes
        -----
        This method applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame*, which contains the data

        .. code::

            >>> my_frame.inspect()

             idnum:int32   x1:float32   x2:float32   x3:float32   x4:float32  
           /-------------------------------------------------------------------/
                       0          1.0          4.0          0.0         -1.0  
                       1          2.0          3.0          0.0         -1.0  
                       2          3.0          2.0          1.0         -1.0  
                       3          4.0          1.0          2.0         -1.0  
                       4          5.0          0.0          2.0         -1.0  

        my_frame.correlation_matrix computes the common correlation coefficient (Pearson's) on each pair
        of columns in the user-provided list.
        In this example, the *idnum* and most of the columns have trivial correlations: -1, 0, or +1.
        Column *x3* provides a contrasting coefficient of 3 / sqrt(3) = 0.948683298051 .
        The resulting table (specifying all columns) is

        .. code::

            >>> corr_matrix = my_frame.correlation_matrix(my_frame.column_names)
            >>> corr_matrix.inspect()

              idnum:float64       x1:float64        x2:float64        x3:float64   x4:float64  
           ------------------------------------------------------------------------------------
                        1.0              1.0              -1.0    0.948683298051          0.0  
                        1.0              1.0              -1.0    0.948683298051          0.0  
                       -1.0             -1.0               1.0   -0.948683298051          0.0  
             0.948683298051   0.948683298051   -0.948683298051               1.0          0.0  
                        0.0              0.0               0.0               0.0          1.0  



        :param data_column_names: The names of the columns from
            which to compute the matrix.
        :type data_column_names: list
        :param matrix_name: (default=None)  The name for the returned
            matrix Frame.
        :type matrix_name: unicode

        :returns: A Frame with the matrix of the correlation values for the columns.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def count(self, where):
        """
        Counts the number of rows which meet given criteria.

        :param where: |UDF| which evaluates a row to a boolean
        :type where: function

        :returns: number of rows for which the where |UDF| evaluated to True.
        :rtype: int
        """
        return None


    @doc_stub
    def covariance(self, data_column_names):
        """
        Calculate covariance for exactly two columns.

        Notes
        -----
        This method applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column named *obs*:

        .. code::

            >>> cov = my_frame.covariance(['col_0', 'col_1'])
            >>> print(cov)



        :param data_column_names: The names of two columns from which
            to compute the covariance.
        :type data_column_names: list

        :returns: Covariance of the two columns.
        :rtype: dict
        """
        return None


    @doc_stub
    def covariance_matrix(self, data_column_names, matrix_name=None):
        """
        Calculate covariance matrix for two or more columns.

        Notes
        -----
        This function applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame1*, which computes the covariance matrix for three
        numeric columns:

        .. code::

            >>> my_frame1.inspect()

              col_0:int64    col_1:int64   col_3:float64
            \--------------------------------------------\
                1            4             33.4
                2            5             43.7
                3            6             20.1

            >>> cov_matrix = my_frame1.covariance_matrix(['col_0', 'col_1', 'col_2'])
            >>> cov_matrix.inspect()

              col_0:float64    col_1:float64   col_3:float64
            \------------------------------------------------\
                 1.00             1.00            -6.65
                 1.00             1.00            -6.65
                 -6.65           -6.65            139.99

        Consider Frame *my_frame2*, which computes the covariance matrix for a single
        vector column:

        .. code::

            >>> my_frame2.inspect()

              State:unicode             Population_HISTOGRAM:vector
            \-------------------------------------------------------\
                Louisiana               [0.0, 1.0, 0.0, 0.0]
                Georgia                 [0.0, 1.0, 0.0, 0.0]
                Texas                   [0.0, 0.54, 0.46, 0.0]
                Florida                 [0.0, 0.83, 0.17, 0.0]

            >>> cov_matrix = my_frame2.covariance_matrix(['Population_HISTOGRAM'])
            >>> cov_matrix.inspect()

              Population_HISTOGRAM:vector
            \-------------------------------------\
              [0,  0.00000000,  0.00000000,    0]
              [0,  0.04709167, -0.04709167,    0]
              [0, -0.04709167,  0.04709167,    0]
              [0,  0.00000000,  0.00000000,    0]




        :param data_column_names: The names of the column from which to compute the matrix.
            Names should refer to a single column of type vector, or two or more
            columns of numeric scalars.
        :type data_column_names: list
        :param matrix_name: (default=None)  The name of the new
            matrix.
        :type matrix_name: unicode

        :returns: A matrix with the covariance values for the columns.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def cumulative_percent(self, sample_col):
        """
        Add column to frame with cumulative percent sum.

        A cumulative percent sum is computed by sequentially stepping through the
        rows, observing the column values and keeping track of the current percentage of the total sum
        accounted for at the current value.


        Notes
        -----
        This method applies only to columns containing numerical data.
        Although this method will execute for columns containing negative
        values, the interpretation of the result will change (for example,
        negative percentages).

        Examples
        --------
        Consider Frame *my_frame* accessing a frame that contains a single
        column named *obs*:

        .. code::

            >>> my_frame.inspect()

              obs:int32
            /-----------/
                 0
                 1
                 2
                 0
                 1
                 2

        The cumulative percent sum for column *obs* is obtained by:

        .. code::

            >>> my_frame.cumulative_percent('obs')

        The Frame *my_frame* now contains two columns *obs* and
        *obsCumulativePercentSum*.
        They contain the original data and the cumulative percent sum,
        respectively:

        .. code::

            >>> my_frame.inspect()

              obs:int32   obs_cumulative_percent:float64
            /--------------------------------------------/
                 0                             0.0
                 1                             0.16666666
                 2                             0.5
                 0                             0.5
                 1                             0.66666666
                 2                             1.0



        :param sample_col: The name of the column from which to compute
            the cumulative percent sum.
        :type sample_col: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def cumulative_sum(self, sample_col):
        """
        Add column to frame with cumulative percent sum.

        A cumulative sum is computed by sequentially stepping through the rows,
        observing the column values and keeping track of the cumulative sum for each value.

        Notes
        -----
        This method applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column named *obs*:

        .. code::

             >>> my_frame.inspect()

               obs:int32
             /-----------/
                  0
                  1
                  2
                  0
                  1
                  2

        The cumulative sum for column *obs* is obtained by:

        .. code::

            >>> my_frame.cumulative_sum('obs')

        The Frame *my_frame* accesses the original frame that now contains two
        columns, *obs* that contains the original column values, and
        *obsCumulativeSum* that contains the cumulative percent count:

        .. code::

            >>> my_frame.inspect()

              obs:int32   obs_cumulative_sum:int32
            /--------------------------------------/
                 0                          0
                 1                          1
                 2                          3
                 0                          3
                 1                          4
                 2                          6



        :param sample_col: The name of the column from which to compute
            the cumulative sum.
        :type sample_col: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def dot_product(self, left_column_names, right_column_names, dot_product_column_name, default_left_values=None, default_right_values=None):
        """
        Calculate dot product for each row in current frame.

        Calculate the dot product for each row in a frame using values from two
        equal-length sequences of columns.

        Dot product is computed by the following formula:

        The dot product of two vectors :math:`A=[a_1, a_2, ..., a_n]` and
        :math:`B =[b_1, b_2, ..., b_n]` is :math:`a_1*b_1 + a_2*b_2 + ...+ a_n*b_n`.
        The dot product for each row is stored in a new column in the existing frame.

        Notes
        -----
        If default_left_values or default_right_values are not specified, any null
        values will be replaced by zeros.

        Examples
        --------
        Calculate the dot product for a sequence of columns in Frame object *my_frame*:

        .. code::

             >>> my_frame.inspect()

               col_0:int32  col_1:float64  col_2:int32  col3:int32
             /-----------------------------------------------------/
               1            0.2            -2           5
               2            0.4            -1           6
               3            0.6             0           7
               4            0.8             1           8
               5            None            2           None

        Modify the frame by computing the dot product for a sequence of columns:

        .. code::

             >>> my_frame.dot_product(['col_0','col_1'], ['col_2', 'col_3'], 'dot_product')
             >>> my_frame.inspect()

               col_0:int32  col_1:float64 col_2:int32 col3:int32  dot_product:float64
             /------------------------------------------------------------------------/
               1            0.2           -2          5            -1.0
               2            0.4           -1          6             0.4
               3            0.6            0          7             4.2
               4            0.8            1          8            10.4
               5            None           2          None         10.0

        Modify the frame by computing the dot product with default values for nulls:

        .. only:: html

            .. code::

                 >>> my_frame.dot_product(['col_0','col_1'], ['col_2', 'col_3'], 'dot_product_2', [0.1, 0.2], [0.3, 0.4])
                 >>> my_frame.inspect()

                   col_0:int32  col_1:float64 col_2:int32 col3:int32  dot_product:float64  dot_product_2:float64
                 /--------------------------------------------------------------------------------------------/
                    1            0.2           -2          5            -1.0               -1.0
                    2            0.4           -1          6             0.4                0.4
                    3            0.6            0          7             4.2                4.2
                    4            0.8            1          8            10.4                10.4
                    5            None           2          None         10.0                10.08

        .. only:: latex

            .. code::

                 >>> my_frame.dot_product(['col_0','col_1'], ['col_2', 'col_3'],
                 ... 'dot_product_2', [0.1, 0.2], [0.3, 0.4])
                 >>> my_frame.inspect()

                   col_0  col_1    col_2  col3   dot_product  dot_product_2
                   int32  float64  int32  int32  float64      float64
                 /----------------------------------------------------------/
                    1     0.2      -2     5         -1.0         -1.0
                    2     0.4      -1     6          0.4          0.4
                    3     0.6       0     7          4.2          4.2
                    4     0.8       1     8         10.4          10.4
                    5     None      2     None      10.0          10.08

        Calculate the dot product for columns of vectors in Frame object *my_frame*:

        .. code::

             >>> my_frame.dot_product('col_4', 'col_5, 'dot_product')

             col_4:vector  col_5:vector  dot_product:float64
             /----------------------------------------------/
              [1, 0.2]     [-2, 5]       -1.0
              [2, 0.4]     [-1, 6]        0.4
              [3, 0.6]     [0,  7]        4.2
              [4, 0.8]     [1,  8]       10.4


        :param left_column_names: Names of columns used to create the left vector (A) for each row.
            Names should refer to a single column of type vector, or two or more
            columns of numeric scalars.
        :type left_column_names: list
        :param right_column_names: Names of columns used to create right vector (B) for each row.
            Names should refer to a single column of type vector, or two or more
            columns of numeric scalars.
        :type right_column_names: list
        :param dot_product_column_name: Name of column used to store the
            dot product.
        :type dot_product_column_name: unicode
        :param default_left_values: (default=None)  Default values used to substitute null values in left vector.
            Default is None.
        :type default_left_values: list
        :param default_right_values: (default=None)  Default values used to substitute null values in right vector.
            Default is None.
        :type default_right_values: list

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def download(self, n=100, offset=0, columns=None):
        """
        Download a frame from the server into client workspace.

        Copies an trustedanalytics Frame into a Pandas DataFrame.


        Examples
        --------
        Frame *my_frame* accesses a frame with millions of rows of data.
        Get a sample of 500 rows:

        .. code::

            >>> pandas_frame = my_frame.download( 500 )

        We now have a new frame accessed by a pandas DataFrame *pandas_frame*
        with a copy of the first 500 rows of the original frame.

        If we use the method with an offset like:

        .. code::

            >>> pandas_frame = my_frame.take( 500, 100 )

        We end up with a new frame accessed by the pandas DataFrame
        *pandas_frame* again, but this time it has a copy of rows 101 to 600 of
        the original frame.



        :param n: (default=100)  The number of rows to download to the client
        :type n: int
        :param offset: (default=0)  The number of rows to skip before copying
        :type offset: int
        :param columns: (default=None)  Column filter, the names of columns to be included (default is all columns)
        :type columns: list

        :returns: A new pandas dataframe object containing the downloaded frame data
        :rtype: pandas.DataFrame
        """
        return None


    @doc_stub
    def drop_columns(self, columns):
        """
        Remove columns from the frame.

        The data from the columns is lost.

        Notes
        -----
        It is not possible to delete all columns from a frame.
        At least one column needs to remain.
        If it is necessary to delete all columns, then delete the frame.

        Examples
        --------
        For this example, Frame object *my_frame* accesses a frame with
        columns *column_a*, *column_b*, *column_c* and *column_d*.

        .. only:: html

            .. code::

                >>> print my_frame.schema
                [("column_a", str), ("column_b", ta.int32), ("column_c", str), ("column_d", ta.int32)]

        .. only:: latex

            .. code::

                >>> print my_frame.schema
                [("column_a", str), ("column_b", ta.int32), ("column_c", str),
                ("column_d", ta.int32)]

        Eliminate columns *column_b* and *column_d*:

        .. code::

            >>> my_frame.drop_columns(["column_b", "column_d"])
            >>> print my_frame.schema
            [("column_a", str), ("column_c", str)]


        Now the frame only has the columns *column_a* and *column_c*.
        For further examples, see: ref:`example_frame.drop_columns`.




        :param columns: Column name OR list of column names to be removed from the frame.
        :type columns: list

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def drop_duplicates(self, unique_columns=None):
        """
        Modify the current frame, removing duplicate rows.

        Remove data rows which are the same as other rows.
        The entire row can be checked for duplication, or the search for duplicates
        can be limited to one or more columns.
        This modifies the current frame.

        Examples
        --------
        Given a Frame *my_frame* with data:

        .. code::

            >>> my_frame.inspect(11)
              a:int32   b:int32   c:int32
            /-------------------------------/
                  200         4        25
                  200         5        25
                  200         4        25
                  200         5        35
                  200         6        25
                  200         8        35
                  200         4        45
                  200         4        25
                  200         5        25
                  200         5        35
                  201         4        25

        Remove any rows that are identical to a previous row.
        The result is a frame of unique rows.
        Note that row order may change.

        .. code::

            >>> my_frame.drop_duplicates()
            >>> my_frame.inspect(11)
              a:int32   b:int32   c:int32
            /-------------------------------/
                  200         4        25
                  200         6        25
                  200         4        45
                  201         4        25
                  200         5        35
                  200         5        25
                  200         8        35

        Instead of that, remove any rows that have the same data in columns *a* and 
        *c* as a previously checked row:

        .. code::

           >>> my_frame.drop_duplicates([ "a", "c"])

        The result is a frame with unique values for the combination of columns *a*
        and *c*.

        .. code::

            >>>my_frame.inspect(11)
              a:int32   b:int32   c:int32
            /-------------------------------/
                  200         4        45
                  200         4        25
                  200         8        35
                  201         4        25

        Remove any rows that have the same data in column *b* as a previously
        checked row:

        .. code::

            >>> my_frame.drop_duplicates("b")

        The result is a frame with unique values in column *b*.

        .. code::

              a:int32   b:int32   c:int32
            /-------------------------------/
                  200         8        35  
                  200         4        45  


        :param unique_columns: (default=None)  
        :type unique_columns: None

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def drop_rows(self, predicate):
        """
        Erase any row in the current frame which qualifies.

        Examples
        --------
        For this example, my_frame is a Frame object accessing a frame with
        lots of data for the attributes of ``lions``, ``tigers``, and
        ``ligers``.
        Get rid of the ``lions`` and ``tigers``:

        .. code::

            >>> my_frame.drop_rows(lambda row: row.animal_type == "lion" or
            ...    row.animal_type == "tiger")

        Now the frame only has information about ``ligers``.

        More information on a |UDF| can be found at :doc:`/ds_apir`.




        :param predicate: |UDF| which evaluates a row to a boolean; rows that answer True are dropped from the Frame
        :type predicate: function
        """
        return None


    @doc_stub
    def ecdf(self, column, result_frame_name=None):
        """
        Builds new frame with columns for data and distribution.

        Generates the empirical cumulative distribution for the input column.

        Examples
        --------
        Consider the following sample data set in *frame* with actual data labels
        specified in the *labels* column and the predicted labels in the
        *predictions* column:

        .. code::

            >>> import trustedanalytics as ta
            >>> import pandas as p
            >>> f = ta.Frame(ta.Pandas(p.DataFrame([1, 3, 1, 0]), [('numbers', ta.int32)]))

            [==Job Progress...]

            >>> f.take(5)
            [[1], [3], [1], [0]]

            [==Job Progress...]

            >>> result = f.ecdf('numbers')
            >>> result.inspect()

              b:int32   b_ECDF:float64
            /--------------------------/
               1             0.2
               2             0.5
               3             0.8
               4             1.0



        :param column: The name of the input column containing sample.
        :type column: unicode
        :param result_frame_name: (default=None)  A name for the resulting frame which is created
            by this operation.
        :type result_frame_name: unicode

        :returns: A new Frame containing each distinct value in the sample and its corresponding ECDF value.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def entropy(self, data_column, weights_column=None):
        """
        Calculate the Shannon entropy of a column.

        The data column is weighted via the weights column.
        All data elements of weight <= 0 are excluded from the calculation, as are
        all data elements whose weight is NaN or infinite.
        If there are no data elements with a finite weight greater than 0,
        the entropy is zero.

        Examples
        --------
        Given a frame of coin flips, half heads and half tails, the entropy is simply ln(2):
        .. code::

            >>> print frame.inspect()

                      data:unicode  
                    /----------------/
                      H             
                      T             
                      H             
                      T             
                      H             
                      T             
                      H             
                      T             
                      H             
                      T             

            >>> print "Computed entropy:", frame.entropy("data")

                    Computed entropy: 0.69314718056

        If we have more choices and weights, the computation is not as simple.
        An on-line search for "Shannon Entropy" will provide more detail.

        .. code::

           >>> print frame.inspect()
                      data:int32   weight:int32  
                    -----------------------------
                               0              1  
                               1              2  
                               2              4  
                               4              8  

           >>> print "Computed entropy:", frame.entropy("data", "weight")

                    Computed entropy: 1.13691659183



        :param data_column: The column whose entropy is to be calculated.
        :type data_column: unicode
        :param weights_column: (default=None)  The column that provides weights (frequencies) for the entropy calculation.
            Must contain numerical data.
            Default is using uniform weights of 1 for all items.
        :type weights_column: unicode

        :returns: Entropy.
        :rtype: dict
        """
        return None


    @doc_stub
    def export_to_csv(self, folder_name, separator=None, count=None, offset=None):
        """
        Write current frame to HDFS in csv format.

        Export the frame to a file in csv format as a Hadoop file.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_csv('covarianceresults')



        :param folder_name: The HDFS folder path where the files
            will be created.
        :type folder_name: unicode
        :param separator: (default=None)  
        :type separator: None
        :param count: (default=None)  The number of records you want.
            Default, or a non-positive value, is the whole frame.
        :type count: int32
        :param offset: (default=None)  The number of rows to skip before exporting to the file.
            Default is zero (0).
        :type offset: int32

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def export_to_hbase(self, table_name, key_column_name=None, family_name=None):
        """
        Write current frame to HBase table.

        Table must exist in HBase.
        Export of Vectors is not currently supported.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_hbase('covarianceresults')



        :param table_name: The name of the HBase table that will contain the exported frame
        :type table_name: unicode
        :param key_column_name: (default=None)  The name of the column to be used as row key in hbase table
        :type key_column_name: unicode
        :param family_name: (default=None)  The family name of the HBase table that will contain the exported frame
        :type family_name: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def export_to_hive(self, table_name):
        """
        Write current frame to Hive table.

        Table must not exist in Hive.
        Export of Vectors is not currently supported.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_hive('covarianceresults')

        :param table_name: The name of the Hive table that will contain the exported frame
        :type table_name: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def export_to_jdbc(self, table_name, connector_type=None, url=None, driver_name=None, query=None):
        """
        Write current frame to JDBC table.

        Table will be created or appended to.
        Export of Vectors is not currently supported.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_jdbc('covarianceresults')



        :param table_name: JDBC table name
        :type table_name: unicode
        :param connector_type: (default=None)  (optional) JDBC connector type
        :type connector_type: unicode
        :param url: (default=None)  (optional) connection url (includes server name, database name, user acct and password
        :type url: unicode
        :param driver_name: (default=None)  (optional) driver name
        :type driver_name: unicode
        :param query: (default=None)  (optional) query for filtering. Not supported yet.
        :type query: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def export_to_json(self, folder_name, count=None, offset=None):
        """
        Write current frame to HDFS in JSON format.

        Export the frame to a file in JSON format as a Hadoop file.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_json('covarianceresults')



        :param folder_name: The HDFS folder path where the files
            will be created.
        :type folder_name: unicode
        :param count: (default=None)  The number of records you want.
            Default, or a non-positive value, is the whole frame.
        :type count: int32
        :param offset: (default=None)  The number of rows to skip before exporting to the file.
            Default is zero (0).
        :type offset: int32

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def filter(self, predicate):
        """
        Select all rows which satisfy a predicate.

        Modifies the current frame to save defined rows and delete everything
        else.

        Examples
        --------
        For this example, *my_frame* is a Frame object with lots of data for
        the attributes of ``lizards``, ``frogs``, and ``snakes``.
        Get rid of everything, except information about ``lizards`` and
        ``frogs``:

        .. code::

            >>> def my_filter(row):
            ... return row['animal_type'] == 'lizard' or
            ... row['animal_type'] == "frog"

            >>> my_frame.filter(my_filter)

        The frame now only has data about ``lizards`` and ``frogs``.

        More information on a |UDF| can be found at :doc:`/ds_apir`.



        :param predicate: |UDF| which evaluates a row to a boolean; rows that answer False are dropped from the Frame
        :type predicate: function
        """
        return None


    @doc_stub
    def flatten_column(self, column, delimiter=None):
        """
        Spread data to multiple rows based on cell data.

        Splits cells in the specified column into multiple rows according to a string
        delimiter.
        New rows are a full copy of the original row, but the specified column only
        contains one value.
        The original row is deleted.

        Examples
        --------
        Given a data file::

            1-"solo,mono,single"
            2-"duo,double"

        The commands to bring the data into a frame, where it can be worked on:

        .. only:: html

            .. code::

                >>> my_csv = CsvFile("original_data.csv", schema=[('a', int32), ('b', str)], delimiter='-')
                >>> my_frame = Frame(source=my_csv)

        .. only:: latex

            .. code::

                >>> my_csv = CsvFile("original_data.csv", schema=[('a', int32),
                ... ('b', str)], delimiter='-')
                >>> my_frame = Frame(source=my_csv)

        Looking at it:

        .. code::

            >>> my_frame.inspect()

              a:int32   b:str
            /-------------------------------/
                1       solo, mono, single
                2       duo, double

        Now, spread out those sub-strings in column *b*:

        .. code::

            >>> my_frame.flatten_column('b')

        Check again:

        .. code::

            >>> my_frame.inspect()

              a:int32   b:str
            /------------------/
                1       solo
                1       mono
                1       single
                2       duo
                2       double



        :param column: The column to be flattened.
        :type column: unicode
        :param delimiter: (default=None)  The delimiter string.
            Default is comma (,).
        :type delimiter: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def get_error_frame(self):
        """
        Get a frame with error recordings.

        When a frame is created, another frame is transparently
        created to capture parse errors.

        Returns
        -------
        Frame : error frame object
            A new object accessing a frame that contains the parse errors of
            the currently active Frame or None if no error frame exists.



        """
        return None


    @doc_stub
    def group_by(self, group_by_columns, aggregation_arguments=None):
        """
        Create summarized frame.

        Creates a new frame and returns a Frame object to access it.
        Takes a column or group of columns, finds the unique combination of
        values, and creates unique rows with these column values.
        The other columns are combined according to the aggregation
        argument(s).

        Notes
        -----
        *   Column order is not guaranteed when columns are added
        *   The column names created by aggregation functions in the new frame
            are the original column name appended with the '_' character and
            the aggregation function.
            For example, if the original field is *a* and the function is
            *avg*, the resultant column is named *a_avg*.
        *   An aggregation argument of *count* results in a column named
            *count*.
        *   The aggregation function *agg.count* is the only full row
            aggregation function supported at this time.
        *   Aggregation currently supports using the following functions:

            *   avg
            *   count
            *   count_distinct
            *   max
            *   min
            *   stdev
            *   sum
            *   var (see glossary Bias vs Variance)

        Examples
        --------
        For setup, we will use a Frame *my_frame* accessing a frame with a
        column *a*:

        .. code::

            >>> my_frame.inspect()

              a:str
            /-------/
              cat
              apple
              bat
              cat
              bat
              cat

        Create a new frame, combining similar values of column *a*,
        and count how many of each value is in the original frame:

        .. code::

            >>> new_frame = my_frame.group_by('a', agg.count)
            >>> new_frame.inspect()

              a:str       count:int
            /-----------------------/
              cat             3
              apple           1
              bat             2

        In this example, 'my_frame' is accessing a frame with three columns,
        *a*, *b*, and *c*:

        .. code::

            >>> my_frame.inspect()

              a:int   b:str   c:float
            /-------------------------/
              1       alpha     3.0
              1       bravo     5.0
              1       alpha     5.0
              2       bravo     8.0
              2       bravo    12.0

        Create a new frame from this data, grouping the rows by unique
        combinations of column *a* and *b*.
        Average the value in *c* for each group:

        .. code::

            >>> new_frame = my_frame.group_by(['a', 'b'], {'c' : agg.avg})
            >>> new_frame.inspect()

              a:int   b:str   c_avg:float
            /-----------------------------/
              1       alpha     4.0
              1       bravo     5.0
              2       bravo    10.0

        For this example, we use *my_frame* with columns *a*, *c*, *d*,
        and *e*:

        .. code::

            >>> my_frame.inspect()

              a:str   c:int   d:float e:int
            /-------------------------------/
              ape     1       4.0     9
              ape     1       8.0     8
              big     1       5.0     7
              big     1       6.0     6
              big     1       8.0     5

        Create a new frame from this data, grouping the rows by unique
        combinations of column *a* and *c*.
        Count each group; for column *d* calculate the average, sum and minimum
        value.
        For column *e*, save the maximum value:

        .. only:: html

            .. code::

                >>> new_frame = my_frame.group_by(['a', 'c'], agg.count, {'d': [agg.avg, agg.sum, agg.min], 'e': agg.max})

                  a:str   c:int   count:int  d_avg:float  d_sum:float   d_min:float   e_max:int
                /-------------------------------------------------------------------------------/
                  ape     1       2          6.0          12.0          4.0           9
                  big     1       3          6.333333     19.0          5.0           7

        .. only:: latex

            .. code::

                >>> new_frame = my_frame.group_by(['a', 'c'], agg.count,
                ... {'d': [agg.avg, agg.sum, agg.min], 'e': agg.max})

                  a    c    count  d_avg  d_sum  d_min  e_max
                  str  int  int    float  float  float  int
                /---------------------------------------------/
                  ape  1    2      6.0    12.0   4.0    9
                  big  1    3      6.333  19.0   5.0    7


        For further examples, see :ref:`example_frame.group_by`.


        :param group_by_columns: Column name or list of column names
        :type group_by_columns: list
        :param aggregation_arguments: (default=None)  Aggregation function based on entire row, and/or dictionaries (one or more) of { column name str : aggregation function(s) }.
        :type aggregation_arguments: dict

        :returns: A new frame with the results of the group_by
        :rtype: Frame
        """
        return None


    @doc_stub
    def histogram(self, column_name, num_bins=None, weight_column_name=None, bin_type='equalwidth'):
        """
        Compute the histogram for a column in a frame.

        Compute the histogram of the data in a column.
        The returned value is a Histogram object containing 3 lists one each for:
        the cutoff points of the bins, size of each bin, and density of each bin.

        **Notes**

        The num_bins parameter is considered to be the maximum permissible number
        of bins because the data may dictate fewer bins.
        With equal depth binning, for example, if the column to be binned has 10
        elements with only 2 distinct values and the *num_bins* parameter is
        greater than 2, then the number of actual number of bins will only be 2.
        This is due to a restriction that elements with an identical value must
        belong to the same bin.

        Examples
        --------
        Consider the following sample data set\:

        .. code::

            >>> frame.inspect()

              a:unicode  b:int32
            /--------------------/
                a          2
                b          7
                c          3
                d          9
                e          1

        A simple call for 3 equal-width bins gives\:

        .. code::

            >>> hist = frame.histogram("b", num_bins=3)
            >>> print hist

            Histogram:
                cutoffs: cutoffs: [1.0, 3.6666666666666665, 6.333333333333333, 9.0],
                hist: [3, 0, 2],
                density: [0.6, 0.0, 0.4]


        Switching to equal depth gives\:

        .. code::

            >>> hist = frame.histogram("b", num_bins=3, bin_type='equaldepth')
            >>> print hist

            Histogram:
                cutoffs: [1, 2, 7, 9],
                hist: [1, 2, 2],
                density: [0.2, 0.4, 0.4]


        .. only:: html

               Plot hist as a bar chart using matplotlib\:

            .. code::

                >>> import matplotlib.pyplot as plt

                >>> plt.bar(hist.cutoffs[:1], hist.hist, width=hist.cutoffs[1] - hist.cutoffs[0])

        .. only:: latex

               Plot hist as a bar chart using matplotlib\:

            .. code::

                >>> import matplotlib.pyplot as plt

                >>> plt.bar(hist.cutoffs[:1], hist.hist, width=hist.cutoffs[1] - 
                ... hist.cutoffs[0])



        :param column_name: Name of column to be evaluated.
        :type column_name: unicode
        :param num_bins: (default=None)  Number of bins in histogram.
            Default is Square-root choice will be used
            (in other words math.floor(math.sqrt(frame.row_count)).
        :type num_bins: int32
        :param weight_column_name: (default=None)  Name of column containing weights.
            Default is all observations are weighted equally.
        :type weight_column_name: unicode
        :param bin_type: (default=equalwidth)  The type of binning algorithm to use: ["equalwidth"|"equaldepth"]
            Defaults is "equalwidth".
        :type bin_type: unicode

        :returns: histogram
                A Histogram object containing the result set.
                The data returned is composed of multiple components:
            cutoffs : array of float
                A list containing the edges of each bin.
            hist : array of float
                A list containing count of the weighted observations found in each bin.
            density : array of float
                A list containing a decimal containing the percentage of
                observations found in the total set per bin.
        :rtype: dict
        """
        return None


    @doc_stub
    def inspect(self, n=10, offset=0, columns=None, wrap='inspect_settings', truncate='inspect_settings', round='inspect_settings', width='inspect_settings', margin='inspect_settings', with_types='inspect_settings'):
        """
        Pretty-print of the frame data

        Essentially returns a string, but technically returns a RowInspection object which renders a string.
        The RowInspection object naturally converts to a str when needed, like when printed or when displayed
        by python REPL (i.e. using the object's __repr__).  If running in a script and want the inspect output
        to be printed, then it must be explicitly printed, then `print frame.inspect()`

        Examples
        --------
        Given a frame of data and a Frame to access it.
        To look at the first 4 rows of data:

        .. code::

            >>> my_frame.inspect(4)
           [#]    animal      name    age     weight
           =========================================
           [0]  human       George      8      542.5
           [1]  human       Ursula      6      495.0
           [2]  ape         Ape        41      400.0
           [3]  elephant    Shep        5     8630.0

        # For other examples, see :ref:`example_frame.inspect`.

        **Global Settings**

        If not specified, the arguments that control formatting receive default values from
        'trustedanalytics.inspect_settings'.  Make changes there to affect all calls to inspect.

        .. code::

            >>> import trustedanalytics as ta
            >>> ta.inspect_settings
            wrap             20
            truncate       None
            round          None
            width            80
            margin         None
            with_types    False
            >>> ta.inspect_settings.width = 120  # changes inspect to use 120 width globally
            >>> ta.inspect_settings.truncate = 16  # changes inspect to always truncate strings to 16 chars
            >>> ta.inspect_settings
            wrap             20
            truncate         16
            round          None
            width           120
            margin         None
            with_types    False
            >>> ta.inspect_settings.width = None  # return value back to default
            >>> ta.inspect_settings
            wrap             20
            truncate         16
            round          None
            width            80
            margin         None
            with_types    False
            >>> ta.inspect_settings.reset()  # set everything back to default
            >>> ta.inspect_settings
            wrap             20
            truncate       None
            round          None
            width            80
            margin         None
            with_types    False

        ..


        :param n: (default=10)  The number of rows to print.
        :type n: int
        :param offset: (default=0)  The number of rows to skip before printing.
        :type offset: int
        :param columns: (default=None)  Filter columns to be included.  By default, all columns are included
        :type columns: int
        :param wrap: (default=inspect_settings)  If set to 'stripes' then inspect prints rows in stripes; if set to an integer N, rows will be printed in clumps of N columns, where the columns are wrapped
        :type wrap: int or 'stripes'
        :param truncate: (default=inspect_settings)  If set to integer N, all strings will be truncated to length N, including a tagged ellipses
        :type truncate: int
        :param round: (default=inspect_settings)  If set to integer N, all floating point numbers will be rounded and truncated to N digits
        :type round: int
        :param width: (default=inspect_settings)  If set to integer N, the print out will try to honor a max line width of N
        :type width: int
        :param margin: (default=inspect_settings)  ('stripes' mode only) If set to integer N, the margin for printing names in a stripe will be limited to N characters
        :type margin: int
        :param with_types: (default=inspect_settings)  If set to True, header will include the data_type of each column
        :type with_types: bool

        :returns: An object which naturally converts to a pretty-print string
        :rtype: RowsInspection
        """
        return None


    @doc_stub
    def join(self, right, left_on, right_on=None, how='inner', name=None):
        """
        Join operation on one or two frames, creating a new frame.

        Create a new frame from a SQL JOIN operation with another frame.
        The frame on the 'left' is the currently active frame.
        The frame on the 'right' is another frame.
        This method takes a column in the left frame and matches its values
        with a column in the right frame.
        Using the default 'how' option ['inner'] will only allow data in the
        resultant frame if both the left and right frames have the same value
        in the matching column.
        Using the 'left' 'how' option will allow any data in the resultant
        frame if it exists in the left frame, but will allow any data from the
        right frame if it has a value in its column which matches the value in
        the left frame column.
        Using the 'right' option works similarly, except it keeps all the data
        from the right frame and only the data from the left frame when it
        matches.
        The 'outer' option provides a frame with data from both frames where
        the left and right frames did not have the same value in the matching
        column.

        Notes
        -----
        When a column is named the same in both frames, it will result in two
        columns in the new frame.
        The column from the *left* frame (originally the current frame) will be
        copied and the column name will have the string "_L" added to it.
        The same thing will happen with the column from the *right* frame,
        except its name has the string "_R" appended. The order of columns
        after this method is called is not guaranteed.

        It is recommended that you rename the columns to meaningful terms prior
        to using the ``join`` method.
        Keep in mind that unicode in column names will likely cause the
        drop_frames() method (and others) to fail!

        Examples
        --------
        For this example, we will use a Frame *my_frame* accessing a frame with
        columns *a*, *b*, *c*, and a Frame *your_frame* accessing a frame with
        columns *a*, *d*, *e*.
        Join the two frames keeping only those rows having the same value in
        column *a*:

        .. code::

            >>> print my_frame.inspect()

              a:unicode   b:unicode   c:unicode
            /--------------------------------------/
              alligator   bear        cat
              apple       berry       cantaloupe
              auto        bus         car
              mirror      frog        ball

            >>> print your_frame.inspect()

              b:unicode   c:int   d:unicode
            /-------------------------------------/
              berry        5218   frog
              blue            0   log
              bus           871   dog

            >>> joined_frame = my_frame.join(your_frame, 'b', how='inner')

        Now, joined_frame is a Frame accessing a frame with the columns *a*,
        *b*, *c_L*, *ci_R*, and *d*.
        The data in the new frame will be from the rows where column 'a' was
        the same in both frames.

        .. code::

            >>> print joined_frame.inspect()

              a:unicode   b:unicode     c_L:unicode   c_R:int64   d:unicode
            /-------------------------------------------------------------------/
              apple       berry         cantaloupe         5218   frog
              auto        bus           car                 871   dog

        More examples can be found in the :ref:`user manual
        <example_frame.join>`.



        :param right: Another frame to join with
        :type right: Frame
        :param left_on: Name of the column in the left frame used to match up the two frames.
        :type left_on: str
        :param right_on: (default=None)  Name of the column in the right frame used to match up the two frames. Default is the same as the left frame.
        :type right_on: str
        :param how: (default=inner)  How to qualify the data to be joined together.  Must be one of the following:  'left', 'right', 'inner', 'outer'.  Default is 'inner'
        :type how: str
        :param name: (default=None)  Name of the result grouped frame
        :type name: str

        :returns: A new frame with the results of the join
        :rtype: Frame
        """
        return None


    @doc_stub
    def label_propagation(self, src_col_name, dest_col_name, weight_col_name, src_label_col_name, result_col_name=None, max_iterations=None, convergence_threshold=None, alpha=None):
        """
        Label Propagation on Gaussian Random Fields.

        Label Propagation on Gaussian Random Fields.

        This algorithm is presented in `X. Zhu and Z. Ghahramani.
        Learning from labeled and unlabeled data with label propagation.
        Technical Report CMU-CALD-02-107, CMU, 2002 <http://www.cs.cmu.edu/~zhuxj/pub/CMU-CALD-02-107.pdf>`__.

        **Label Propagation (LP)**

        |LP| is a message passing technique for inputing or
        smoothing labels in partially-labeled datasets.
        Labels are propagated from *labeled* data to *unlabeled* data along a graph
        encoding similarity relationships among data points.
        The labels of known data can be probabilistic, in other words, a known point
        can be represented with fuzzy labels such as 90% label 0 and 10% label 1.
        The inverse distance between data points is represented by edge weights, with
        closer points having a higher weight (stronger influence
        on posterior estimates) than points farther away.
        |LP| has been used for many problems, particularly those involving a similarity
        measure between data points.
        Our implementation is based on Zhu and Ghahramani's 2002 paper,
        `Learning from labeled and unlabeled data. <http://www.cs.cmu.edu/~zhuxj/pub/CMU-CALD-02-107.pdf>`__.

        **The Label Propagation Algorithm**

        In |LP|, all nodes start with a prior distribution of states and the initial
        messages vertices pass to their neighbors are simply their prior beliefs.
        If certain observations have states that are known deterministically, they can
        be given a prior probability of 100% for their true state and 0% for all others.
        Unknown observations should be given uninformative priors.

        Each node, :math:`i`, receives messages from its :math:`k` neighbors and
        updates its beliefs by taking a weighted average of its current beliefs
        and a weighted average of the messages received from its neighbors.

        The updated beliefs for node :math:`i` are:

        .. math::

            updated\ beliefs_{i} = \lambda * (prior\ belief_{i} ) + (1 - \lambda ) \
            * \sum_k w_{i,k} * previous\ belief_{k}

        where :math:`w_{i,k}` is the normalized weight between nodes :math:`i` and
        :math:`k`, normalized such that the sum of all weights to neighbors is 1.

        :math:`\lambda` is a leaning parameter.
        If :math:`\lambda` is greater than zero, updated probabilities will be anchored
        in the direction of prior beliefs.

        The final distribution of state probabilities will also tend to be biased in
        the direction of the distribution of initial beliefs.
        For the first iteration of updates, nodes' previous beliefs are equal to the
        priors, and, in each future iteration,
        previous beliefs are equal to their beliefs as of the last iteration.
        All beliefs for every node will be updated in this fashion, including known
        observations, unless ``anchor_threshold`` is set.
        The ``anchor_threshold`` parameter specifies a probability threshold above
        which beliefs should no longer be updated.
        Hence, with an ``anchor_threshold`` of 0.99, observations with states known
        with 100% certainty will not be updated by this algorithm.

        This process of updating and message passing continues until the convergence
        criteria is met, or the maximum number of supersteps is reached.
        A node is said to converge if the total change in its cost function is below
        the convergence threshold.
        The cost function for a node is given by:

        .. math::

            cost =& \sum_k w_{i,k} * \Big[ \big( 1 - \lambda \big) * \big[ previous\ \
            belief_{i}^{2} - w_{i,k} * previous\ belief_{i} * \\
            & previous\ belief_{k} \big] + 0.5 * \lambda * \big( previous\ belief_{i} \
            - prior_{i} \big) ^{2} \Big]


        Convergence is a local phenomenon; not all nodes will converge at the same time.
        It is also possible that some (most) nodes will converge and others will not converge.
        The algorithm requires all nodes to converge before declaring global convergence.
        If this condition is not met, the algorithm will continue up to the maximum
        number of supersteps.


        Examples
        --------
        .. only:: html

            .. code::

            input frame (lp.csv)
            "a"        "b"        "c"        "d"
            1,         2,         0.5,       "0.5,0.5"
            2,         3,         0.4,       "-1,-1"
            3,         1,         0.1,       "0.8,0.2"

            script

            ta.connect()
            s = [("a", ta.int32), ("b", ta.int32), ("c", ta.float32), ("d", ta.vector(2))]
            d = "lp.csv"
            c = ta.CsvFile(d,s)
            f = ta.Frame(c)
            r = f.label_propagation("a", "b", "c", "d", "results")
            r['frame'].inspect()
            r['report']

        .. only:: latex

            .. code::

                >>> r = f.label_propagation(
                ... srcColName = "a",
                ... destColName  = "b",
                ... weightColName = "c",
                ... srcLabelColName = "d",
                ... resultColName = "resultLabels")
                ... r['frame'].inspect()
                ... r['report']

        The expected output is like this:

        .. only:: html

            .. code::

                {u'value': u'======Graph Statistics======\nNumber of vertices: 600\nNumber of edges: 15716\n\n======LP Configuration======\nlambda: 0.000000\nanchorThreshold: 0.900000\nconvergenceThreshold: 0.000000\nmaxSupersteps: 10\nbidirectionalCheck: false\n\n======Learning Progress======\nsuperstep = 1\tcost = 0.008692\nsuperstep = 2\tcost = 0.008155\nsuperstep = 3\tcost = 0.007809\nsuperstep = 4\tcost = 0.007544\nsuperstep = 5\tcost = 0.007328\nsuperstep = 6\tcost = 0.007142\nsuperstep = 7\tcost = 0.006979\nsuperstep = 8\tcost = 0.006833\nsuperstep = 9\tcost = 0.006701\nsuperstep = 10\tcost = 0.006580'}

        .. only:: latex

            .. code::

                {u'value': u'======Graph Statistics======\n
                Number of vertices: 600\n
                Number of edges: 15716\n
                \n
                ======LP Configuration======\n
                lambda: 0.000000\n
                anchorThreshold: 0.900000\n
                convergenceThreshold: 0.000000\n
                maxSupersteps: 10\n
                bidirectionalCheck: false\n
                \n
                ======Learning Progress======\n
                superstep = 1\tcost = 0.008692\n
                superstep = 2\tcost = 0.008155\n
                superstep = 3\tcost = 0.007809\n
                superstep = 4\tcost = 0.007544\n
                superstep = 5\tcost = 0.007328\n
                superstep = 6\tcost = 0.007142\n
                superstep = 7\tcost = 0.006979\n
                superstep = 8\tcost = 0.006833\n
                superstep = 9\tcost = 0.006701\n
                superstep = 10\tcost = 0.006580'}



        :param src_col_name: The column name for the
            source vertex id.
        :type src_col_name: unicode
        :param dest_col_name: The column name for the
            destination vertex id.
        :type dest_col_name: unicode
        :param weight_col_name: The column name for the
            edge weight.
        :type weight_col_name: unicode
        :param src_label_col_name: The column name for the
            label properties for the source vertex.
        :type src_label_col_name: unicode
        :param result_col_name: (default=None)  The column name for the
            results (holding the post labels for the vertices).
        :type result_col_name: unicode
        :param max_iterations: (default=None)  The maximum number of supersteps
            that the algorithm will execute.
            The valid value range is all positive int.
            Default is 10.
        :type max_iterations: int32
        :param convergence_threshold: (default=None)  The amount of change in
            cost function that will be tolerated at convergence.
            If the change is less than this threshold, the algorithm exits earlier
            before it reaches the maximum number of supersteps.
            The valid value range is all float and zero.
            Default is 0.00000001f.
        :type convergence_threshold: float32
        :param alpha: (default=None)  The tradeoff parameter that
            controls how much influence an external
            classifier's prediction contributes to the final prediction.
            This is for the case where an external classifier is available that can
            produce initial probabilistic classification on unlabeled examples, and
            the option allows incorporating external classifier's prediction into
            the LP training process.
            The valid value range is [0.0,1.0].
            Default is 0.
        :type alpha: float32

        :returns: A 2-column frame:

            vertex: int
                A vertex id.
            result : Vector (long)
                label vector for the results (for the node id in column 1)
        :rtype: dict
        """
        return None


    @property
    @doc_stub
    def last_read_date(self):
        """
        Last time this frame's data was accessed.



        :returns: Date string of the last time this frame's data was accessed
        :rtype: str
        """
        return None


    @doc_stub
    def loadhbase(self, table_name, schema, start_tag=None, end_tag=None):
        """
        Append data from an HBase table into an existing (possibly empty) FrameRDD

        Append data from an HBase table into an existing (possibly empty) FrameRDD

        :param table_name: hbase table name
        :type table_name: unicode
        :param schema: hbase schema as a list of tuples (columnFamily, columnName, dataType for cell value)
        :type schema: list
        :param start_tag: (default=None)  optional start tag for filtering
        :type start_tag: unicode
        :param end_tag: (default=None)  optional end tag for filtering
        :type end_tag: unicode

        :returns: the initial FrameRDD with the HBase data appended
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def loadhive(self, query):
        """
        Append data from a hive table into an existing (possibly empty) frame

        Append data from a hive table into an existing (possibly empty) frame

        :param query: Initial query to run at load time
        :type query: unicode

        :returns: the initial frame with the hive data appended
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def loadjdbc(self, table_name, connector_type=None, url=None, driver_name=None, query=None):
        """
        Append data from a JDBC table into an existing (possibly empty) frame

        Append data from a JDBC table into an existing (possibly empty) frame

        :param table_name: table name
        :type table_name: unicode
        :param connector_type: (default=None)  (optional) connector type
        :type connector_type: unicode
        :param url: (default=None)  (optional) connection url (includes server name, database name, user acct and password
        :type url: unicode
        :param driver_name: (default=None)  (optional) driver name
        :type driver_name: unicode
        :param query: (default=None)  (optional) query for filtering. Not supported yet.
        :type query: unicode

        :returns: the initial frame with the JDBC data appended
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def loopy_belief_propagation(self, src_col_name, dest_col_name, weight_col_name, src_label_col_name, result_col_name=None, ignore_vertex_type=None, max_iterations=None, convergence_threshold=None, anchor_threshold=None, smoothing=None, max_product=None, power=None):
        """
        Message passing to infer state probabilities.

        Loopy belief propagation on Markov Random Fields (MRF).
        :ref:`Belief Propagation <python_api/graphs/graph-/ml/belief_propagation>`
        (BP) was originally designed for acyclic graphical models, then it
        was found that the |BP| algorithm can be used in general graphs.
        The algorithm is then sometimes called "Loopy" Belief Propagation (LBP),
        because graphs typically contain cycles, or loops.

        **Loopy Belief Propagation (LBP)**

        Loopy Belief Propagation (LBP) is a message passing algorithm for inferring
        state probabilities, given a graph and a set of noisy initial estimates.
        The |LBP| implementation assumes that the joint distribution of the
        data is given by a Boltzmann distribution.

        For more information about |LBP|, see: "K. Murphy, Y. Weiss, and M. Jordan,
        Loopy-belief Propagation for Approximate Inference: An Empirical Study, UAI 1999."

        |LBP| has a wide range of applications in structured prediction, such as
        low-level vision and influence spread in social networks, where we have prior
        noisy predictions for a large set of random variables and a graph encoding
        relationships between those variables.

        The algorithm performs approximate inference on an undirected graph of
        hidden variables, where each variable is represented as a node, and each edge
        encodes relations to its neighbors.
        Initially, a prior noisy estimate of state probabilities is given to each
        node, then the algorithm infers the posterior distribution of each node by
        propagating and collecting messages to and from its neighbors and updating
        the beliefs.

        In graphs containing loops, convergence is not guaranteed, though |LBP| has
        demonstrated empirical success in many areas and in practice often converges
        close to the true joint probability distribution.

        **Discrete Loopy Belief Propagation**

        |LBP| is typically considered a :term:`semi-supervised machine learning
        <Semi-Supervised Learning>` algorithm as

        #)  there is typically no ground truth observation of states
        #)  the algorithm is primarily concerned with estimating a joint
            probability function rather than
            with classification or point prediction.

        The standard (discrete) |LBP| algorithm requires a set of probability thresholds
        to be considered a classifier.
        Nonetheless, the discrete |LBP| algorithm allows Test/Train/Validate splits of
        the data and the algorithm will treat "Train" observations
        differently from "Test" and "Validate" observations.
        Vertices labeled with "Test" or "Validate" will be treated as though they have
        uninformative (uniform) priors and are
        allowed to receive messages, but not send messages.
        This simulates a "scoring scenario" in which a new observation is added to a
        graph containing fully trained |LBP| posteriors, the new vertex is scored based
        on received messages, but the full |LBP| algorithm is not repeated in full.
        This behavior can be turned off by setting the ``ignore_vertex_type`` parameter
        to True.
        When ``ignore_vertex_type=True``, all nodes will be considered "Train"
        regardless of their sample type designation.
        The Gaussian (continuous) version of |LBP| does not allow Train/Test/Validate
        splits.

        The standard |LBP| algorithm included with the toolkit assumes an ordinal and
        cardinal set of discrete states.
        For notational convenience, we'll denote the value of state :math:`s_{i}` as
        :math:`i`, and the prior probability of state
        :math:`s_{i}` as :math:`prior_{i}`.

        Each node sends out initial messages of the form:

        .. math::

           \ln \left ( \sum_{s_{j}} \exp \left ( - \frac { | i - j | ^{p} }{ n - 1 } \
           * w * s + \ln (prior_{i}) \right ) \right )

        Where

        *   :math:`w` is the weight between the messages destination and origin vertices
        *   :math:`s` is the smoothing parameter
        *   :math:`p` is the power parameter
        *   :math:`n` is the number of states

        The larger the weight between two nodes, or the higher the smoothing parameter,
        the more neighboring vertices are assumed to "agree" on states.
        We represent messages as sums of log probabilities rather than products
        of non-logged probabilities which makes it easier to subtract messages in the
        future steps of the algorithm.
        Also note that the states are cardinal in the sense that the "pull" of state
        :math:`i` on state :math:`j` depends on the distance between :math:`i` and
        :math:`j`.
        The *power* parameter intensifies the rate at which the pull of distant states
        drops off.

        In order for the algorithm to work properly, all edges of the graph must be
        bidirectional.
        In other words, messages need to be able to flow in both directions across
        every edge.
        Bidirectional edges can be enforced during graph building, but the |LBP| function
        provides an option to do an initial check for bidirectionality using the
        ``bidirectional_check=True`` option.
        If not all the edges of the graph are bidirectional, the algorithm will return
        an error.

        Look at a case where a node has two states, 0 and 1.
        The 0 state has a prior probability of 0.9 and the 1 state has a prior
        probability of 0.2.
        The states have uniform weights of 1, power of 1 and a smoothing parameter of 2.
        The nodes initial message would be :math:`\textstyle \left [ \ln \left ( 0.2 \
        + 0.8 e ^{-2} \right ), \ln \left ( 0.8 + 0.2 e ^{-2} \right ) \right ]`,
        which gets sent to each of that node's neighbors.
        Note that messages will typically not be proper probability distributions,
        hence each message is normalized so that the probability of all states sum to 1
        before being sent out.
        For simplicity of discussion, we will consider all messages as normalized
        messages.

        After nodes have sent out their initial messages, they then update their
        beliefs based on messages that they have received from their neighbors,
        denoted by the set :math:`k`.

        Updated Posterior Beliefs:

        .. math::

           \ln (newbelief) = \propto \exp \left [ \ln (prior) + \sum_k message _{k} \
           \right ]

        Note that the messages in the above equation are still in log form.
        Nodes then send out new messages which take the same form as their initial
        messages, with updated beliefs in place of priors and subtracting out the
        information previously received from the new message's recipient.
        The recipient's prior message is subtracted out to prevent feedback loops of
        nodes "learning" from themselves.

        .. math::

           \ln \left ( \sum_{s_{j}} \exp \left ( - \frac { | i - j | ^{p} }{ n - 1 } \
           * w * s + \ln (newbelief_{i}) - \
           previous\ message\ from\ recipient \right ) \right )

        In updating beliefs, new beliefs tend to be most influenced by the largest
        message.
        Setting the ``max_product`` option to "True" ignores all incoming messages
        other than the strongest signal.
        Doing this results in approximate solutions, but requires significantly less
        memory and run-time than the more exact computation.
        Users should consider this option when processing power is a constraint and
        approximate solutions to |LBP| will be sufficient.

        This process of updating and message passing continues until the convergence
        criteria is met or the maximum number of supersteps is
        reached without converging.
        A node is said to converge if the total change in its distribution (the sum of
        absolute value changes in state probabilities) is less than
        the ``convergence_threshold`` parameter.
        Convergence is a local phenomenon; not all nodes will converge at the same
        time.
        It is also possible for some (most) nodes to converge and others to never
        converge.
        The algorithm requires all nodes to converge before declaring that the
        algorithm has converged overall.
        If this condition is not met, the algorithm will continue up to the maximum
        number of supersteps.

        See: http://en.wikipedia.org/wiki/Belief_propagation.


        Examples
        --------
        .. only:: html

            .. code::

            input frame (lbp.csv)
            "a"        "b"        "c"        "d"
            1,         2,         0.5,       "0.5,0.5"
            2,         3,         0.4,       "-1,-1"
            3,         1,         0.1,       "0.8,0.2"

            script

            ta.connect()
            s = [("a", ta.int32), ("b", ta.int32), ("c", ta.float32), ("d", ta.vector(2))]
            d = "lbp.csv"
            c = ta.CsvFile(d,s)
            f = ta.Frame(c)
            r = f.loopy_belief_propagation("a", "b", "c", "d", "results")
            r['frame'].inspect()
            r['report']

        .. only:: latex

            .. code::

                >>> r = f.loopy_belief_propagation(
                ... srcColName = "a",
                ... destColName  = "b",
                ... weightColName = "c",
                ... srcLabelColName = "d",
                ... resultColName = "resultLabels")
                ... r['frame'].inspect()
                ... r['report']

        The expected output is like this:

        .. only:: html

            .. code::

                {u'value': u'======Graph Statistics======\nNumber of vertices: 80000 (train: 56123, validate: 15930, test: 7947)\nNumber of edges: 318400\n\n======LBP Configuration======\nmaxSupersteps: 10\nconvergenceThreshold: 0.000000\nanchorThreshold: 0.900000\nsmoothing: 2.000000\nbidirectionalCheck: false\nignoreVertexType: false\nmaxProduct: false\npower: 0.000000\n\n======Learning Progress======\nsuperstep = 1\tavgTrainDelta = 0.594534\tavgValidateDelta = 0.542366\tavgTestDelta = 0.542801\nsuperstep = 2\tavgTrainDelta = 0.322596\tavgValidateDelta = 0.373647\tavgTestDelta = 0.371556\nsuperstep = 3\tavgTrainDelta = 0.180468\tavgValidateDelta = 0.194503\tavgTestDelta = 0.198478\nsuperstep = 4\tavgTrainDelta = 0.113280\tavgValidateDelta = 0.117436\tavgTestDelta = 0.122555\nsuperstep = 5\tavgTrainDelta = 0.076510\tavgValidateDelta = 0.074419\tavgTestDelta = 0.077451\nsuperstep = 6\tavgTrainDelta = 0.051452\tavgValidateDelta = 0.051683\tavgTestDelta = 0.052538\nsuperstep = 7\tavgTrainDelta = 0.038257\tavgValidateDelta = 0.033629\tavgTestDelta = 0.034017\nsuperstep = 8\tavgTrainDelta = 0.027924\tavgValidateDelta = 0.026722\tavgTestDelta = 0.025877\nsuperstep = 9\tavgTrainDelta = 0.022886\tavgValidateDelta = 0.019267\tavgTestDelta = 0.018190\nsuperstep = 10\tavgTrainDelta = 0.018271\tavgValidateDelta = 0.015924\tavgTestDelta = 0.015377'}

        .. only:: latex

            .. code::

                {u'value': u'======Graph Statistics======\n
                Number of vertices: 80000 (train: 56123, validate: 15930, test: 7947)\n
                Number of edges: 318400\n
                \n
                ======LBP Configuration======\n
                maxSupersteps: 10\n
                convergenceThreshold: 0.000000\n
                anchorThreshold: 0.900000\n
                smoothing: 2.000000\n
                bidirectionalCheck: false\n
                ignoreVertexType: false\n
                maxProduct: false\n
                power: 0.000000\n
                \n
                ======Learning Progress======\n
                superstep = 1\t
                    avgTrainDelta = 0.594534\t
                    avgValidateDelta = 0.542366\t
                    avgTestDelta = 0.542801\n
                superstep = 2\t
                    avgTrainDelta = 0.322596\t
                    avgValidateDelta = 0.373647\t
                    avgTestDelta = 0.371556\n
                superstep = 3\t
                    avgTrainDelta = 0.180468\t
                    avgValidateDelta = 0.194503\t
                    avgTestDelta = 0.198478\n
                superstep = 4\t
                    avgTrainDelta = 0.113280\t
                    avgValidateDelta = 0.117436\t
                    avgTestDelta = 0.122555\n
                superstep = 5\t
                    avgTrainDelta = 0.076510\t
                    avgValidateDelta = 0.074419\t
                    avgTestDelta = 0.077451\n
                superstep = 6\t
                    avgTrainDelta = 0.051452\t
                    avgValidateDelta = 0.051683\t
                    avgTestDelta = 0.052538\n
                superstep = 7\t
                    avgTrainDelta = 0.038257\t
                    avgValidateDelta = 0.033629\t
                    avgTestDelta = 0.034017\n
                superstep = 8\t
                    avgTrainDelta = 0.027924\t
                    avgValidateDelta = 0.026722\t
                    avgTestDelta = 0.025877\n
                superstep = 9\t
                    avgTrainDelta = 0.022886\t
                    avgValidateDelta = 0.019267\t
                    avgTestDelta = 0.018190\n
                superstep = 10\t
                    avgTrainDelta = 0.018271\t
                    avgValidateDelta = 0.015924\t
                    avgTestDelta = 0.015377'}



        :param src_col_name: The column name for the
            source vertex id.
        :type src_col_name: unicode
        :param dest_col_name: The column name for the
            destination vertex id.
        :type dest_col_name: unicode
        :param weight_col_name: The column name for the
            edge weight.
        :type weight_col_name: unicode
        :param src_label_col_name: The column name for the
            label properties for the source vertex.
        :type src_label_col_name: unicode
        :param result_col_name: (default=None)  The column name for the results (holding
            the post labels for the vertices).
        :type result_col_name: unicode
        :param ignore_vertex_type: (default=None)  If True, all vertex will be treated as training data.
            Default is False.
        :type ignore_vertex_type: bool
        :param max_iterations: (default=None)  The maximum number of
            supersteps that the algorithm will execute.
            The valid value range is all positive int.
            The default value is 10.
        :type max_iterations: int32
        :param convergence_threshold: (default=None)  The amount of change in cost
            function that will be tolerated at convergence.
            If the change is less than this threshold, the algorithm exits earlier
            before it reaches the maximum number of supersteps.
            The valid value range is all float and zero.
            The default value is 0.00000001f.
        :type convergence_threshold: float32
        :param anchor_threshold: (default=None)  The parameter that determines
            if a node's posterior will be updated or not.
            If a node's maximum prior value is greater than this threshold, the node will be
            treated as anchor node, whose posterior will inherit from prior without update.
            This is for the case where we have confident prior estimation for some
            nodes and don't want the algorithm to update these nodes.
            The valid value range is in [0, 1].
            Default is 1.0.
        :type anchor_threshold: float64
        :param smoothing: (default=None)  The Ising smoothing parameter.
            This parameter adjusts the relative strength of closeness encoded edge
            weights, similar to the width of Gaussian distribution.
            Larger value implies smoother decay and the edge weight becomes less important.
            Default is 2.0.
        :type smoothing: float32
        :param max_product: (default=None)  Should |LBP| use max_product or not.
            Default is False.
        :type max_product: bool
        :param power: (default=None)  Power coefficient for power edge potential.
            Default is 0.
        :type power: float32

        :returns: a 2-column frame:

                vertex: int
                    A vertex id.
                result : Vector (long)
                    label vector for the results (for the node id in column 1).
        :rtype: dict
        """
        return None


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the frame object.

        Change or retrieve frame object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_frame.name

            "csv_data"

            >>> my_frame.name = "cleaned_data"
            >>> my_frame.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def quantiles(self, column_name, quantiles):
        """
        New frame with Quantiles and their values.

        Calculate quantiles on the given column.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column *final_sale_price*:

        .. code::

            >>> my_frame.inspect()

              final_sale_price:int32
            /------------------------/
                        100
                        250
                         95
                        179
                        315
                        660
                        540
                        420
                        250
                        335

        To calculate 10th, 50th, and 100th quantile:

        .. code::

            >>> quantiles_frame = my_frame.quantiles('final_sale_price', [10, 50, 100])

        A new Frame containing the requested Quantiles and their respective values
        will be returned :

        .. code::

           >>> quantiles_frame.inspect()

             Quantiles:float64   final_sale_price_QuantileValue:float64
           /------------------------------------------------------------/
                    10.0                                     95.0
                    50.0                                    250.0
                   100.0                                    660.0




        :param column_name: The column to calculate quantiles.
        :type column_name: unicode
        :param quantiles: What is being requested.
        :type quantiles: list

        :returns: A new frame with two columns (float64): requested Quantiles and their respective values.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def rename_columns(self, names):
        """
        Rename columns

        Examples
        --------
        Start with a frame with columns *Wrong* and *Wong*.

        .. code::

            >>> print my_frame.schema
            [('Wrong', str), ('Wong', str)]

        Rename the columns to *Right* and *Wite*:

        .. code::

            >>> my_frame.rename_columns({"Wrong": "Right, "Wong": "Wite"})

        Now, what was *Wrong* is now *Right* and what was *Wong* is now *Wite*.

        .. code::

            >>> print my_frame.schema
            [('Right', str), ('Wite', str)]


        :param names: 
        :type names: None

        :returns: 
        :rtype: _Unit
        """
        return None


    @property
    @doc_stub
    def row_count(self):
        """
        Number of rows in the current frame.

        Counts all of the rows in the frame.

        Examples
        --------
        Get the number of rows:

        .. code::

            >>> my_frame.row_count

        The result given is:

        .. code::

            81734





        :returns: The number of rows in the frame
        :rtype: int
        """
        return None


    @property
    @doc_stub
    def schema(self):
        """
        Current frame column names and types.

        The schema of the current frame is a list of column names and
        associated data types.
        It is retrieved as a list of tuples.
        Each tuple has the name and data type of one of the frame's columns.

        Examples
        --------
        Given that we have an existing data frame *my_data*, create a Frame,
        then show the frame schema:

        .. code::

            >>> BF = ta.get_frame('my_data')
            >>> print BF.schema

        The result is:

        .. code::

            [("col1", str), ("col2", numpy.int32)]





        :returns: list of tuples of the form (<column name>, <data type>)
        :rtype: list
        """
        return None


    @doc_stub
    def sort(self, columns, ascending=True):
        """
        Sort the data in a frame.

        Sort a frame by column values either ascending or descending.

        Examples
        --------
        Sort a single column:

        .. code::

            >>> frame.sort('column_name')

        Sort a single column ascending:

        .. code::

            >>> frame.sort('column_name', True)

        Sort a single column descending:

        .. code::

            >>> frame.sort('column_name', False)

        Sort multiple columns:

        .. code::

            >>> frame.sort(['col1', 'col2'])

        Sort multiple columns ascending:

        .. code::

            >>> frame.sort(['col1', 'col2'], True)

        Sort multiple columns descending:

        .. code::

            >>> frame.sort(['col1', 'col2'], False)

        Sort multiple columns: 'col1' ascending and 'col2' descending:

        .. code::

            >>> frame.sort([ ('col1', True), ('col2', False) ])



        :param columns: Either a column name, a list of column names, or a list of tuples where each tuple is a name and an ascending bool value.
        :type columns: str | list of str | list of tuples
        :param ascending: (default=True)  True for ascending, False for descending.
        :type ascending: bool
        """
        return None


    @doc_stub
    def sorted_k(self, k, column_names_and_ascending, reduce_tree_depth=None):
        """
        Get a sorted subset of the data.

        Take a number of rows and return them
        sorted in either ascending or descending order.

        Sorting a subset of rows is more efficient than sorting the entire frame when
        the number of sorted rows is much less than the total number of rows in the frame.

        Notes
        -----
        The number of sorted rows should be much smaller than the number of rows
        in the original frame.

        In particular:

        #)  The number of sorted rows returned should fit in Spark driver memory.
            The maximum size of serialized results that can fit in the Spark driver is
            set by the Spark configuration parameter *spark.driver.maxResultSize*.
        #)  If you encounter a Kryo buffer overflow exception, increase the Spark
            configuration parameter *spark.kryoserializer.buffer.max.mb*.
        #)  Use Frame.sort() instead if the number of sorted rows is very large (in
            other words, it cannot fit in Spark driver memory).

        Examples
        --------
        These examples deal with the most recently-released movies in a private collection.
        Consider the movie collection already stored in the frame below:

        .. code::

            >>> big_frame.inspect(10)

              genre:str  year:int32   title:str
            /-----------------------------------/
              Drama        1957       12 Angry Men
              Crime        1946       The Big Sleep
              Western      1969       Butch Cassidy and the Sundance Kid
              Drama        1971       A Clockwork Orange
              Drama        2008       The Dark Knight
              Animation    2013       Frozen
              Drama        1972       The Godfather
              Animation    1994       The Lion King
              Animation    2010       Tangled
              Fantasy      1939       The Wonderful Wizard of Oz


        This example returns the top 3 rows sorted by a single column: 'year' descending:

        .. code::

            >>> topk_frame = big_frame.sorted_k(3, [ ('year', False) ])
            >>> topk_frame.inspect()

              genre:str  year:int32   title:str
            /-----------------------------------/
              Animation    2013       Frozen
              Animation    2010       Tangled
              Drama        2008       The Dark Knight


        This example returns the top 5 rows sorted by multiple columns: 'genre' ascending, then 'year' descending:

        .. code::

            >>> topk_frame = big_frame.sorted_k(5, [ ('genre', True), ('year', False) ])
            >>> topk_frame.inspect()

              genre:str  year:int32   title:str
            /-----------------------------------/
              Animation    2013       Frozen
              Animation    2010       Tangled
              Animation    1994       The Lion King
              Crime        1946       The Big Sleep
              Drama        2008       The Dark Knight

        This example returns the top 5 rows sorted by multiple columns: 'genre'
        ascending, then 'year' ascending.
        It also illustrates the optional tuning parameter for reduce-tree depth
        (which does not affect the final result).

        .. code::

            >>> topk_frame = big_frame.sorted_k(5, [ ('genre', True), ('year', True) ], reduce_tree_depth=1)
            >>> topk_frame.inspect()

              genre:str  year:int32   title:str
            /-----------------------------------/
              Animation    1994       The Lion King
              Animation    2010       Tangled
              Animation    2013       Frozen
              Crime        1946       The Big Sleep
              Drama        1972       The Godfather



        :param k: Number of sorted records to return.
        :type k: int32
        :param column_names_and_ascending: Column names to sort by, and true to sort column by ascending order,
            or false for descending order.
        :type column_names_and_ascending: list
        :param reduce_tree_depth: (default=None)  Advanced tuning parameter which determines the depth of the
            reduce-tree (uses Spark's treeReduce() for scalability.)
            Default is 2.
        :type reduce_tree_depth: int32

        :returns: A new frame with a subset of sorted rows from the original frame.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @property
    @doc_stub
    def status(self):
        """
        Current frame life cycle status.

        One of three statuses: Active, Dropped, Finalized
           Active:    Entity is available for use
           Dropped:   Entity has been dropped by user or by garbage collection which found it stale
           Finalized: Entity's data has been deleted

        Examples
        --------
        Given that we have an existing data frame *my_data*, create a Frame,
        then show the frame schema:

        .. code::

            >>> BF = ta.get_frame('my_data')
            >>> print BF.status

        The result is:

        .. code::

            u'Active'




        :returns: Status of the frame
        :rtype: str
        """
        return None


    @doc_stub
    def take(self, n, offset=0, columns=None):
        """
        Get data subset.

        Take a subset of the currently active Frame.

        Notes
        -----
        The data is considered 'unstructured', therefore taking a certain
        number of rows, the rows obtained may be different every time the
        command is executed, even if the parameters do not change.

        Examples
        --------
        Frame *my_frame* accesses a frame with millions of rows of data.
        Get a sample of 5000 rows:

        .. code::

            >>> my_data_list = my_frame.take( 5000 )

        We now have a list of data from the original frame.

        .. code::

            >>> print my_data_list

            [[ 1, "text", 3.1415962 ]
             [ 2, "bob", 25.0 ]
             [ 3, "weave", .001 ]
             ...]

        If we use the method with an offset like:

        .. code::

            >>> my_data_list = my_frame.take( 5000, 1000 )

        We end up with a new list, but this time it has a copy of the data from
        rows 1001 to 5000 of the original frame.



        :param n: The number of rows to copy to the client from the frame.
        :type n: int
        :param offset: (default=0)  The number of rows to skip before starting to copy
        :type offset: int
        :param columns: (default=None)  If not None, only the given columns' data will be provided.  By default, all columns are included
        :type columns: str | iterable of str

        :returns: A list of lists, where each contained list is the data for one row.
        :rtype: list
        """
        return None


    @doc_stub
    def tally(self, sample_col, count_val):
        """
        Count number of times a value is seen.

        A cumulative count is computed by sequentially stepping through the rows,
        observing the column values and keeping track of the number of times the specified
        *count_value* has been seen.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column *obs*:

        .. code::

            >>> my_frame.inspect()

              obs:int32
            /-----------/
                0
                1
                2
                0
                1
                2

        The cumulative count for column *obs* using *count_value = 1* is obtained by:

        .. code::

            >>> my_frame.tally('obs', '1')

        The Frame *my_frame* accesses a frame which now contains two columns *obs*
        and *obsCumulativeCount*.
        Column *obs* still has the same data and *obsCumulativeCount* contains the
        cumulative counts:

        .. code::

            >>> my_frame.inspect()

              obs:int32        obs_tally:int32
            /----------------------------------/
                 0                      0
                 1                      1
                 2                      1
                 0                      1
                 1                      2
                 2                      2



        :param sample_col: The name of the column from which to compute the cumulative count.
        :type sample_col: unicode
        :param count_val: The column value to be used for the counts.
        :type count_val: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def tally_percent(self, sample_col, count_val):
        """
        Compute a cumulative percent count.

        A cumulative percent count is computed by sequentially stepping through
        the rows, observing the column values and keeping track of the percentage of the
        total number of times the specified *count_value* has been seen up to
        the current value.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column named *obs*:

        .. code::

            >>> my_frame.inspect()

              obs:int32
            /-----------/
                 0
                 1
                 2
                 0
                 1
                 2

        The cumulative percent count for column *obs* is obtained by:

        .. code::

            >>> my_frame.tally_percent('obs', 1)

        The Frame *my_frame* accesses the original frame that now contains two
        columns, *obs* that contains the original column values, and
        *obsCumulativePercentCount* that contains the cumulative percent count:

        .. code::

            >>> my_frame.inspect()

              obs:int32    obs_tally_percent:float64
            /----------------------------------------/
                 0                         0.0
                 1                         0.5
                 2                         0.5
                 0                         0.5
                 1                         1.0
                 2                         1.0



        :param sample_col: The name of the column from which to compute
            the cumulative sum.
        :type sample_col: unicode
        :param count_val: The column value to be used for the counts.
        :type count_val: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def top_k(self, column_name, k, weights_column=None):
        """
        Most or least frequent column values.

        Calculate the top (or bottom) K distinct values by count of a column.
        The column can be weighted.
        All data elements of weight <= 0 are excluded from the calculation, as are
        all data elements whose weight is NaN or infinite.
        If there are no data elements of finite weight > 0, then topK is empty.

        Examples
        --------
        For this example, we calculate the top 5 movie genres in a data frame:

        .. code::

            >>> top5 = frame.top_k('genre', 5)
            >>> top5.inspect()

              genre:str   count:float64
            /---------------------------/
              Drama        738278
              Comedy       671398
              Short        455728
              Documentary  323150
              Talk-Show    265180

        This example calculates the top 3 movies weighted by rating:

        .. code::

            >>> top3 = frame.top_k('genre', 3, weights_column='rating')
            >>> top3.inspect()

              movie:str      count:float64
            /------------------------------/
              The Godfather         7689.0
              Shawshank Redemption  6358.0
              The Dark Knight       5426.0

        This example calculates the bottom 3 movie genres in a data frame:

        .. code::

            >>> bottom3 = frame.top_k('genre', -3)
            >>> bottom3.inspect()

              genre:str   count:float64
            /---------------------------/
              Musical       26
              War           47
              Film-Noir    595




        :param column_name: The column whose top (or bottom) K distinct values are
            to be calculated.
        :type column_name: unicode
        :param k: Number of entries to return (If k is negative, return bottom k).
        :type k: int32
        :param weights_column: (default=None)  The column that provides weights (frequencies) for the topK calculation.
            Must contain numerical data.
            Default is 1 for all items.
        :type weights_column: unicode

        :returns: An object with access to the frame of data.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def unflatten_column(self, composite_key_column_names, delimiter=None):
        """
        Compacts data from multiple rows based on cell data.

        Groups together cells in all columns (less the composite key) using "," as string delimiter.
        The original rows are deleted.
        The grouping takes place based on a composite key created from cell values.
        The column datatypes are changed to string.

        Examples
        --------
        Given a data file::

            user1 1/1/2015 1 70
            user1 1/1/2015 2 60
            user2 1/1/2015 1 65

        The commands to bring the data into a frame, where it can be worked on:

        .. only:: html

            .. code::

                >>> my_csv = ta.CsvFile("original_data.csv", schema=[('a', str), ('b', str),('c', int32) ,('d', int32]))
                >>> my_frame = ta.Frame(source=my_csv)

        .. only:: latex

            .. code::

                >>> my_csv = ta.CsvFile("unflatten_column.csv", schema=[('a', str), ('b', str),('c', int32) ,('d', int32)])
                >>> my_frame = ta.Frame(source=my_csv)

        Looking at it:

        .. code::

            >>> my_frame.inspect()

              a:str        b:str       c:int32       d:int32
            /------------------------------------------------/
               user1       1/1/12015   1             70
               user1       1/1/12015   2             60
               user2       1/1/2015    1             65

        Unflatten the data using columns a & b:

        .. code::

            >>> my_frame.unflatten_column({'a','b'})

        Check again:

        .. code::

            >>> my_frame.inspect()

              a:str        b:str       c:str     d:str
            /-------------------------------------------/
               user1       1/1/12015   1,2       70,60
               user2       1/1/2015    1         65



        :param composite_key_column_names: Name of the column(s) to be used as keys
            for unflattening.
        :type composite_key_column_names: list
        :param delimiter: (default=None)  Separator for the data in the result columns.
            Default is comma (,).
        :type delimiter: unicode

        :returns: 
        :rtype: _Unit
        """
        return None



@doc_stub
class _DocStubsGraph(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Initialize the graph.

        Examples
        --------
        This example uses a single source data frame and creates a graph of 'user'
        and 'movie' vertices connected by 'rating' edges.

        The first step is to bring in some data to create a frame as the source
        for a graph:

        .. only:: html

            .. code::

                >>> my_schema = [('user_id', ta.int32), ('user_name', str), ('movie_id', ta.int32), ('movie_title', str), ('rating', str)]
                >>> my_csv = ta.CsvFile("/movie.csv", my_schema)
                >>> my_frame = ta.Frame(my_csv)

        .. only:: latex

            .. code::

                >>> my_schema = [('user_id', ta.int32), ('user_name', str),
                ... ('movie_id', ta.int32), ('movie_title', str), ('rating', str)]
                >>> my_csv = ta.CsvFile("/movie.csv", my_schema)
                >>> my_frame = ta.Frame(my_csv)

        Now, make an empty graph:

        .. code::

            >>> my_graph = ta.Graph()

        Then, define the types of vertices and edges this graph will be made of:

        .. code::

            >>> my_graph.define_vertex_type('users')
            >>> my_graph.define_vertex_type('movies')
            >>> my_graph.define_edge_type('ratings','users','movies',directed=True)

        And finally, add the data to the graph:

        .. only:: latex

            .. code::

                >>> my_graph.vertices['users'].add_vertices(my_frame, 'user_id', ['user_name'])
                >>> my_graph.vertices['movies'].add_vertices(my_frame, 'movie_id', ['movie_title'])
                >>> my_graph.edges['ratings'].add_edges(my_frame, 'user_id', 'movie_id', ['rating']

        .. only:: html

            .. code::

                >>> my_graph.vertices['users'].add_vertices(my_frame, 'user_id', ['user_name'])
                >>> my_graph.vertices['movies'].add_vertices(my_frame, 'movie_id', ['movie_title'])
                >>> my_graph.edges['ratings'].add_edges(my_frame, 'user_id',
                ... 'movie_id', ['rating'])

        |

        Adding additional data to the graph from another frame (my_frame2),
        is simply adding vertices (and edges) in row formation.

        .. code::

            >>> my_graph.vertices['users'].add_vertices(my_frame2, 'user_id', ['user_name'])

        Getting basic information about the graph:

        .. code::

            >>> my_graph.vertex_count
            >>> my_graph.edge_count
            >>> my_graph.vertices['users'].inspect(20)

        |

        This example uses multiple source data frames and creates a graph of
        'user' and 'movie' vertices connected by 'rating' edges.

        Create a frame as the source for a graph:

        .. code::

            >>> user_schema = [('user_id', ta.int32), ('user_name', str), ('age', ta.int32)]))
            >>> user_frame = ta.Frame(ta.CsvFile("/users.csv", userSchema)

            >>> movie_schema = [('movie_id', ta.int32), ('movie_title', str), ('year', str)]))
            >>> movie_frame = ta.Frame(ta.CsvFile("/movie.csv", movie_schema)

            >>> ratings_schema = [('ser_id', ta.int32), ('movie_id', ta.int32), ('rating', str)]))
            >>> ratings_frame = ta.Frame(ta.CsvFile("/ratings.csv", ratings_schema)

        Create a graph:

        .. code::

            >>> my_graph = ta.Graph()

        Define the types of vertices and edges this graph will be made of:

        .. code::

            >>> my_graph.define_vertex_type('users')
            >>> my_graph.define_vertex_type('movies')
            >>> my_graph.define_edge_type('ratings','users','movies',directed=True)

        Add data to the graph:

        .. only:: html

            .. code::

                >>> my_graph.vertices['users'].add_vertices(user_frame, 'user_id', ['user_name', 'age'])
                >>> my_graph.vertices['movies'].add_vertices(movie_frame, 'movie_id') # all columns automatically added as properties
                >>> my_graph.edges['ratings'].add_edges(ratings_frame, 'user_id', 'movie_id', ['rating'])

        .. only:: latex

            .. code::

                >>> my_graph.vertices['users'].add_vertices(user_frame, 'user_id',
                ... ['user_name', 'age'])
                >>> my_graph.vertices['movies'].add_vertices(movie_frame, 'movie_id')
                ... # all columns automatically added as properties
                >>> my_graph.edges['ratings'].add_edges(ratings_frame, 'user_id',
                ... 'movie_id', ['rating'])

        |

        This example shows edges between vertices of the same type.
        Specifically, "employees work under other employees".

        Create a frame to use as the source for the graph data:

        .. only:: html

            .. code::

                >>> employees_frame = ta.Frame(ta.CsvFile("employees.csv", schema = [('Employee', str), ('Manager', str), ('Title', str), ('Years', ta.int64)], skip_header_lines=1), 'employees_frame')

        .. only:: latex

            .. code::

                >>> employees_frame = ta.Frame(ta.CsvFile("employees.csv",
                ... schema = [('Employee', str), ('Manager', str),
                ... ('Title', str), ('Years', ta.int64)], skip_header_lines=1),
                ... 'employees_frame')

        Define a graph:

        .. code::

            >>> my_graph = ta.Graph()
            >>> my_graph.define_vertex_type('Employee')
            >>> my_graph.define_edge_type('worksunder', 'Employee', 'Employee', directed=True)

        Add data:

        .. only:: html

            .. code::

                >>> my_graph.vertices['Employee'].add_vertices(employees_frame, 'Employee', ['Title'])
                >>> my_graph.edges['worksunder'].add_edges(employees_frame, 'Employee', 'Manager', ['Years'], create_missing_vertices = True)

        .. only:: latex

            .. code::

                >>> my_graph.vertices['Employee'].add_vertices(employees_frame,
                ... 'Employee', ['Title'])
                >>> my_graph.edges['worksunder'].add_edges(employees_frame,
                ... 'Employee', 'Manager', ['Years'],
                ... create_missing_vertices = True)

        Inspect the graph:

        .. code::

            >>> my_graph.vertex_count
            >>> my_graph.edge_count
            >>> my_graph.vertices['Employee'].inspect(20)
            >>> my_graph.edges['worksunder'].inspect(20)

            

        :param name: (default=None)  Name for the new graph.
            Default is None.
        :type name: str
        """
        raise DocStubCalledError("graph:/__init__")


    @doc_stub
    def annotate_degrees(self, output_property_name, degree_option=None, input_edge_labels=None):
        """
        Make new graph with degrees.

        Creates a new graph which is the same as the input graph, with the addition
        that every vertex of the graph has its degree stored in a user-specified property.

        **Degree Calculation**

        A fundamental quantity in graph analysis is the degree of a vertex:
        The degree of a vertex is the number of edges adjacent to it.

        For a directed edge relation, a vertex has both an out-degree (the number of
        edges leaving the vertex) and an in-degree (the number of edges entering the
        vertex).

        The toolkit provides this routine for calculating the degrees of vertices.
        This calculation could be performed with a Gremlin query on smaller datasets
        because Gremlin queries cannot be executed on a distributed scale.
        The |PACKAGE| routine ``annotate_degrees`` can be executed at distributed scale.

        In the presence of edge weights, vertices can have weighted degrees: The
        weighted degree of a vertex is the sum of weights of edges adjacent to it.
        Analogously, the weighted in-degree of a vertex is the sum of the weights of
        the edges entering it, and the weighted out-degree is the sum
        of the weights of the edges leaving the vertex.

        The toolkit provides :ref:`annotate_weighted_degrees <python_api/graphs/graph-/annotate_weighted_degrees>`
        for the distributed calculation of weighted vertex degrees.

        Examples
        --------
        Given a graph:

        .. code::

            >>> g.query.gremlin('g.V [ 0 .. 1]')

            Out[12]:
               {u'results': [{u'_id': 19456,
                u'_label': u'vertex',
                u'_type': u'vertex',
                u'_vid': 545413,
                u'source': 6961},
               {u'_id': 19968,
                u'_label': u'vertex',
                u'_type': u'vertex',
                u'_vid': 511316,
                u'source': 31599}],
                u'run_time_seconds': 1.822}

            >>> h = g.annotate_degrees('degree')



        :param output_property_name: The name of the new property.
            The degree is stored in this property.
        :type output_property_name: unicode
        :param degree_option: (default=None)  Indicator for the definition of degree to be used for the
            calculation.
            Permitted values:

            *   "out" (default value) : Degree is calculated as the out-degree.
            *   "in" : Degree is calculated as the in-degree.
            *   "undirected" : Degree is calculated as the undirected degree.
                (Assumes that the edges are all undirected.)
               
            Any prefix of the strings "out", "in", "undirected" will select the
            corresponding option.
        :type degree_option: unicode
        :param input_edge_labels: (default=None)  If this list is provided, only edges whose labels are
            included in the given set will be considered in the degree calculation.
            In the default situation (when no list is provided), all edges will be used
            in the degree calculation, regardless of label.
        :type input_edge_labels: list

        :returns: Dictionary containing the vertex type as the key and the corresponding
            vertex's frame with a column storing the annotated degree for the vertex
            in a user specified property.
            Call dictionary_name['label'] to get the handle to frame whose vertex type
            is label.
        :rtype: dict
        """
        return None


    @doc_stub
    def annotate_weighted_degrees(self, output_property_name, degree_option=None, input_edge_labels=None, edge_weight_property=None, edge_weight_default=None):
        """
        Calculates the weighted degree of each vertex with respect to an (optional) set of labels.

        Pulls graph from underlying store, calculates weighted degrees and writes them into the property
        specified, and then writes the output graph to the underlying store.

        **Degree Calculation**

        A fundamental quantity in graph analysis is the degree of a vertex:
        The degree of a vertex is the number of edges adjacent to it.

        For a directed edge relation, a vertex has both an out-degree (the number of
        edges leaving the vertex) and an in-degree (the number of edges entering the
        vertex).

        The toolkit provides a routine :ref:`annotate_degrees
        <python_api/graphs/graph-/annotate_weighted_degrees>`
        for calculating the degrees of vertices.
        This calculation could be performed with a Gremlin query on smaller datasets
        because Gremlin queries cannot be executed on a distributed scale.
        The |PACKAGE| routine ``annotate_degrees`` can be executed at distributed scale.

        In the presence of edge weights, vertices can have weighted degrees: The
        weighted degree of a vertex is the sum of weights of edges adjacent to it.
        Analogously, the weighted in-degree of a vertex is the sum of the weights of
        the edges entering it, and the weighted out-degree is the sum
        of the weights of the edges leaving the vertex.

        The toolkit provides this routine for the distributed calculation of weighted
        vertex degrees.

        Examples
        --------
        Given a directed graph with three nodes and two edges like this:

        .. only:: html

            .. code::

                >>> g.query.gremlin('g.V')
                Out[23]: {u'results': [{u'_id': 28304, u'_label': u'vertex', u'_type': u'vertex', u'_vid': 4, u'source': 2}, {u'_id': 21152, u'_label': u'vertex', u'_type': u'vertex', u'_vid': 1, u'source': 1}, {u'_id': 28064, u'_label': u'vertex', u'_type': u'vertex', u'_vid': 3, u'source': 3}], u'run_time_seconds': 1.245}

                >>> g.query.gremlin('g.E')
                Out[24]: {u'results': [{u'_eid': 3, u'_id': u'34k-gbk-bth-lnk', u'_inV': 28064, u'_label': u'edge', u'_outV': 21152, u'_type': u'edge', u'weight': 0.01}, {u'_eid': 4, u'_id': u'1xw-gbk-bth-lu8', u'_inV': 28304, u'_label': u'edge', u'_outV': 21152, u'_type': u'edge', u'weight': 0.1}], u'run_time_seconds': 1.359}

                >>> h = g.annotate_weighted_degrees('weight',  edge_weight_property = 'weight')

        .. only:: latex

            .. code::

                >>> g.query.gremlin('g.V')
                Out[23]:
                {u'results': [{u'_id': 28304,
                 u'_label': u'vertex',
                 u'_type': u'vertex',
                 u'_vid': 4,
                 u'source': 2},
                {u'_id': 21152,
                 u'_label': u'vertex',
                 u'_type': u'vertex',
                 u'_vid': 1,
                 u'source': 1},
                {u'_id': 28064,
                 u'_label': u'vertex',
                 u'_type': u'vertex',
                 u'_vid': 3,
                 u'source': 3}],
                 u'run_time_seconds': 1.245}

                >>> g.query.gremlin('g.E')
                Out[24]:
                {u'results': [{u'_eid': 3,
                 u'_id': u'34k-gbk-bth-lnk',
                 u'_inV': 28064,
                 u'_label': u'edge',
                 u'_outV': 21152,
                 u'_type': u'edge',
                 u'weight': 0.01},
                {u'_eid': 4,
                 u'_id': u'1xw-gbk-bth-lu8',
                 u'_inV': 28304,
                 u'_label': u'edge',
                 u'_outV': 21152,
                 u'_type': u'edge',
                 u'weight': 0.1}],
                 u'run_time_seconds': 1.359}

                >>> h = g.annotate_weighted_degrees(
                ...        'weight',
                ...        edge_weight_property = 'weight')



        :param output_property_name: property name of where to store output
        :type output_property_name: unicode
        :param degree_option: (default=None)  choose from 'out', 'in', 'undirected'
        :type degree_option: unicode
        :param input_edge_labels: (default=None)  labels of edge types that should be included
        :type input_edge_labels: list
        :param edge_weight_property: (default=None)  property name of edge weight, if not provided all edges are weighted equally
        :type edge_weight_property: unicode
        :param edge_weight_default: (default=None)  default edge weight
        :type edge_weight_default: float64

        :returns: 
        :rtype: dict
        """
        return None


    @doc_stub
    def clustering_coefficient(self, output_property_name=None, input_edge_labels=None):
        """
        Coefficient of graph with respect to labels.

        Calculates the clustering coefficient of the graph with respect to an (optional) set of labels.

        Pulls graph from underlying store, calculates degrees and writes them into the property specified,
        and then writes the output graph to the underlying store.

        .. warning::

            THIS FUNCTION IS FOR UNDIRECTED GRAPHS.
            If it is called on a directed graph, its output is NOT guaranteed to calculate
            the local directed clustering coefficients.

        |
        **Clustering Coefficients**

        The clustering coefficient of a graph provides a measure of how tightly
        clustered an undirected graph is.
        Informally, if the edge relation denotes "friendship", the clustering
        coefficient of the graph is the probability that two people are friends given
        that they share a common friend.

        More formally:

        .. math::

            cc(G)  = \frac{ \| \{ (u,v,w) \in V^3: \ \{u,v\}, \{u, w\}, \{v,w \} \in \
            E \} \| }{\| \{ (u,v,w) \in V^3: \ \{u,v\}, \{u, w\} \in E \} \|}


        Analogously, the clustering coefficient of a vertex provides a measure of how
        tightly clustered that vertex's neighborhood is.
        Informally, if the edge relation denotes "friendship", the clustering
        coefficient at a vertex :math:`v` is the probability that two acquaintances of
        :math:`v` are themselves friends.

        More formally:

        .. math::

            cc(v)  = \frac{ \| \{ (u,v,w) \in V^3: \ \{u,v\}, \{u, w\}, \{v,w \} \in \
            E \} \| }{\| \{ (u,v,w) \in V^3: \ \{v, u \}, \{v, w\} \in E \} \|}


        The toolkit provides the function clustering_coefficient which computes both
        local and global clustering coefficients for a given undirected graph.

        For more details on the mathematics and applications of clustering
        coefficients, see http://en.wikipedia.org/wiki/Clustering_coefficient.



        Examples
        --------
        .. code::

            >>> results = g.clustering_coefficient('ccgraph', 'local_clustering_coefficient')

            >>> results
                Out[8]:
                ClusteringCoefficient:
                global_clustering_coefficient: 0.0853107962708,
                frame: Frame

            >>> results.frame.inspect()


        :param output_property_name: (default=None)  The name of the new property to which each
            vertex's local clustering coefficient will be written.
            If this option is not specified, no output frame will be produced and only
            the global clustering coefficient will be returned.
        :type output_property_name: unicode
        :param input_edge_labels: (default=None)  If this list is provided,
            only edges whose labels are included in the given
            set will be considered in the clustering coefficient calculation.
            In the default situation (when no list is provided), all edges will be used
            in the calculation, regardless of label.
            It is required that all edges that enter into the clustering coefficient
            analysis be undirected.
        :type input_edge_labels: list

        :returns: Dictionary of the global clustering coefficient of the graph or,
            if local clustering coefficients are requested, a reference to the frame with local
            clustering coefficients stored at properties at each vertex.
        :rtype: dict
        """
        return None


    @doc_stub
    def copy(self, name=None):
        """
        Make a copy of the current graph.

        Examples
        --------
        For this example, graph object *my_graph* accesses a graph:

        .. code::

            >>> copied_graph = my_graph.copy('my_graph2')


        :param name: (default=None)  The name for the copy of the graph.
            Default is None.
        :type name: unicode

        :returns: A copy of the original graph.
        :rtype: dict
        """
        return None


    @doc_stub
    def define_edge_type(self, label, src_vertex_label, dest_vertex_label, directed=False):
        """
        Define an edge type.

        Examples
        --------
        .. code::

            >>> graph = ta.Graph()
            >>> graph.define_vertex_type('users')
            >>> graph.define_vertex_type('movie')
            >>> graph.define_edge_type('ratings', 'users', 'movie', directed=True)


        :param label: Label of the edge type.
        :type label: unicode
        :param src_vertex_label: The source "type" of vertices this edge
            connects.
        :type src_vertex_label: unicode
        :param dest_vertex_label: The destination "type" of vertices this
            edge connects.
        :type dest_vertex_label: unicode
        :param directed: (default=False)  True if edges are directed,
            false if they are undirected.
        :type directed: bool

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def define_vertex_type(self, label):
        """
        Define a vertex type by label.

        Examples
        --------
        .. code::

            >>> graph = ta.Graph()
            >>> graph.define_vertex_type('users')



        :param label: Label of the vertex type.
        :type label: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @property
    @doc_stub
    def edge_count(self):
        """
        Get the total number of edges in the graph.

        Returns
        -------
        int32
            The number of edges in the graph.


        Examples
        --------
        .. code::

            >>> my_graph.edge_count

        The result given is:

        .. code::

            1194





        :returns: Total number of edges in the graph
        :rtype: int
        """
        return None


    @property
    @doc_stub
    def edges(self):
        """
        Edge frame collection

        Examples
        --------
        Inspect edges with the supplied label:

        .. code::

            >>> my_graph.edges['label'].inspect()




        """
        return None


    @doc_stub
    def export_to_titan(self, new_graph_name=None):
        """
        Convert current graph to TitanGraph.

        Convert this Graph into a TitanGraph object.
        This will be a new graph backed by Titan with all of the data found in this
        graph.

        Examples
        --------
        .. code::

            >>> graph = ta.get_graph("my_graph")
            >>> titan_graph = graph.export_to_titan("titan_graph")



        :param new_graph_name: (default=None)  The name of the new graph.
            Default is None.
        :type new_graph_name: unicode

        :returns: A new TitanGraph.
        :rtype: dict
        """
        return None


    @doc_stub
    def graphx_connected_components(self, output_property):
        """
        Implements the connected components computation on a graph by invoking graphx api.

        Pulls graph from underlying store, sends it off to the ConnectedComponentGraphXDefault,
        and then writes the output graph back to the underlying store.

        |
        **Connected Components (CC)**

        Connected components are disjoint subgraphs in which all vertices are
        connected to all other vertices in the same component via paths, but not
        connected via paths to vertices in any other component.
        The connected components algorithm uses message passing along a specified edge
        type to find all of the connected components of a graph and label each edge
        with the identity of the component to which it belongs.
        The algorithm is specific to an edge type, hence in graphs with several
        different types of edges, there may be multiple, overlapping sets of connected
        components.

        The algorithm works by assigning each vertex a unique numerical index and
        passing messages between neighbors.
        Vertices pass their indices back and forth with their neighbors and update
        their own index as the minimum of their current index and all other indices
        received.
        This algorithm continues until there is no change in any of the vertex
        indices.
        At the end of the algorithm, the unique levels of the indices denote the
        distinct connected components.
        The complexity of the algorithm is proportional to the diameter of the graph.


        Examples
        --------
        .. code::

            >>> f= g.graphx_connected_components(output_property = "ccId")

        The expected output is like this:

        .. code::

            {u'movie': Frame "None"
             row_count = 597
             schema =
               _vid:int64
               _label:unicode
               movie:int32
               Con_Com:int64, u'user': Frame "None"
             row_count = 597
             schema =
               _vid:int64
               _label:unicode
               vertexType:unicode
               user:int32
               Con_Com:int64}

        To query:

        .. code::

            >>> movie_frame = f['movie']
            >>> user_frame = f['user']



        :param output_property: The name of the column containing the connected component value.
        :type output_property: unicode

        :returns: Dictionary containing the vertex type as the key and the corresponding
              vertex's frame with a connected component column.
              Call dictionary_name['label'] to get the handle to frame whose vertex type is label.
        :rtype: dict
        """
        return None


    @doc_stub
    def graphx_pagerank(self, output_property, input_edge_labels=None, max_iterations=None, reset_probability=None, convergence_tolerance=None):
        """
        Determine which vertices are the most important.

        Pulls graph from underlying store, sends it off to the
        PageRankRunner, and then writes the output graph back to the underlying store.

        This method (currently) only supports Titan for graph storage.

        ** Experimental Feature **

        **Basics and Background**

        *PageRank* is a method for determining which vertices in a directed graph are
        the most central or important.
        *PageRank* gives each vertex a score which can be interpreted as the
        probability that a person randomly walking along the edges of the graph will
        visit that vertex.

        The calculation of *PageRank* is based on the supposition that if a vertex has
        many vertices pointing to it, then it is "important",
        and that a vertex grows in importance as more important vertices point to it.
        The calculation is based only on the network structure of the graph and makes
        no use of any side data, properties, user-provided scores or similar
        non-topological information.

        *PageRank* was most famously used as the core of the Google search engine for
        many years, but as a general measure of centrality in a graph, it has
        other uses to other problems, such as recommendation systems and
        analyzing predator-prey food webs to predict extinctions.

        **Background references**

        *   Basic description and principles: `Wikipedia\: PageRank`_
        *   Applications to food web analysis: `Stanford\: Applications of PageRank`_
        *   Applications to recommendation systems: `PLoS\: Computational Biology`_

        **Mathematical Details of PageRank Implementation**

        The |PACKAGE| implementation of *PageRank* satisfies the following equation
        at each vertex :math:`v` of the graph:

        .. math::

            PR(v) = \frac {\rho}{n} + \rho \left( \sum_{u\in InSet(v)} \
            \frac {PR(u)}{L(u)} \right)

        Where:
            |   :math:`v` |EM| a vertex
            |   :math:`L(v)` |EM| outbound degree of the vertex v
            |   :math:`PR(v)` |EM| *PageRank* score of the vertex v
            |   :math:`InSet(v)` |EM| set of vertices pointing to the vertex v
            |   :math:`n` |EM| total number of vertices in the graph
            |   :math:`\rho` |EM| user specified damping factor (also known as reset
                probability)

        Termination is guaranteed by two mechanisms.

        *   The user can specify a convergence threshold so that the algorithm will
            terminate when, at every vertex, the difference between successive
            approximations to the *PageRank* score falls below the convergence
            threshold.
        *   The user can specify a maximum number of iterations after which the
            algorithm will terminate.

        .. _Wikipedia\: PageRank: http://en.wikipedia.org/wiki/PageRank
        .. _Stanford\: Applications of PageRank: http://web.stanford.edu/class/msande233/handouts/lecture8.pdf
        .. _PLoS\: Computational Biology:
            http://www.ploscompbiol.org/article/fetchObject.action?uri=info%3Adoi%2F10.1371%2Fjournal.pcbi.1000494&representation=PDF

        Examples
        --------
        .. only:: html

            .. code::

                >>> graph = ta.Graph()
                >>> graph.define_vertex_type("node")
                >>> graph.vertices["node"].add_vertices(frame,"follows")
                >>> graph.vertices["node"].add_vertices(frame,"followed")
                >>> graph.define_edge_type("e1","node","node",directed=True)
                >>> graph.edges["e1"].add_edges(frame,"follows","followed")
                >>> result = graph.graphx_pagerank(output_property="PageRank",max_iterations=2,convergence_tolerance=0.001)
                >>> vertex_dict = result['vertex_dictionary']
                >>> edge_dict = result['edge_dictionary']

        .. only:: latex

            .. code::

                >>> graph = ta.Graph()
                >>> graph.define_vertex_type("node")
                >>> graph.vertices["node"].add_vertices(frame,"follows")
                >>> graph.vertices["node"].add_vertices(frame,"followed")
                >>> graph.define_edge_type("e1","node","node",directed=True)
                >>> graph.edges["e1"].add_edges(frame,"follows","followed")
                >>> result = graph.graphx_pagerank(output_property="PageRank",max_iterations=2,convergence_tolerance=0.001)
                >>> vertex_dict = result['vertex_dictionary']
                >>> edge_dict = result['edge_dictionary']


        :param output_property: Name of the property to which PageRank
            value will be stored on vertex and edge.
        :type output_property: unicode
        :param input_edge_labels: (default=None)  List of edge labels to consider for PageRank computation.
            Default is all edges are considered.
        :type input_edge_labels: list
        :param max_iterations: (default=None)  The maximum number of iterations that will be invoked.
            The valid range is all positive int.
            Invalid value will terminate with vertex page rank set to reset_probability.
            Default is 20.
        :type max_iterations: int32
        :param reset_probability: (default=None)  The probability that the random walk of a page is reset.
            Default is 0.15.
        :type reset_probability: float64
        :param convergence_tolerance: (default=None)  The amount of change in cost function that will be tolerated at
            convergence.
            If this parameter is specified, max_iterations is not considered as a stopping condition.
            If the change is less than this threshold, the algorithm exits earlier.
            The valid value range is all float and zero.
            Default is 0.001.
        :type convergence_tolerance: float64

        :returns: dict((vertex_dictionary, (label, Frame)), (edge_dictionary,(label,Frame))).

            Dictionary containing dictionaries of labeled vertices and labeled edges.

            For the *vertex_dictionary* the vertex type is the key and the corresponding
            vertex's frame with a new column storing the page rank value for the vertex.
            Call vertex_dictionary['label'] to get the handle to frame whose vertex
            type is label.

            For the *edge_dictionary* the edge type is the key and the corresponding
            edge's frame with a new column storing the page rank value for the edge.
            Call edge_dictionary['label'] to get the handle to frame whose edge type
            is label.
        :rtype: dict
        """
        return None


    @doc_stub
    def graphx_triangle_count(self, output_property, input_edge_labels=None):
        """
        Number of triangles among vertices of current graph.

        ** Experimental Feature **

        Counts the number of triangles among vertices in an undirected graph.
        If an edge is marked bidirectional, the implementation opts for canonical
        orientation of edges hence counting it only once (similar to an
        undirected graph).

        Examples
        --------
        .. only:: html
           
            .. code::

                >>> f = g.graphx_triangle_count(output_property = "triangle_count", output_graph_name = "tc_graph")

        .. only:: latex
           
            .. code::

                >>> f = g.graphx_triangle_count(output_property = "triangle_count",
                ... output_graph_name = "tc_graph")

        The expected output is like this:

        .. code::

            {u'label1': Frame "None"
            row_count = 110
            schema =
              _vid:int64
              _label:unicode
              max_k:int64
              cc:int64
              TC:int32
              node:unicode,
            u'label2': Frame "None"
            row_count = 430
            schema =
              _vid:int64
              _label:unicode
              max_k:int64
              cc:int64
              TC:int32
              node:unicode}


        To query:

        .. only:: html

            .. code::

                >>> frame_for_label1 = f['label1']
                >>> frame_for_label1.inspect(10)
                
                  _vid:int64   _label:unicode   max_k:int64   cc:int64   TC:int32   node:unicode
                /--------------------------------------------------------------------------------/
                      106656   label1                     2         12          0   node158
                      129504   label1                     3         23          1   node2116
                       86640   label1                     7         17         15   node183
                       20424   label1                     7         47         15   node4248
                      164184   label1                     2         72          0   node7388
                       23232   label1                     9         39         28   node3210
                       93840   label1                     3         83          1   node8446
                      114480   label1                     8         58         21   node5311
                       48480   label1                    10         30         36   node2166
                       31152   label1                     6         96         10   node9516


        .. only:: latex

            .. code::

                >>> frame_for_label1 = f['label1']
                >>> frame_for_label1.inspect(10)

                   _vid   _label   max_k  cc     TC     node
                   int64  unicode  int64  int64  int32  unicode
                /------------------------------------------------\
                  106656  label1       2     12      0  node158
                  129504  label1       3     23      1  node2116
                   86640  label1       7     17     15  node183
                   20424  label1       7     47     15  node4248
                  164184  label1       2     72      0  node7388
                   23232  label1       9     39     28  node3210
                   93840  label1       3     83      1  node8446
                  114480  label1       8     58     21  node5311
                   48480  label1      10     30     36  node2166
                   31152  label1       6     96     10  node9516




        :param output_property: The name of output property to be
            added to vertex/edge upon completion.
        :type output_property: unicode
        :param input_edge_labels: (default=None)  The name of edge labels to be considered for triangle count.
            Default is all edges are considered.
        :type input_edge_labels: list

        :returns: dict(label, Frame).

            Dictionary containing the vertex type as the key and the corresponding
            vertex's frame with a triangle_count column.
            Call dictionary_name['label'] to get the handle to frame whose vertex
            type is label.
        :rtype: dict
        """
        return None


    @property
    @doc_stub
    def last_read_date(self):
        """
        Last time this frame's data was accessed.



        :returns: Date string of the last time this frame's data was accessed
        :rtype: str
        """
        return None


    @property
    @doc_stub
    def ml(self):
        """
        Access to object's ml functionality (See :class:`~trustedanalytics.core.docstubs.GraphMl`)



        :returns: GraphMl object
        :rtype: GraphMl
        """
        return None


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the graph object.

        Change or retrieve graph object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_graph.name

            "csv_data"

            >>> my_graph.name = "cleaned_data"
            >>> my_graph.name

            "cleaned_data"



        """
        return None


    @property
    @doc_stub
    def status(self):
        """
        Current graph life cycle status.

        One of three statuses: Active, Dropped, Finalized
        -   Active:    Entity is available for use
        -   Dropped:   Entity has been dropped by user or by garbage collection which found it stale
        -   Finalized: Entity's data has been deleted




        :returns: Status of the graph.
        :rtype: str
        """
        return None


    @property
    @doc_stub
    def vertex_count(self):
        """
        Get the total number of vertices in the graph.

        Returns
        -------
        int32
            The number of vertices in the graph.


        Examples
        --------

        .. code::

            >>> my_graph.vertex_count

        The result given is:

        .. code::

            1194




        """
        return None


    @property
    @doc_stub
    def vertices(self):
        """
        Vertex frame collection

        Examples
        --------
        Inspect vertices with the supplied label:

        .. code::

            >>> my_graph.vertices['label'].inspect()




        """
        return None



@doc_stub
class GraphMl(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """

    @doc_stub
    def belief_propagation(self, prior_property, posterior_property, edge_weight_property=None, convergence_threshold=None, max_iterations=None):
        """
        Classification on sparse data using Belief Propagation.

        Belief propagation by the sum-product algorithm.
        This algorithm analyzes a graphical model with prior beliefs using sum product message passing.
        The priors are read from a property in the graph, the posteriors are written to another property in the graph.
        This is the GraphX-based implementation of belief propagation.

        See :ref:`Loopy Belief Propagation <python_api/frames/frame-/loopy_belief_propagation>`
        for a more in-depth discussion of |BP| and |LBP|.

        Examples
        --------
        .. only:: html

            .. code::

                >>> graph.ml.belief_propagation("value", "lbp_output", string_output = True, state_space_size = 5, max_iterations = 6)

                {u'log': u'Vertex Count: 80000\nEdge Count: 318398\nAtkPregel engine has completed iteration 1  The average delta is 0.6853413553663811\nAtkPregel engine has completed iteration 2  The average delta is 0.38626944467366386\nAtkPregel engine has completed iteration 3  The average delta is 0.2365329376479823\nAtkPregel engine has completed iteration 4  The average delta is 0.14170840479478952\nAtkPregel engine has completed iteration 5  The average delta is 0.08676093923623975\n', u'time': 70.248999999999995}

                >>> graph.query.gremlin("g.V [0..4]")

                {u'results': [{u'vertex_type': u'VA', u'target': 12779523, u'lbp_output': u'0.9485759073302487, 0.001314151524421738, 0.040916996746627056, 0.001397331576080859, 0.0077956128226217315', u'_type': u'vertex', u'value': u'0.125 0.125 0.5 0.125 0.125', u'titanPhysicalId': 4, u'_id': 4}, {u'vertex_type': u'VA', u'titanPhysicalId': 8, u'lbp_output': u'0.7476996339617544, 0.0021769696832380173, 0.24559940461433935, 0.0023272253558738786, 0.002196766384794168', u'_type': u'vertex', u'value': u'0.125 0.125 0.5 0.125 0.125', u'source': 7798852, u'_id': 8}, {u'vertex_type': u'TR', u'target': 13041863, u'lbp_output': u'0.7288360734608738, 0.07162637515155296, 0.15391773902131053, 0.022620779563724287, 0.02299903280253846', u'_type': u'vertex', u'value': u'0.5 0.125 0.125 0.125 0.125', u'titanPhysicalId': 12, u'_id': 12}, {u'vertex_type': u'TR', u'titanPhysicalId': 16, u'lbp_output': u'0.9996400056392905, 9.382190989071985E-5, 8.879762476576982E-5, 8.867586165695348E-5, 8.869896439624652E-5', u'_type': u'vertex', u'value': u'0.5 0.125 0.125 0.125 0.125', u'source': 11731127, u'_id': 16}, {u'vertex_type': u'TE', u'titanPhysicalId': 20, u'lbp_output': u'0.004051247779081896, 0.2257641948616088, 0.01794622866204068, 0.7481547408142287, 0.004083587883039745', u'_type': u'vertex', u'value': u'0.125 0.125 0.5 0.125 0.125', u'source': 3408035, u'_id': 20}], u'run_time_seconds': 1.042}

        .. only:: latex

            .. code::

                >>> graph.ml.belief_propagation("value", "lbp_output", string_output = True,
                ...    state_space_size = 5, max_iterations = 6)

                {u'log': u'Vertex Count: 80000\n
                Edge Count: 318398\n
                AtkPregel engine has completed iteration 1  The average delta is 0.6853413553663811\n
                AtkPregel engine has completed iteration 2  The average delta is 0.38626944467366386\n
                AtkPregel engine has completed iteration 3  The average delta is 0.2365329376479823\n
                AtkPregel engine has completed iteration 4  The average delta is 0.14170840479478952\n
                AtkPregel engine has completed iteration 5  The average delta is 0.08676093923623975\n
                ', u'time': 70.248999999999995}

                >>> graph.query.gremlin("g.V [0..4]")

                {u'results': [{u'vertex_type':
                 u'VA',
                 u'target': 12779523,
                 u'lbp_output':
                 u'0.9485759073302487, 0.001314151524421738,
                    0.040916996746627056, 0.001397331576080859, 0.0077956128226217315',
                 u'_type':
                 u'vertex',
                 u'value':
                 u'0.125 0.125 0.5 0.125 0.125',
                 u'titanPhysicalId': 4,
                 u'_id': 4},
                {u'vertex_type':
                 u'VA',
                 u'titanPhysicalId': 8,
                 u'lbp_output':
                 u'0.7476996339617544,
                    0.0021769696832380173, 0.24559940461433935, 0.0023272253558738786,
                    0.002196766384794168',
                 u'_type':
                 u'vertex',
                 u'value':
                 u'0.125 0.125 0.5 0.125 0.125',
                 u'source': 7798852,
                 u'_id': 8},
                {u'vertex_type':
                 u'TR',
                 u'target': 13041863,
                 u'lbp_output':
                 u'0.7288360734608738, 0.07162637515155296,
                    0.15391773902131053, 0.022620779563724287, 0.02299903280253846',
                 u'_type':
                 u'vertex',
                 u'value':
                 u'0.5 0.125 0.125 0.125 0.125',
                 u'titanPhysicalId': 12,
                 u'_id': 12},
                {u'vertex_type':
                 u'TR',
                 u'titanPhysicalId': 16,
                 u'lbp_output':
                 u'0.9996400056392905,
                    9.382190989071985E-5, 8.879762476576982E-5, 8.867586165695348E-5,
                    8.869896439624652E-5',
                 u'_type':
                 u'vertex',
                 u'value':
                 u'0.5 0.125 0.125 0.125 0.125',
                 u'source': 11731127,
                 u'_id': 16},
                {u'vertex_type':
                 u'TE',
                 u'titanPhysicalId': 20,
                 u'lbp_output':
                 u'0.004051247779081896, 0.2257641948616088,
                    0.01794622866204068, 0.7481547408142287, 0.004083587883039745',
                 u'_type':
                 u'vertex',
                 u'value':
                 u'0.125 0.125 0.5 0.125 0.125',
                 u'source': 3408035,
                 u'_id': 20}],
                 u'run_time_seconds': 1.045}




        :param prior_property: Name of the vertex property which contains the prior belief
            for the vertex.
        :type prior_property: unicode
        :param posterior_property: Name of the vertex property which
            will contain the posterior belief for each
            vertex.
        :type posterior_property: unicode
        :param edge_weight_property: (default=None)  Name of the edge property that contains the edge weight for each edge.
        :type edge_weight_property: unicode
        :param convergence_threshold: (default=None)  Belief propagation will terminate
            when the average change in posterior beliefs between supersteps is
            less than or equal to this threshold.
        :type convergence_threshold: float64
        :param max_iterations: (default=None)  The maximum number of supersteps that the algorithm will execute.
            The valid range is all positive int.
        :type max_iterations: int32

        :returns: Progress report for belief propagation in the format of a multiple-line string.
        :rtype: dict
        """
        return None


    @doc_stub
    def kclique_percolation(self, clique_size, community_property_label):
        """
        Find groups of vertices with similar attributes.

        **Community Detection Using the K-Clique Percolation Algorithm**

        **Overview**

        Modeling data as a graph captures relations, for example, friendship ties
        between social network users or chemical interactions between proteins.
        Analyzing the structure of the graph reveals collections (often termed
        'communities') of vertices that are more likely to interact amongst each
        other.
        Examples could include a community of friends in a social network or a
        collection of highly interacting proteins in a cellular process.

        |PACKAGE| provides community detection using the k-Clique
        percolation method first proposed by Palla et. al. [1]_ that has been widely
        used in many contexts.

        **K-Clique Percolation**

        K-clique percolation is a method for detecting community structure in graphs.
        Here we provide mathematical background on how communities are defined in the
        context of the k-clique percolation algorithm.

        A clique is a group of vertices in which every vertex is connected (via
        undirected edge) with every other vertex in the clique.
        This graphically looks like a triangle or a structure composed of triangles:

        .. image:: /k-clique_201508281155.*

        A clique is certainly a community in the sense that its vertices are all
        connected, but, it is too restrictive for most purposes,
        since it is natural some members of a community may not interact.

        Mathematically, a k-clique has :math:`k` vertices, each with :math:`k - 1`
        common edges, each of which connects to another vertex in the k-clique.
        The k-clique percolation method forms communities by taking unions of k-cliques
        that have :math:`k - 1` vertices in common.

        **K-Clique Example**

        In the graph below, the cliques are the sections defined by their triangular
        appearance and the 3-clique communities are {1, 2, 3, 4} and {4, 5, 6, 7, 8}.
        The vertices 9, 10, 11, 12 are not in 3-cliques, therefore they do not belong
        to any community.
        Vertex 4 belongs to two distinct (but overlapping) communities.

        .. image:: /ds_mlal_a1.png

        **Distributed Implementation of K-Clique Community Detection**

        The implementation of k-clique community detection in |PACKAGE| is a fully
        distributed implementation that follows the map-reduce
        algorithm proposed in Varamesh et. al. [2]_ .

        It has the following steps:

        #.  All k-cliques are enumerated <enumerate>.
        #.  k-cliques are used to build a "clique graph" by declaring each k-clique to
            be a vertex in a new graph and placing edges between k-cliques that share
            k-1 vertices in the base graph.
        #.  A connected component analysis is performed on the clique graph.
            Connected components of the clique graph correspond to k-clique communities
            in the base graph.
        #.  The connected components information for the clique graph is projected back
            down to the base graph, providing each vertex with the set of k-clique
            communities to which it belongs.

        Notes
        -----
        Spawns a number of Spark jobs that cannot be calculated before execution
        (it is bounded by the diameter of the clique graph derived from the input graph).
        For this reason, the initial loading, clique enumeration and clique-graph
        construction steps are tracked with a single progress bar (this is most of
        the time), and then successive iterations of analysis of the clique graph
        are tracked with many short-lived progress bars, and then finally the
        result is written out.


        .. rubric:: Footnotes

        .. [1]
            G. Palla, I. Derenyi, I. Farkas, and T. Vicsek. Uncovering the overlapping
            community structure of complex networks in nature and society.
            Nature, 435:814, 2005 ( See http://hal.elte.hu/cfinder/wiki/papers/communitylettm.pdf )

        .. [2]
            Varamesh, A.; Akbari, M.K.; Fereiduni, M.; Sharifian, S.; Bagheri, A.,
            "Distributed Clique Percolation based community detection on social
            networks using MapReduce,"
            Information and Knowledge Technology (IKT), 2013 5th Conference on, vol.,
            no., pp.478,483, 28-30 May 2013


        Examples
        --------
        .. code::

            >>> import trustedanalytics as ta
            >>> ta.connect()
            >>> dataset = r"datasets/kclique_edges.csv"
            >>> schema = [("source", int64), ("target", int64)]
            >>> csvfile = ta.CsvFile(dataset, schema)
            >>> my_frame = ta.Frame(csvfile)

            >>> my_graph = ta.Graph())
            >>> my_graph.name = "mygraph"
            >>> source_vertex_type = my_graph.define_vertex_type("source")
            >>> target_vertex_type = my_graph.define_vertex_type("target")
            >>> direction_edge_type = my_graph.define_edge_type("direction",
            ... "source", "target", directed=True)

            >>> my_graph.vertices['source'].add_vertices(my_frame, 'source')
            >>> my_graph.vertices['target'].add_vertices(my_frame, 'target')
            >>> my_graph.edges['direction'].add_edges(my_frame, 'source', 'target',
            ... is_directed=True)
            >>> my_titan_graph = my_graph.export_to_titan("mytitangraph"))
            >>> my_titan_graph.ml.kclique_percolation(cliqueSize = 3,
            ... communityPropertyDefaultLabel = "Community")


        :param clique_size: The sizes of the cliques used to form communities.
            Larger values of clique size result in fewer, smaller communities that are more connected.
            Must be at least 2.
        :type clique_size: int32
        :param community_property_label: Name of the community property of vertex that will be updated/created in the graph.
            This property will contain for each vertex the set of communities that contain that
            vertex.
        :type community_property_label: unicode

        :returns: Dictionary of vertex label and frame, Execution time.
        :rtype: dict
        """
        return None



@doc_stub
class _DocStubsTitanGraph(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Initialize the graph.

        Examples
        --------
        Starting with a ta.Graph you can export to Titan to take advantage of Gremlin query.

        .. code::

            >>> graph = ta.get_graph("my_graph")
            >>> titan_graph = graph.export_to_titan("titan_graph")


        :param name: (default=None)  
        :type name: 
        """
        raise DocStubCalledError("graph:titan/__init__")


    @doc_stub
    def annotate_degrees(self, output_property_name, degree_option=None, input_edge_labels=None):
        """
        Make new graph with degrees.

        Creates a new graph which is the same as the input graph, with the addition
        that every vertex of the graph has its degree stored in a user-specified property.

        **Degree Calculation**

        A fundamental quantity in graph analysis is the degree of a vertex:
        The degree of a vertex is the number of edges adjacent to it.

        For a directed edge relation, a vertex has both an out-degree (the number of
        edges leaving the vertex) and an in-degree (the number of edges entering the
        vertex).

        The toolkit provides this routine for calculating the degrees of vertices.
        This calculation could be performed with a Gremlin query on smaller datasets
        because Gremlin queries cannot be executed on a distributed scale.
        The |PACKAGE| routine ``annotate_degrees`` can be executed at distributed scale.

        In the presence of edge weights, vertices can have weighted degrees: The
        weighted degree of a vertex is the sum of weights of edges adjacent to it.
        Analogously, the weighted in-degree of a vertex is the sum of the weights of
        the edges entering it, and the weighted out-degree is the sum
        of the weights of the edges leaving the vertex.

        The toolkit provides :ref:`annotate_weighted_degrees <python_api/graphs/graph-/annotate_weighted_degrees>`
        for the distributed calculation of weighted vertex degrees.

        Examples
        --------
        Given a graph:

        .. code::

            >>> g.query.gremlin('g.V [ 0 .. 1]')

            Out[12]:
               {u'results': [{u'_id': 19456,
                u'_label': u'vertex',
                u'_type': u'vertex',
                u'_vid': 545413,
                u'source': 6961},
               {u'_id': 19968,
                u'_label': u'vertex',
                u'_type': u'vertex',
                u'_vid': 511316,
                u'source': 31599}],
                u'run_time_seconds': 1.822}

            >>> h = g.annotate_degrees('degree')



        :param output_property_name: The name of the new property.
            The degree is stored in this property.
        :type output_property_name: unicode
        :param degree_option: (default=None)  Indicator for the definition of degree to be used for the
            calculation.
            Permitted values:

            *   "out" (default value) : Degree is calculated as the out-degree.
            *   "in" : Degree is calculated as the in-degree.
            *   "undirected" : Degree is calculated as the undirected degree.
                (Assumes that the edges are all undirected.)
               
            Any prefix of the strings "out", "in", "undirected" will select the
            corresponding option.
        :type degree_option: unicode
        :param input_edge_labels: (default=None)  If this list is provided, only edges whose labels are
            included in the given set will be considered in the degree calculation.
            In the default situation (when no list is provided), all edges will be used
            in the degree calculation, regardless of label.
        :type input_edge_labels: list

        :returns: Dictionary containing the vertex type as the key and the corresponding
            vertex's frame with a column storing the annotated degree for the vertex
            in a user specified property.
            Call dictionary_name['label'] to get the handle to frame whose vertex type
            is label.
        :rtype: dict
        """
        return None


    @doc_stub
    def annotate_weighted_degrees(self, output_property_name, degree_option=None, input_edge_labels=None, edge_weight_property=None, edge_weight_default=None):
        """
        Calculates the weighted degree of each vertex with respect to an (optional) set of labels.

        Pulls graph from underlying store, calculates weighted degrees and writes them into the property
        specified, and then writes the output graph to the underlying store.

        **Degree Calculation**

        A fundamental quantity in graph analysis is the degree of a vertex:
        The degree of a vertex is the number of edges adjacent to it.

        For a directed edge relation, a vertex has both an out-degree (the number of
        edges leaving the vertex) and an in-degree (the number of edges entering the
        vertex).

        The toolkit provides a routine :ref:`annotate_degrees
        <python_api/graphs/graph-/annotate_weighted_degrees>`
        for calculating the degrees of vertices.
        This calculation could be performed with a Gremlin query on smaller datasets
        because Gremlin queries cannot be executed on a distributed scale.
        The |PACKAGE| routine ``annotate_degrees`` can be executed at distributed scale.

        In the presence of edge weights, vertices can have weighted degrees: The
        weighted degree of a vertex is the sum of weights of edges adjacent to it.
        Analogously, the weighted in-degree of a vertex is the sum of the weights of
        the edges entering it, and the weighted out-degree is the sum
        of the weights of the edges leaving the vertex.

        The toolkit provides this routine for the distributed calculation of weighted
        vertex degrees.

        Examples
        --------
        Given a directed graph with three nodes and two edges like this:

        .. only:: html

            .. code::

                >>> g.query.gremlin('g.V')
                Out[23]: {u'results': [{u'_id': 28304, u'_label': u'vertex', u'_type': u'vertex', u'_vid': 4, u'source': 2}, {u'_id': 21152, u'_label': u'vertex', u'_type': u'vertex', u'_vid': 1, u'source': 1}, {u'_id': 28064, u'_label': u'vertex', u'_type': u'vertex', u'_vid': 3, u'source': 3}], u'run_time_seconds': 1.245}

                >>> g.query.gremlin('g.E')
                Out[24]: {u'results': [{u'_eid': 3, u'_id': u'34k-gbk-bth-lnk', u'_inV': 28064, u'_label': u'edge', u'_outV': 21152, u'_type': u'edge', u'weight': 0.01}, {u'_eid': 4, u'_id': u'1xw-gbk-bth-lu8', u'_inV': 28304, u'_label': u'edge', u'_outV': 21152, u'_type': u'edge', u'weight': 0.1}], u'run_time_seconds': 1.359}

                >>> h = g.annotate_weighted_degrees('weight',  edge_weight_property = 'weight')

        .. only:: latex

            .. code::

                >>> g.query.gremlin('g.V')
                Out[23]:
                {u'results': [{u'_id': 28304,
                 u'_label': u'vertex',
                 u'_type': u'vertex',
                 u'_vid': 4,
                 u'source': 2},
                {u'_id': 21152,
                 u'_label': u'vertex',
                 u'_type': u'vertex',
                 u'_vid': 1,
                 u'source': 1},
                {u'_id': 28064,
                 u'_label': u'vertex',
                 u'_type': u'vertex',
                 u'_vid': 3,
                 u'source': 3}],
                 u'run_time_seconds': 1.245}

                >>> g.query.gremlin('g.E')
                Out[24]:
                {u'results': [{u'_eid': 3,
                 u'_id': u'34k-gbk-bth-lnk',
                 u'_inV': 28064,
                 u'_label': u'edge',
                 u'_outV': 21152,
                 u'_type': u'edge',
                 u'weight': 0.01},
                {u'_eid': 4,
                 u'_id': u'1xw-gbk-bth-lu8',
                 u'_inV': 28304,
                 u'_label': u'edge',
                 u'_outV': 21152,
                 u'_type': u'edge',
                 u'weight': 0.1}],
                 u'run_time_seconds': 1.359}

                >>> h = g.annotate_weighted_degrees(
                ...        'weight',
                ...        edge_weight_property = 'weight')



        :param output_property_name: property name of where to store output
        :type output_property_name: unicode
        :param degree_option: (default=None)  choose from 'out', 'in', 'undirected'
        :type degree_option: unicode
        :param input_edge_labels: (default=None)  labels of edge types that should be included
        :type input_edge_labels: list
        :param edge_weight_property: (default=None)  property name of edge weight, if not provided all edges are weighted equally
        :type edge_weight_property: unicode
        :param edge_weight_default: (default=None)  default edge weight
        :type edge_weight_default: float64

        :returns: 
        :rtype: dict
        """
        return None


    @doc_stub
    def clustering_coefficient(self, output_property_name=None, input_edge_labels=None):
        """
        Coefficient of graph with respect to labels.

        Calculates the clustering coefficient of the graph with respect to an (optional) set of labels.

        Pulls graph from underlying store, calculates degrees and writes them into the property specified,
        and then writes the output graph to the underlying store.

        .. warning::

            THIS FUNCTION IS FOR UNDIRECTED GRAPHS.
            If it is called on a directed graph, its output is NOT guaranteed to calculate
            the local directed clustering coefficients.

        |
        **Clustering Coefficients**

        The clustering coefficient of a graph provides a measure of how tightly
        clustered an undirected graph is.
        Informally, if the edge relation denotes "friendship", the clustering
        coefficient of the graph is the probability that two people are friends given
        that they share a common friend.

        More formally:

        .. math::

            cc(G)  = \frac{ \| \{ (u,v,w) \in V^3: \ \{u,v\}, \{u, w\}, \{v,w \} \in \
            E \} \| }{\| \{ (u,v,w) \in V^3: \ \{u,v\}, \{u, w\} \in E \} \|}


        Analogously, the clustering coefficient of a vertex provides a measure of how
        tightly clustered that vertex's neighborhood is.
        Informally, if the edge relation denotes "friendship", the clustering
        coefficient at a vertex :math:`v` is the probability that two acquaintances of
        :math:`v` are themselves friends.

        More formally:

        .. math::

            cc(v)  = \frac{ \| \{ (u,v,w) \in V^3: \ \{u,v\}, \{u, w\}, \{v,w \} \in \
            E \} \| }{\| \{ (u,v,w) \in V^3: \ \{v, u \}, \{v, w\} \in E \} \|}


        The toolkit provides the function clustering_coefficient which computes both
        local and global clustering coefficients for a given undirected graph.

        For more details on the mathematics and applications of clustering
        coefficients, see http://en.wikipedia.org/wiki/Clustering_coefficient.



        Examples
        --------
        .. code::

            >>> results = g.clustering_coefficient('ccgraph', 'local_clustering_coefficient')

            >>> results
                Out[8]:
                ClusteringCoefficient:
                global_clustering_coefficient: 0.0853107962708,
                frame: Frame

            >>> results.frame.inspect()


        :param output_property_name: (default=None)  The name of the new property to which each
            vertex's local clustering coefficient will be written.
            If this option is not specified, no output frame will be produced and only
            the global clustering coefficient will be returned.
        :type output_property_name: unicode
        :param input_edge_labels: (default=None)  If this list is provided,
            only edges whose labels are included in the given
            set will be considered in the clustering coefficient calculation.
            In the default situation (when no list is provided), all edges will be used
            in the calculation, regardless of label.
            It is required that all edges that enter into the clustering coefficient
            analysis be undirected.
        :type input_edge_labels: list

        :returns: Dictionary of the global clustering coefficient of the graph or,
            if local clustering coefficients are requested, a reference to the frame with local
            clustering coefficients stored at properties at each vertex.
        :rtype: dict
        """
        return None


    @doc_stub
    def copy(self, name=None):
        """
        Make a copy of the current graph.

        Examples
        --------
        For this example, graph object *my_graph* accesses a graph:

        .. code::

            >>> copied_graph = my_graph.copy('my_graph2')


        :param name: (default=None)  The name for the copy of the graph.
            Default is None.
        :type name: unicode

        :returns: A copy of the original graph.
        :rtype: dict
        """
        return None


    @doc_stub
    def export_to_graph(self):
        """
        Export from TitanGraph to Graph.



        :returns: 
        :rtype: dict
        """
        return None


    @doc_stub
    def graph_clustering(self, edge_distance):
        """
        Performs graph clustering over an initial titan graph.

        Performs graph clustering over an initial titan graph using a distributed edge collapse algorithm.

        Examples
        --------
        The data file sample_graph.txt is a file in the following format: src, dest,
        distance:

        .. code::

            1, 2, 1.5f
            2, 1, 1.5f
            2, 3, 1.5f
            3, 2, 1.5f
            1, 3, 1.5f
            3, 1, 1.5f

        The edge column name should be passed in as an argument to the plug-in.

        .. code::

            >>> import trustedanalytics as ta
            >>> ta.connect()
            >>> my_graph = ta.get_graph("mytitangraph")
            >>> my_graph.graph_clustering("dist")

        The expected output (new vertices) can be queried:

        .. only:: html

            .. code::

                >>> my_graph.query.gremlin('g.V.map(\'id\', \'vertex\', \'_label\', \'name\',\'count\')')

        .. only:: latex

            .. code::

                >>> my_graph.query.gremlin('g.V.map(\'id\', \'vertex\', \'_label\',
                ... \'name\',\'count\')')

        Snippet output for the above query will look like this:

        .. only:: html

            .. code::

                {u'results': [u'{id=18432, count=null, _label=null, vertex=29, name=null}', u'{id=24576, count=null, _label=null, vertex=22, name=null}', u'{id=27136, count=null, _label=2, vertex=null, name=21944_25304}'

        .. only:: latex

            .. code::

                {u'results':
                 [u'{id=18432, count=null, _label=null, vertex=29, name=null}',
                  u'{id=24576, count=null, _label=null, vertex=22, name=null}',
                  u'{id=27136, count=null, _label=2, vertex=null, name=21944_25304}'

        where:

            ``24576`` - represents an initial node
            ``27136`` - represents a meta-node of 2 nodes (as per _label value)







        :param edge_distance: Column name for the edge distance.
        :type edge_distance: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def graphx_connected_components(self, output_property):
        """
        Implements the connected components computation on a graph by invoking graphx api.

        Pulls graph from underlying store, sends it off to the ConnectedComponentGraphXDefault,
        and then writes the output graph back to the underlying store.

        |
        **Connected Components (CC)**

        Connected components are disjoint subgraphs in which all vertices are
        connected to all other vertices in the same component via paths, but not
        connected via paths to vertices in any other component.
        The connected components algorithm uses message passing along a specified edge
        type to find all of the connected components of a graph and label each edge
        with the identity of the component to which it belongs.
        The algorithm is specific to an edge type, hence in graphs with several
        different types of edges, there may be multiple, overlapping sets of connected
        components.

        The algorithm works by assigning each vertex a unique numerical index and
        passing messages between neighbors.
        Vertices pass their indices back and forth with their neighbors and update
        their own index as the minimum of their current index and all other indices
        received.
        This algorithm continues until there is no change in any of the vertex
        indices.
        At the end of the algorithm, the unique levels of the indices denote the
        distinct connected components.
        The complexity of the algorithm is proportional to the diameter of the graph.


        Examples
        --------
        .. code::

            >>> f= g.graphx_connected_components(output_property = "ccId")

        The expected output is like this:

        .. code::

            {u'movie': Frame "None"
             row_count = 597
             schema =
               _vid:int64
               _label:unicode
               movie:int32
               Con_Com:int64, u'user': Frame "None"
             row_count = 597
             schema =
               _vid:int64
               _label:unicode
               vertexType:unicode
               user:int32
               Con_Com:int64}

        To query:

        .. code::

            >>> movie_frame = f['movie']
            >>> user_frame = f['user']



        :param output_property: The name of the column containing the connected component value.
        :type output_property: unicode

        :returns: Dictionary containing the vertex type as the key and the corresponding
              vertex's frame with a connected component column.
              Call dictionary_name['label'] to get the handle to frame whose vertex type is label.
        :rtype: dict
        """
        return None


    @doc_stub
    def graphx_pagerank(self, output_property, input_edge_labels=None, max_iterations=None, reset_probability=None, convergence_tolerance=None):
        """
        Determine which vertices are the most important.

        Pulls graph from underlying store, sends it off to the
        PageRankRunner, and then writes the output graph back to the underlying store.

        This method (currently) only supports Titan for graph storage.

        ** Experimental Feature **

        **Basics and Background**

        *PageRank* is a method for determining which vertices in a directed graph are
        the most central or important.
        *PageRank* gives each vertex a score which can be interpreted as the
        probability that a person randomly walking along the edges of the graph will
        visit that vertex.

        The calculation of *PageRank* is based on the supposition that if a vertex has
        many vertices pointing to it, then it is "important",
        and that a vertex grows in importance as more important vertices point to it.
        The calculation is based only on the network structure of the graph and makes
        no use of any side data, properties, user-provided scores or similar
        non-topological information.

        *PageRank* was most famously used as the core of the Google search engine for
        many years, but as a general measure of centrality in a graph, it has
        other uses to other problems, such as recommendation systems and
        analyzing predator-prey food webs to predict extinctions.

        **Background references**

        *   Basic description and principles: `Wikipedia\: PageRank`_
        *   Applications to food web analysis: `Stanford\: Applications of PageRank`_
        *   Applications to recommendation systems: `PLoS\: Computational Biology`_

        **Mathematical Details of PageRank Implementation**

        The |PACKAGE| implementation of *PageRank* satisfies the following equation
        at each vertex :math:`v` of the graph:

        .. math::

            PR(v) = \frac {\rho}{n} + \rho \left( \sum_{u\in InSet(v)} \
            \frac {PR(u)}{L(u)} \right)

        Where:
            |   :math:`v` |EM| a vertex
            |   :math:`L(v)` |EM| outbound degree of the vertex v
            |   :math:`PR(v)` |EM| *PageRank* score of the vertex v
            |   :math:`InSet(v)` |EM| set of vertices pointing to the vertex v
            |   :math:`n` |EM| total number of vertices in the graph
            |   :math:`\rho` |EM| user specified damping factor (also known as reset
                probability)

        Termination is guaranteed by two mechanisms.

        *   The user can specify a convergence threshold so that the algorithm will
            terminate when, at every vertex, the difference between successive
            approximations to the *PageRank* score falls below the convergence
            threshold.
        *   The user can specify a maximum number of iterations after which the
            algorithm will terminate.

        .. _Wikipedia\: PageRank: http://en.wikipedia.org/wiki/PageRank
        .. _Stanford\: Applications of PageRank: http://web.stanford.edu/class/msande233/handouts/lecture8.pdf
        .. _PLoS\: Computational Biology:
            http://www.ploscompbiol.org/article/fetchObject.action?uri=info%3Adoi%2F10.1371%2Fjournal.pcbi.1000494&representation=PDF

        Examples
        --------
        .. only:: html

            .. code::

                >>> graph = ta.Graph()
                >>> graph.define_vertex_type("node")
                >>> graph.vertices["node"].add_vertices(frame,"follows")
                >>> graph.vertices["node"].add_vertices(frame,"followed")
                >>> graph.define_edge_type("e1","node","node",directed=True)
                >>> graph.edges["e1"].add_edges(frame,"follows","followed")
                >>> result = graph.graphx_pagerank(output_property="PageRank",max_iterations=2,convergence_tolerance=0.001)
                >>> vertex_dict = result['vertex_dictionary']
                >>> edge_dict = result['edge_dictionary']

        .. only:: latex

            .. code::

                >>> graph = ta.Graph()
                >>> graph.define_vertex_type("node")
                >>> graph.vertices["node"].add_vertices(frame,"follows")
                >>> graph.vertices["node"].add_vertices(frame,"followed")
                >>> graph.define_edge_type("e1","node","node",directed=True)
                >>> graph.edges["e1"].add_edges(frame,"follows","followed")
                >>> result = graph.graphx_pagerank(output_property="PageRank",max_iterations=2,convergence_tolerance=0.001)
                >>> vertex_dict = result['vertex_dictionary']
                >>> edge_dict = result['edge_dictionary']


        :param output_property: Name of the property to which PageRank
            value will be stored on vertex and edge.
        :type output_property: unicode
        :param input_edge_labels: (default=None)  List of edge labels to consider for PageRank computation.
            Default is all edges are considered.
        :type input_edge_labels: list
        :param max_iterations: (default=None)  The maximum number of iterations that will be invoked.
            The valid range is all positive int.
            Invalid value will terminate with vertex page rank set to reset_probability.
            Default is 20.
        :type max_iterations: int32
        :param reset_probability: (default=None)  The probability that the random walk of a page is reset.
            Default is 0.15.
        :type reset_probability: float64
        :param convergence_tolerance: (default=None)  The amount of change in cost function that will be tolerated at
            convergence.
            If this parameter is specified, max_iterations is not considered as a stopping condition.
            If the change is less than this threshold, the algorithm exits earlier.
            The valid value range is all float and zero.
            Default is 0.001.
        :type convergence_tolerance: float64

        :returns: dict((vertex_dictionary, (label, Frame)), (edge_dictionary,(label,Frame))).

            Dictionary containing dictionaries of labeled vertices and labeled edges.

            For the *vertex_dictionary* the vertex type is the key and the corresponding
            vertex's frame with a new column storing the page rank value for the vertex.
            Call vertex_dictionary['label'] to get the handle to frame whose vertex
            type is label.

            For the *edge_dictionary* the edge type is the key and the corresponding
            edge's frame with a new column storing the page rank value for the edge.
            Call edge_dictionary['label'] to get the handle to frame whose edge type
            is label.
        :rtype: dict
        """
        return None


    @doc_stub
    def graphx_triangle_count(self, output_property, input_edge_labels=None):
        """
        Number of triangles among vertices of current graph.

        ** Experimental Feature **

        Counts the number of triangles among vertices in an undirected graph.
        If an edge is marked bidirectional, the implementation opts for canonical
        orientation of edges hence counting it only once (similar to an
        undirected graph).

        Examples
        --------
        .. only:: html
           
            .. code::

                >>> f = g.graphx_triangle_count(output_property = "triangle_count", output_graph_name = "tc_graph")

        .. only:: latex
           
            .. code::

                >>> f = g.graphx_triangle_count(output_property = "triangle_count",
                ... output_graph_name = "tc_graph")

        The expected output is like this:

        .. code::

            {u'label1': Frame "None"
            row_count = 110
            schema =
              _vid:int64
              _label:unicode
              max_k:int64
              cc:int64
              TC:int32
              node:unicode,
            u'label2': Frame "None"
            row_count = 430
            schema =
              _vid:int64
              _label:unicode
              max_k:int64
              cc:int64
              TC:int32
              node:unicode}


        To query:

        .. only:: html

            .. code::

                >>> frame_for_label1 = f['label1']
                >>> frame_for_label1.inspect(10)
                
                  _vid:int64   _label:unicode   max_k:int64   cc:int64   TC:int32   node:unicode
                /--------------------------------------------------------------------------------/
                      106656   label1                     2         12          0   node158
                      129504   label1                     3         23          1   node2116
                       86640   label1                     7         17         15   node183
                       20424   label1                     7         47         15   node4248
                      164184   label1                     2         72          0   node7388
                       23232   label1                     9         39         28   node3210
                       93840   label1                     3         83          1   node8446
                      114480   label1                     8         58         21   node5311
                       48480   label1                    10         30         36   node2166
                       31152   label1                     6         96         10   node9516


        .. only:: latex

            .. code::

                >>> frame_for_label1 = f['label1']
                >>> frame_for_label1.inspect(10)

                   _vid   _label   max_k  cc     TC     node
                   int64  unicode  int64  int64  int32  unicode
                /------------------------------------------------\
                  106656  label1       2     12      0  node158
                  129504  label1       3     23      1  node2116
                   86640  label1       7     17     15  node183
                   20424  label1       7     47     15  node4248
                  164184  label1       2     72      0  node7388
                   23232  label1       9     39     28  node3210
                   93840  label1       3     83      1  node8446
                  114480  label1       8     58     21  node5311
                   48480  label1      10     30     36  node2166
                   31152  label1       6     96     10  node9516




        :param output_property: The name of output property to be
            added to vertex/edge upon completion.
        :type output_property: unicode
        :param input_edge_labels: (default=None)  The name of edge labels to be considered for triangle count.
            Default is all edges are considered.
        :type input_edge_labels: list

        :returns: dict(label, Frame).

            Dictionary containing the vertex type as the key and the corresponding
            vertex's frame with a triangle_count column.
            Call dictionary_name['label'] to get the handle to frame whose vertex
            type is label.
        :rtype: dict
        """
        return None


    @property
    @doc_stub
    def last_read_date(self):
        """
        Last time this frame's data was accessed.



        :returns: Date string of the last time this frame's data was accessed
        :rtype: str
        """
        return None


    @property
    @doc_stub
    def ml(self):
        """
        Access to object's ml functionality (See :class:`~trustedanalytics.core.docstubs.TitanGraphMl`)



        :returns: TitanGraphMl object
        :rtype: TitanGraphMl
        """
        return None


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the graph object.

        Change or retrieve graph object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_graph.name

            "csv_data"

            >>> my_graph.name = "cleaned_data"
            >>> my_graph.name

            "cleaned_data"



        """
        return None


    @property
    @doc_stub
    def query(self):
        """
        Access to object's query functionality (See :class:`~trustedanalytics.core.docstubs.TitanGraphQuery`)



        :returns: TitanGraphQuery object
        :rtype: TitanGraphQuery
        """
        return None


    @property
    @doc_stub
    def status(self):
        """
        Current graph life cycle status.

        One of three statuses: Active, Dropped, Finalized
        -   Active:    Entity is available for use
        -   Dropped:   Entity has been dropped by user or by garbage collection which found it stale
        -   Finalized: Entity's data has been deleted




        :returns: Status of the graph.
        :rtype: str
        """
        return None


    @doc_stub
    def vertex_sample(self, size, sample_type, seed=None):
        """
        Make subgraph from vertex sampling.

        Create a vertex induced subgraph obtained by vertex sampling.
        Three types of vertex sampling are provided: 'uniform', 'degree', and
        'degreedist'.
        A 'uniform' vertex sample is obtained by sampling vertices uniformly at random.
        For 'degree' vertex sampling, each vertex is weighted by its out-degree.
        For 'degreedist' vertex sampling, each vertex is weighted by the total
        number of vertices that have the same out-degree as it.
        That is, the weight applied to each vertex for 'degreedist' vertex sampling
        is given by the out-degree histogram bin size.

        :param size: The number of vertices to sample from the graph.
        :type size: int32
        :param sample_type: The type of vertex sample among: ['uniform', 'degree', 'degreedist'].
        :type sample_type: unicode
        :param seed: (default=None)  Random seed value.
        :type seed: int64

        :returns: A new Graph object representing the vertex induced subgraph.
        :rtype: dict
        """
        return None



@doc_stub
class TitanGraphMl(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """

    @doc_stub
    def belief_propagation(self, prior_property, posterior_property, edge_weight_property=None, convergence_threshold=None, max_iterations=None):
        """
        Classification on sparse data using Belief Propagation.

        Belief propagation by the sum-product algorithm.
        This algorithm analyzes a graphical model with prior beliefs using sum product message passing.
        The priors are read from a property in the graph, the posteriors are written to another property in the graph.
        This is the GraphX-based implementation of belief propagation.

        See :ref:`Loopy Belief Propagation <python_api/frames/frame-/loopy_belief_propagation>`
        for a more in-depth discussion of |BP| and |LBP|.

        Examples
        --------
        .. only:: html

            .. code::

                >>> graph.ml.belief_propagation("value", "lbp_output", string_output = True, state_space_size = 5, max_iterations = 6)

                {u'log': u'Vertex Count: 80000\nEdge Count: 318398\nAtkPregel engine has completed iteration 1  The average delta is 0.6853413553663811\nAtkPregel engine has completed iteration 2  The average delta is 0.38626944467366386\nAtkPregel engine has completed iteration 3  The average delta is 0.2365329376479823\nAtkPregel engine has completed iteration 4  The average delta is 0.14170840479478952\nAtkPregel engine has completed iteration 5  The average delta is 0.08676093923623975\n', u'time': 70.248999999999995}

                >>> graph.query.gremlin("g.V [0..4]")

                {u'results': [{u'vertex_type': u'VA', u'target': 12779523, u'lbp_output': u'0.9485759073302487, 0.001314151524421738, 0.040916996746627056, 0.001397331576080859, 0.0077956128226217315', u'_type': u'vertex', u'value': u'0.125 0.125 0.5 0.125 0.125', u'titanPhysicalId': 4, u'_id': 4}, {u'vertex_type': u'VA', u'titanPhysicalId': 8, u'lbp_output': u'0.7476996339617544, 0.0021769696832380173, 0.24559940461433935, 0.0023272253558738786, 0.002196766384794168', u'_type': u'vertex', u'value': u'0.125 0.125 0.5 0.125 0.125', u'source': 7798852, u'_id': 8}, {u'vertex_type': u'TR', u'target': 13041863, u'lbp_output': u'0.7288360734608738, 0.07162637515155296, 0.15391773902131053, 0.022620779563724287, 0.02299903280253846', u'_type': u'vertex', u'value': u'0.5 0.125 0.125 0.125 0.125', u'titanPhysicalId': 12, u'_id': 12}, {u'vertex_type': u'TR', u'titanPhysicalId': 16, u'lbp_output': u'0.9996400056392905, 9.382190989071985E-5, 8.879762476576982E-5, 8.867586165695348E-5, 8.869896439624652E-5', u'_type': u'vertex', u'value': u'0.5 0.125 0.125 0.125 0.125', u'source': 11731127, u'_id': 16}, {u'vertex_type': u'TE', u'titanPhysicalId': 20, u'lbp_output': u'0.004051247779081896, 0.2257641948616088, 0.01794622866204068, 0.7481547408142287, 0.004083587883039745', u'_type': u'vertex', u'value': u'0.125 0.125 0.5 0.125 0.125', u'source': 3408035, u'_id': 20}], u'run_time_seconds': 1.042}

        .. only:: latex

            .. code::

                >>> graph.ml.belief_propagation("value", "lbp_output", string_output = True,
                ...    state_space_size = 5, max_iterations = 6)

                {u'log': u'Vertex Count: 80000\n
                Edge Count: 318398\n
                AtkPregel engine has completed iteration 1  The average delta is 0.6853413553663811\n
                AtkPregel engine has completed iteration 2  The average delta is 0.38626944467366386\n
                AtkPregel engine has completed iteration 3  The average delta is 0.2365329376479823\n
                AtkPregel engine has completed iteration 4  The average delta is 0.14170840479478952\n
                AtkPregel engine has completed iteration 5  The average delta is 0.08676093923623975\n
                ', u'time': 70.248999999999995}

                >>> graph.query.gremlin("g.V [0..4]")

                {u'results': [{u'vertex_type':
                 u'VA',
                 u'target': 12779523,
                 u'lbp_output':
                 u'0.9485759073302487, 0.001314151524421738,
                    0.040916996746627056, 0.001397331576080859, 0.0077956128226217315',
                 u'_type':
                 u'vertex',
                 u'value':
                 u'0.125 0.125 0.5 0.125 0.125',
                 u'titanPhysicalId': 4,
                 u'_id': 4},
                {u'vertex_type':
                 u'VA',
                 u'titanPhysicalId': 8,
                 u'lbp_output':
                 u'0.7476996339617544,
                    0.0021769696832380173, 0.24559940461433935, 0.0023272253558738786,
                    0.002196766384794168',
                 u'_type':
                 u'vertex',
                 u'value':
                 u'0.125 0.125 0.5 0.125 0.125',
                 u'source': 7798852,
                 u'_id': 8},
                {u'vertex_type':
                 u'TR',
                 u'target': 13041863,
                 u'lbp_output':
                 u'0.7288360734608738, 0.07162637515155296,
                    0.15391773902131053, 0.022620779563724287, 0.02299903280253846',
                 u'_type':
                 u'vertex',
                 u'value':
                 u'0.5 0.125 0.125 0.125 0.125',
                 u'titanPhysicalId': 12,
                 u'_id': 12},
                {u'vertex_type':
                 u'TR',
                 u'titanPhysicalId': 16,
                 u'lbp_output':
                 u'0.9996400056392905,
                    9.382190989071985E-5, 8.879762476576982E-5, 8.867586165695348E-5,
                    8.869896439624652E-5',
                 u'_type':
                 u'vertex',
                 u'value':
                 u'0.5 0.125 0.125 0.125 0.125',
                 u'source': 11731127,
                 u'_id': 16},
                {u'vertex_type':
                 u'TE',
                 u'titanPhysicalId': 20,
                 u'lbp_output':
                 u'0.004051247779081896, 0.2257641948616088,
                    0.01794622866204068, 0.7481547408142287, 0.004083587883039745',
                 u'_type':
                 u'vertex',
                 u'value':
                 u'0.125 0.125 0.5 0.125 0.125',
                 u'source': 3408035,
                 u'_id': 20}],
                 u'run_time_seconds': 1.045}




        :param prior_property: Name of the vertex property which contains the prior belief
            for the vertex.
        :type prior_property: unicode
        :param posterior_property: Name of the vertex property which
            will contain the posterior belief for each
            vertex.
        :type posterior_property: unicode
        :param edge_weight_property: (default=None)  Name of the edge property that contains the edge weight for each edge.
        :type edge_weight_property: unicode
        :param convergence_threshold: (default=None)  Belief propagation will terminate
            when the average change in posterior beliefs between supersteps is
            less than or equal to this threshold.
        :type convergence_threshold: float64
        :param max_iterations: (default=None)  The maximum number of supersteps that the algorithm will execute.
            The valid range is all positive int.
        :type max_iterations: int32

        :returns: Progress report for belief propagation in the format of a multiple-line string.
        :rtype: dict
        """
        return None



@doc_stub
class TitanGraphQuery(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """

    @doc_stub
    def gremlin(self, gremlin):
        """
        Executes a Gremlin query.

        Executes a Gremlin query on an existing graph.

        Notes
        -----
        The query does not support pagination so the results of query should be limited
        using the Gremlin range filter [i..j], for example, g.V[0..9] to return the
        first 10 vertices.

        Examples
        --------
        Get the first two outgoing edges of the vertex whose source equals 5767244:

        .. code::

            >>> mygraph = ta.get_graph("mytitangraph")
            >>> results = mygraph.query.gremlin("g.V('source', 5767244).outE[0..1]")
            >>> print results["results"]

        The expected output is a list of edges in GraphSON format:

        .. only:: html

            .. code::

                [{u'_label': u'edge', u'_type': u'edge', u'_inV': 1381202500, u'weight': 1, u'_outV': 1346400004, u'_id': u'fDEQC9-1t7m96-1U'},{u'_label': u'edge', u'_type': u'edge', u'_inV': 1365600772, u'weight': 1, u'_outV': 1346400004, u'_id': u'frtzv9-1t7m96-1U'}]

        .. only:: latex

            .. code::

                [{u'_label': u'edge',
                  u'_type': u'edge',
                  u'_inV': 1381202500,
                  u'weight': 1,
                  u'_outV': 1346400004,
                  u'_id': u'fDEQC9-1t7m96-1U'},
                 {u'_label': u'edge',
                  u'_type': u'edge',
                  u'_inV': 1365600772,
                  u'weight': 1,
                  u'_outV': 1346400004,
                  u'_id': u'frtzv9-1t7m96-1U'}]

        Get the count of incoming edges for a vertex:

        .. code::

            >>> results = mygraph.query.gremlin("g.V('target', 5767243).inE.count()")
            >>> print results["results"]

        The expected output is:

        .. code::

            [4]

        Get the count of name and age properties from vertices:

        .. code::

            >>> results = mygraph.query.gremlin("g.V.transform{[it.name, it.age]}[0..10])")
            >>> print results["results"]

        The expected output is:

        .. code::

            [u'["alice", 29]', u'[ "bob", 45 ]', u'["cathy", 34 ]']



        :param gremlin: The Gremlin script to execute.

            Examples of Gremlin queries::

            g.V[0..9] - Returns the first 10 vertices in graph
            g.V.userId - Returns the userId property from vertices
            g.V('name','hercules').out('father').out('father').name - Returns the name of Hercules' grandfather
        :type gremlin: unicode

        :returns: List of query results serialized to JSON and runtime of Gremlin query in seconds.
            The list of results is in GraphSON format(for vertices or edges) or JSON (for other results like counts).
            GraphSON is a JSON-based format for property graphs which uses reserved keys
            that begin with underscores to encode vertex and edge metadata.

            Examples of valid GraphSON::

                { \"name\": \"lop\", \"lang\": \"java\",\"_id\": \"3\", \"_type\": \"vertex\" }
                { \"weight\": 1, \"_id\": \"8\", \"_type\": \"edge\", \"_outV\": \"1\", \"_inV\": \"4\", \"_label\": \"knows\" }

            See https://github.com/tinkerpop/blueprints/wiki/GraphSON-Reader-and-Writer-Library
        :rtype: dict
        """
        return None



@doc_stub
class _DocStubsVertexFrame(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, source=None, graph=None, label=None):
        """
            Examples

        --------
        Given a data file, create a frame, move the data to graph and then define a
        new VertexFrame and add data to it:

        .. only:: html

            .. code::

                >>> csv = ta.CsvFile("/movie.csv", schema= [('user_id', int32), ('user_name', str), ('movie_id', int32), ('movie_title', str), ('rating', str)])
                >>> my_frame = ta.Frame(csv)
                >>> my_graph = ta.Graph()
                >>> my_graph.define_vertex_type('users')
                >>> my_vertex_frame = my_graph.vertices['users']
                >>> my_vertex_frame.add_vertices(my_frame, 'user_id', ['user_name', 'age'])

        .. only:: html

            .. code::

                >>> csv = ta.CsvFile("/movie.csv", schema= [('user_id', int32),
                ...                                     ('user_name', str),
                ...                                     ('movie_id', int32),
                ...                                     ('movie_title', str),
                ...                                     ('rating', str)])
                >>> my_frame = ta.Frame(csv)
                >>> my_graph = ta.Graph()
                >>> my_graph.define_vertex_type('users')
                >>> my_vertex_frame = my_graph.vertices['users']
                >>> my_vertex_frame.add_vertices(my_frame, 'user_id',
                ... ['user_name', 'age'])

        Retrieve a previously defined graph and retrieve a VertexFrame from it:

        .. code::

            >>> my_graph = ta.get_graph("your_graph")
            >>> my_vertex_frame = my_graph.vertices["your_label"]

        Calling methods on a VertexFrame:

        .. code::

            >>> my_vertex_frame.vertices["your_label"].inspect(20)

        Convert a VertexFrame to a frame:

        .. code::

            >>> new_Frame = my_vertex_frame.vertices["label"].copy()
            

        :param source: (default=None)  
        :type source: 
        :param graph: (default=None)  
        :type graph: 
        :param label: (default=None)  
        :type label: 
        """
        raise DocStubCalledError("frame:vertex/__init__")


    @doc_stub
    def add_columns(self, func, schema, columns_accessed=None):
        """
        Add columns to current frame.

        Assigns data to column based on evaluating a function for each row.

        Notes
        -----
        1)  The row |UDF| ('func') must return a value in the same format as
            specified by the schema.
            See :doc:`/ds_apir`.
        2)  Unicode in column names is not supported and will likely cause the
            drop_frames() method (and others) to fail!

        Examples
        --------
        Given a Frame *my_frame* identifying a data frame with two int32
        columns *column1* and *column2*.
        Add a third column *column3* as an int32 and fill it with the
        contents of *column1* and *column2* multiplied together:

        .. code::

            >>> my_frame.add_columns(lambda row: row.column1*row.column2,
            ... ('column3', int32))

        The frame now has three columns, *column1*, *column2* and *column3*.
        The type of *column3* is an int32, and the value is the product of
        *column1* and *column2*.

        Add a string column *column4* that is empty:

        .. code::

            >>> my_frame.add_columns(lambda row: '', ('column4', str))

        The Frame object *my_frame* now has four columns *column1*, *column2*,
        *column3*, and *column4*.
        The first three columns are int32 and the fourth column is str.
        Column *column4* has an empty string ('') in every row.

        Multiple columns can be added at the same time.
        Add a column *a_times_b* and fill it with the contents of column *a*
        multiplied by the contents of column *b*.
        At the same time, add a column *a_plus_b* and fill it with the contents
        of column *a* plus the contents of column *b*:

        .. only:: html

            .. code::

                >>> my_frame.add_columns(lambda row: [row.a * row.b, row.a + row.b], [("a_times_b", float32), ("a_plus_b", float32))

        .. only:: latex

            .. code::

                >>> my_frame.add_columns(lambda row: [row.a * row.b, row.a +
                ... row.b], [("a_times_b", float32), ("a_plus_b", float32))

        Two new columns are created, "a_times_b" and "a_plus_b", with the
        appropriate contents.

        Given a frame of data and Frame *my_frame* points to it.
        In addition we have defined a |UDF| *func*.
        Run *func* on each row of the frame and put the result in a new int
        column *calculated_a*:

        .. code::

            >>> my_frame.add_columns( func, ("calculated_a", int))

        Now the frame has a column *calculated_a* which has been filled with
        the results of the |UDF| *func*.

        A |UDF| must return a value in the same format as the column is
        defined.
        In most cases this is automatically the case, but sometimes it is less
        obvious.
        Given a |UDF| *function_b* which returns a value in a list, store
        the result in a new column *calculated_b*:

        .. code::

            >>> my_frame.add_columns(function_b, ("calculated_b", float32))

        This would result in an error because function_b is returning a value
        as a single element list like [2.4], but our column is defined as a
        tuple.
        The column must be defined as a list:

        .. code::

            >>> my_frame.add_columns(function_b, [("calculated_b", float32)])

        To run an optimized version of add_columns, columns_accessed parameter can
        be populated with the column names which are being accessed in |UDF|. This
        speeds up the execution by working on only the limited feature set than the
        entire row.

        Let's say a frame has 4 columns named *a*,*b*,*c* and *d* and we want to add a new column
        with value from column *a* multiplied by value in column *b* and call it *a_times_b*.
        In the example below, columns_accessed is a list with column names *a* and *b*.

        .. code::

            >>> my_frame.add_columns(lambda row: row.a * row.b, ("a_times_b", float32), columns_accessed=["a", "b"])

        add_columns would fail if columns_accessed parameter is not populated with the correct list of accessed
        columns. If not specified, columns_accessed defaults to None which implies that all columns might be accessed
        by the |UDF|.

        More information on a row |UDF| can be found at :doc:`/ds_apir`



        :param func: User-Defined Function (|UDF|) which takes the values in the row and produces a value, or collection of values, for the new cell(s).
        :type func: UDF
        :param schema: The schema for the results of the |UDF|, indicating the new column(s) to add.  Each tuple provides the column name and data type, and is of the form (str, type).
        :type schema: tuple | list of tuples
        :param columns_accessed: (default=None)  List of columns which the |UDF| will access.  This adds significant performance benefit if we know which column(s) will be needed to execute the |UDF|, especially when the frame has significantly more columns than those being used to evaluate the |UDF|.
        :type columns_accessed: list
        """
        return None


    @doc_stub
    def add_vertices(self, source_frame, id_column_name, column_names=None):
        """
        Add vertices to a graph.

        Includes appending to a list of existing vertices.

        Examples
        --------
        .. only:: html

            .. code::

                >>> graph = ta.Graph()
                >>> graph.define_vertex_type('users')
                >>> graph.vertices['users'].add_vertices(frame, 'user_id', ['user_name', 'age'])

        .. only:: latex

            .. code::

                >>> graph = ta.Graph()
                >>> graph.define_vertex_type('users')
                >>> graph.vertices['users'].add_vertices(frame, 'user_id',
                ... ['user_name', 'age'])




        :param source_frame: Frame that will be the source of
            the vertex data.
        :type source_frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        :param id_column_name: Column name for a unique id for each vertex.
        :type id_column_name: unicode
        :param column_names: (default=None)  Column names that will be turned
            into properties for each vertex.
        :type column_names: list

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def assign_sample(self, sample_percentages, sample_labels=None, output_column=None, random_seed=None):
        """
        Randomly group rows into user-defined classes.

        Randomly assign classes to rows given a vector of percentages.
        The table receives an additional column that contains a random label.
        The random label is generated by a probability distribution function.
        The distribution function is specified by the sample_percentages, a list of
        floating point values, which add up to 1.
        The labels are non-negative integers drawn from the range
        :math:`[ 0, len(S) - 1]` where :math:`S` is the sample_percentages.

        **Notes**

        The sample percentages provided by the user are preserved to at least eight
        decimal places, but beyond this there may be small changes due to floating
        point imprecision.

        In particular:

        #)  The engine validates that the sum of probabilities sums to 1.0 within
            eight decimal places and returns an error if the sum falls outside of this
            range.
        #)  The probability of the final class is clamped so that each row receives a
            valid label with probability one.

        Examples
        --------
        Given a frame accessed via Frame *my_frame*:

        .. code::

            >>> my_frame.inspect()
              col_nc:str  col_wk:str
            /------------------------/
              abc         zzz
              def         yyy
              ghi         xxx
              jkl         www
              mno         vvv
              pqr         uuu
              stu         ttt
              vwx         sss
              yza         rrr
              bcd         qqq

        To append a new column *sample_bin* to the frame and assign the value in the
        new column to "train", "test", or "validate":

        .. code::

            >>> my_frame.assign_sample([0.3, 0.3, 0.4], ["train", "test", "validate"])
            >>> my_frame.inspect()
              col_nc:str  col_wk:str  sample_bin:str
            /----------------------------------------/
              abc         zzz         validate
              def         yyy         test
              ghi         xxx         test
              jkl         www         test
              mno         vvv         train
              pqr         uuu         validate
              stu         ttt         validate
              vwx         sss         train
              yza         rrr         validate
              bcd         qqq         train

        Now, the frame accessed by the Frame, *my_frame*, has a new column named
        "sample_bin" and each row contains one of the values "train", "test", or
        "validate".
        Values in the other columns are unaffected.



        :param sample_percentages: Entries are non-negative and sum to 1. (See the note below.)
            If the *i*'th entry of the  list is *p*,
            then then each row receives label *i* with independent probability *p*.
        :type sample_percentages: list
        :param sample_labels: (default=None)  Names to be used for the split classes.
            Defaults to "TR", "TE", "VA" when the length of *sample_percentages* is 3,
            and defaults to Sample_0, Sample_1, ... otherwise.
        :type sample_labels: list
        :param output_column: (default=None)  Name of the new column which holds the labels generated by the
            function.
        :type output_column: unicode
        :param random_seed: (default=None)  Random seed used to generate the labels.
            Defaults to 0.
        :type random_seed: int32

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def bin_column(self, column_name, cutoffs, include_lowest=None, strict_binning=None, bin_column_name=None):
        """
        Classify data into user-defined groups.

        Summarize rows of data based on the value in a single column by sorting them
        into bins, or groups, based on a list of bin cutoff points.

        **Notes**

        #)  Unicode in column names is not supported and will likely cause the
            drop_frames() method (and others) to fail!
        #)  Bins IDs are 0-index, in other words, the lowest bin number is 0.
        #)  The first and last cutoffs are always included in the bins.
            When *include_lowest* is ``True``, the last bin includes both cutoffs.
            When *include_lowest* is ``False``, the first bin (bin 0) includes both
            cutoffs.

        Examples
        --------
        For this example, we will use a frame with column *a* accessed by a Frame
        object *my_frame*:

        .. code::

            >>> my_frame.inspect( n=11 )

              a:int32
            /---------/
                1
                1
                2
                3
                5
                8
               13
               21
               34
               55
               89

        Modify the frame with a column showing what bin the data is in.
        The data values should use strict_binning:

        .. code::

            >>> my_frame.bin_column('a', [5,12,25,60], include_lowest=True,
            ... strict_binning=True, bin_column_name='binned')
            >>> my_frame.inspect( n=11 )

              a:int32     binned:int32
            /---------------------------/
                  1               -1
                  1               -1
                  2               -1
                  3               -1
                  5                0
                  8                0
                 13                1
                 21                1
                 34                2
                 55                2
                 89               -1

        Modify the frame with a column showing what bin the data is in.
        The data value should not use strict_binning:

        .. code::

            >>> my_frame.bin_column('a', [5,12,25,60], include_lowest=True,
            ... strict_binning=False, bin_column_name='binned')
            >>> my_frame.inspect( n=11 )

              a:int32     binned:int32
            /---------------------------/
                  1                0
                  1                0
                  2                0
                  3                0
                  5                0
                  8                0
                 13                1
                 21                1
                 34                2
                 55                2
                 89                2


        Modify the frame with a column showing what bin the data is in.
        The bins should be lower inclusive:

        .. code::

            >>> my_frame.bin_column('a', [1,5,34,55,89], include_lowest=True,
            ... strict_binning=False, bin_column_name='binned')
            >>> my_frame.inspect( n=11 )

              a:int32     binned:int32
            /---------------------------/
                  1                0
                  1                0
                  2                0
                  3                0
                  5                1
                  8                1
                 13                1
                 21                1
                 34                2
                 55                3
                 89                3

        Modify the frame with a column showing what bin the data is in.
        The bins should be upper inclusive:

        .. code::

            >>> my_frame.bin_column('a', [1,5,34,55,89], include_lowest=False,
            ... strict_binning=True, bin_column_name='binned')
            >>> my_frame.inspect( n=11 )

              a:int32     binned:int32
            /---------------------------/
               1                   0
               1                   0
               2                   0
               3                   0
               5                   0
               8                   1
              13                   1
              21                   1
              34                   1
              55                   2
              89                   3


        :param column_name: Name of the column to bin.
        :type column_name: unicode
        :param cutoffs: Array of values containing bin cutoff points.
            Array can be list or tuple.
            Array values must be progressively increasing.
            All bin boundaries must be included, so, with N bins, you need N+1 values.
        :type cutoffs: list
        :param include_lowest: (default=None)  Specify how the boundary conditions are handled.
            ``True`` indicates that the lower bound of the bin is inclusive.
            ``False`` indicates that the upper bound is inclusive.
            Default is ``True``.
        :type include_lowest: bool
        :param strict_binning: (default=None)  Specify how values outside of the cutoffs array should be binned.
            If set to ``True``, each value less than cutoffs[0] or greater than
            cutoffs[-1] will be assigned a bin value of -1.
            If set to ``False``, values less than cutoffs[0] will be included in the first
            bin while values greater than cutoffs[-1] will be included in the final
            bin.
        :type strict_binning: bool
        :param bin_column_name: (default=None)  The name for the new binned column.
            Default is ``<column_name>_binned``.
        :type bin_column_name: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def bin_column_equal_depth(self, column_name, num_bins=None, bin_column_name=None):
        """
        Classify column into groups with the same frequency.

        Group rows of data based on the value in a single column and add a label
        to identify grouping.

        Equal depth binning attempts to label rows such that each bin contains the
        same number of elements.
        For :math:`n` bins of a column :math:`C` of length :math:`m`, the bin
        number is determined by:

        .. math::

            \lceil n * \frac { f(C) }{ m } \rceil

        where :math:`f` is a tie-adjusted ranking function over values of
        :math:`C`.
        If there are multiples of the same value in :math:`C`, then their
        tie-adjusted rank is the average of their ordered rank values.

        **Notes**

        #)  Unicode in column names is not supported and will likely cause the
            drop_frames() method (and others) to fail!
        #)  The num_bins parameter is considered to be the maximum permissible number
            of bins because the data may dictate fewer bins.
            For example, if the column to be binned has a quantity of :math"`X`
            elements with only 2 distinct values and the *num_bins* parameter is
            greater than 2, then the actual number of bins will only be 2.
            This is due to a restriction that elements with an identical value must
            belong to the same bin.

        Examples
        --------
        Given a frame with column *a* accessed by a Frame object *my_frame*:

        .. code::

            >>> my_frame.inspect( n=11 )

              a:int32
            /---------/
                1
                1
                2
                3
                5
                8
               13
               21
               34
               55
               89

        Modify the frame, adding a column showing what bin the data is in.
        The data should be grouped into a maximum of five bins.
        Note that each bin will have the same quantity of members (as much as
        possible):

        .. code::

            >>> cutoffs = my_frame.bin_column_equal_depth('a', 5, 'aEDBinned')
            >>> my_frame.inspect( n=11 )

              a:int32     aEDBinned:int32
            /-----------------------------/
                  1                   0
                  1                   0
                  2                   1
                  3                   1
                  5                   2
                  8                   2
                 13                   3
                 21                   3
                 34                   4
                 55                   4
                 89                   4

            >>> print cutoffs
            [1.0, 2.0, 5.0, 13.0, 34.0, 89.0]


        :param column_name: The column whose values are to be binned.
        :type column_name: unicode
        :param num_bins: (default=None)  The maximum number of bins.
            Default is the Square-root choice
            :math:`\lfloor \sqrt{m} \rfloor`, where :math:`m` is the number of rows.
        :type num_bins: int32
        :param bin_column_name: (default=None)  The name for the new column holding the grouping labels.
            Default is ``<column_name>_binned``.
        :type bin_column_name: unicode

        :returns: A list containing the edges of each bin.
        :rtype: dict
        """
        return None


    @doc_stub
    def bin_column_equal_width(self, column_name, num_bins=None, bin_column_name=None):
        """
        Classify column into same-width groups.

        Group rows of data based on the value in a single column and add a label
        to identify grouping.

        Equal width binning places column values into groups such that the values
        in each group fall within the same interval and the interval width for each
        group is equal.

        **Notes**

        #)  Unicode in column names is not supported and will likely cause the
            drop_frames() method (and others) to fail!
        #)  The num_bins parameter is considered to be the maximum permissible number
            of bins because the data may dictate fewer bins.
            For example, if the column to be binned has 10
            elements with only 2 distinct values and the *num_bins* parameter is
            greater than 2, then the number of actual number of bins will only be 2.
            This is due to a restriction that elements with an identical value must
            belong to the same bin.

        Examples
        --------
        Given a frame with column *a* accessed by a Frame object *my_frame*:

        .. code::

            >>> my_frame.inspect( n=11 )

              a:int32
            /---------/
                1
                1
                2
                3
                5
                8
               13
               21
               34
               55
               89

        Modify the frame, adding a column showing what bin the data is in.
        The data should be separated into a maximum of five bins and the bin cutoffs
        should be evenly spaced.
        Note that there may be bins with no members:

        .. code::

            >>> cutoffs = my_frame.bin_column_equal_width('a', 5, 'aEWBinned')
            >>> my_frame.inspect( n=11 )

              a:int32     aEWBinned:int32
            /-----------------------------/
                1                 0
                1                 0
                2                 0
                3                 0
                5                 0
                8                 0
               13                 0
               21                 1
               34                 1
               55                 3
               89                 4

        The method returns a list of 6 cutoff values that define the edges of each bin.
        Note that difference between the cutoff values is constant:

        .. code::

            >>> print cutoffs
            [1.0, 18.6, 36.2, 53.8, 71.4, 89.0]


        :param column_name: The column whose values are to be binned.
        :type column_name: unicode
        :param num_bins: (default=None)  The maximum number of bins.
            Default is the Square-root choice
            :math:`\lfloor \sqrt{m} \rfloor`, where :math:`m` is the number of rows.
        :type num_bins: int32
        :param bin_column_name: (default=None)  The name for the new column holding the grouping labels.
            Default is ``<column_name>_binned``.
        :type bin_column_name: unicode

        :returns: A list of the edges of each bin.
        :rtype: dict
        """
        return None


    @doc_stub
    def categorical_summary(self, column_inputs=None):
        """
        Compute a summary of the data in a column(s) for categorical or numerical data types.

        The returned value is a Map containing categorical summary for each specified column.

        For each column, levels which satisfy the top k and/or threshold cutoffs are displayed along
        with their frequency and percentage occurrence with respect to the total rows in the dataset.

        Missing data is reported when a column value is empty ("") or null.

        All remaining data is grouped together in the Other category and its frequency and percentage are reported as well.

        User must specify the column name and can optionally specify top_k and/or threshold.

        Optional parameters:

            top_k
                Displays levels which are in the top k most frequently occurring values for that column.

            threshold
                Displays levels which are above the threshold percentage with respect to the total row count.

            top_k and threshold
                Performs level pruning first based on top k and then filters out levels which satisfy the threshold criterion.

            defaults
                Displays all levels which are in Top 10.


        Examples
        --------

        .. code::

            >>> frame.categorical_summary('source','target')
            >>> frame.categorical_summary(('source', {'top_k' : 2}))
            >>> frame.categorical_summary(('source', {'threshold' : 0.5}))
            >>> frame.categorical_summary(('source', {'top_k' : 2}), ('target',
            ... {'threshold' : 0.5}))

        Sample output (for last example above):

            >>> {u'categorical_summary': [{u'column': u'source', u'levels': [
            ... {u'percentage': 0.32142857142857145, u'frequency': 9, u'level': u'thing'},
            ... {u'percentage': 0.32142857142857145, u'frequency': 9, u'level': u'abstraction'},
            ... {u'percentage': 0.25, u'frequency': 7, u'level': u'physical_entity'},
            ... {u'percentage': 0.10714285714285714, u'frequency': 3, u'level': u'entity'},
            ... {u'percentage': 0.0, u'frequency': 0, u'level': u'Missing'},
            ... {u'percentage': 0.0, u'frequency': 0, u'level': u'Other'}]},
            ... {u'column': u'target', u'levels': [
            ... {u'percentage': 0.07142857142857142, u'frequency': 2, u'level': u'thing'},
            ... {u'percentage': 0.07142857142857142, u'frequency': 2,
            ...  u'level': u'physical_entity'},
            ... {u'percentage': 0.07142857142857142, u'frequency': 2, u'level': u'entity'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'variable'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'unit'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'substance'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'subject'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'set'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'reservoir'},
            ... {u'percentage': 0.03571428571428571, u'frequency': 1, u'level': u'relation'},
            ... {u'percentage': 0.0, u'frequency': 0, u'level': u'Missing'},
            ... {u'percentage': 0.5357142857142857, u'frequency': 15, u'level': u'Other'}]}]}



        :param column_inputs: (default=None)  Comma-separated column names to summarize or tuple containing column name and dictionary of optional parameters. Optional parameters (see below for details): top_k (default = 10), threshold (default = 0.0)
        :type column_inputs: str | tuple(str, dict)

        :returns: Summary for specified column(s) consisting of levels with their frequency and percentage
        :rtype: dict
        """
        return None


    @doc_stub
    def classification_metrics(self, label_column, pred_column, pos_label=None, beta=None, frequency_column=None):
        """
        Model statistics of accuracy, precision, and others.

        Calculate the accuracy, precision, confusion_matrix, recall and
        :math:`F_{ \beta}` measure for a classification model.

        *   The **f_measure** result is the :math:`F_{ \beta}` measure for a
            classification model.
            The :math:`F_{ \beta}` measure of a binary classification model is the
            harmonic mean of precision and recall.
            If we let:

            * beta :math:`\equiv \beta`,
            * :math:`T_{P}` denotes the number of true positives,
            * :math:`F_{P}` denotes the number of false positives, and
            * :math:`F_{N}` denotes the number of false negatives

            then:

            .. math::

                F_{ \beta} = (1 + \beta ^ 2) * \frac{ \frac{T_{P}}{T_{P} + F_{P}} * \
                \frac{T_{P}}{T_{P} + F_{N}}}{ \beta ^ 2 * \frac{T_{P}}{T_{P} + \
                F_{P}}  + \frac{T_{P}}{T_{P} + F_{N}}}

            The :math:`F_{ \beta}` measure for a multi-class classification model is
            computed as the weighted average of the :math:`F_{ \beta}` measure for
            each label, where the weight is the number of instances of each label.
            The determination of binary vs. multi-class is automatically inferred
            from the data.

        *   The **recall** result of a binary classification model is the proportion
            of positive instances that are correctly identified.
            If we let :math:`T_{P}` denote the number of true positives and
            :math:`F_{N}` denote the number of false negatives, then the model
            recall is given by :math:`\frac {T_{P}} {T_{P} + F_{N}}`.

            For multi-class classification models, the recall measure is computed as
            the weighted average of the recall for each label, where the weight is
            the number of instances of each label.
            The determination of binary vs. multi-class is automatically inferred
            from the data.

        *   The **precision** of a binary classification model is the proportion of
            predicted positive instances that are correctly identified.
            If we let :math:`T_{P}` denote the number of true positives and
            :math:`F_{P}` denote the number of false positives, then the model
            precision is given by: :math:`\frac {T_{P}} {T_{P} + F_{P}}`.

            For multi-class classification models, the precision measure is computed
            as the weighted average of the precision for each label, where the
            weight is the number of instances of each label.
            The determination of binary vs. multi-class is automatically inferred
            from the data.

        *   The **accuracy** of a classification model is the proportion of
            predictions that are correctly identified.
            If we let :math:`T_{P}` denote the number of true positives,
            :math:`T_{N}` denote the number of true negatives, and :math:`K` denote
            the total number of classified instances, then the model accuracy is
            given by: :math:`\frac{T_{P} + T_{N}}{K}`.

            This measure applies to binary and multi-class classifiers.

        *   The **confusion_matrix** result is a confusion matrix for a
            binary classifier model, formatted for human readability.

        Notes
        -----
        The **confusion_matrix** is not yet implemented for multi-class classifiers.

        Examples
        --------
        Consider the following sample data set in *frame* with actual data
        labels specified in the *labels* column and the predicted labels in the
        *predictions* column:

        .. code::

            >>> frame.inspect()

              a:unicode   b:int32   labels:int32  predictions:int32
            /-------------------------------------------------------/
                red         1              0                  0
                blue        3              1                  0
                blue        1              0                  0
                green       0              1                  1

            >>> cm = frame.classification_metrics(label_column='labels',
            ... pred_column='predictions', pos_label=1, beta=1)

            >>> cm.f_measure

            0.66666666666666663

            >>> cm.recall

            0.5

            >>> cm.accuracy

            0.75

            >>> cm.precision

            1.0

            >>> cm.confusion_matrix

                          Predicted
                         _pos_ _neg__
            Actual  pos |  1     1
                    neg |  0     2



        :param label_column: The name of the column containing the
            correct label for each instance.
        :type label_column: unicode
        :param pred_column: The name of the column containing the
            predicted label for each instance.
        :type pred_column: unicode
        :param pos_label: (default=None)  
        :type pos_label: None
        :param beta: (default=None)  This is the beta value to use for
            :math:`F_{ \beta}` measure (default F1 measure is computed); must be greater than zero.
            Defaults is 1.
        :type beta: float64
        :param frequency_column: (default=None)  The name of an optional column containing the
            frequency of observations.
        :type frequency_column: unicode

        :returns: The data returned is composed of multiple components\:

            |   <object>.accuracy : double
            |   <object>.confusion_matrix : table
            |   <object>.f_measure : double
            |   <object>.precision : double
            |   <object>.recall : double
        :rtype: dict
        """
        return None


    @doc_stub
    def column_median(self, data_column, weights_column=None):
        """
        Calculate the (weighted) median of a column.

        The median is the least value X in the range of the distribution so that
        the cumulative weight of values strictly below X is strictly less than half
        of the total weight and the cumulative weight of values up to and including X
        is greater than or equal to one-half of the total weight.

        All data elements of weight less than or equal to 0 are excluded from the
        calculation, as are all data elements whose weight is NaN or infinite.
        If a weight column is provided and no weights are finite numbers greater
        than 0, None is returned.

        Examples
        --------
        .. code::

            >>> median = frame.column_median('middling column')


        :param data_column: The column whose median is to be calculated.
        :type data_column: unicode
        :param weights_column: (default=None)  The column that provides weights (frequencies)
            for the median calculation.
            Must contain numerical data.
            Default is all items have a weight of 1.
        :type weights_column: unicode

        :returns: varies
                The median of the values.
                If a weight column is provided and no weights are finite numbers greater
                than 0, None is returned.
                The type of the median returned is the same as the contents of the data
                column, so a column of Longs will result in a Long median and a column of
                Floats will result in a Float median.
        :rtype: dict
        """
        return None


    @doc_stub
    def column_mode(self, data_column, weights_column=None, max_modes_returned=None):
        """
        Evaluate the weights assigned to rows.

        Calculate the modes of a column.
        A mode is a data element of maximum weight.
        All data elements of weight less than or equal to 0 are excluded from the
        calculation, as are all data elements whose weight is NaN or infinite.
        If there are no data elements of finite weight greater than 0,
        no mode is returned.

        Because data distributions often have multiple modes, it is possible for a
        set of modes to be returned.
        By default, only one is returned, but by setting the optional parameter
        max_modes_returned, a larger number of modes can be returned.

        Examples
        --------
        .. code::

            >>> mode = frame.column_mode('modum columpne')


        :param data_column: Name of the column supplying the data.
        :type data_column: unicode
        :param weights_column: (default=None)  Name of the column supplying the weights.
            Default is all items have weight of 1.
        :type weights_column: unicode
        :param max_modes_returned: (default=None)  Maximum number of modes returned.
            Default is 1.
        :type max_modes_returned: int32

        :returns: Dictionary containing summary statistics.
                The data returned is composed of multiple components\:

            mode : A mode is a data element of maximum net weight.
                A set of modes is returned.
                The empty set is returned when the sum of the weights is 0.
                If the number of modes is less than or equal to the parameter
                max_modes_returned, then all modes of the data are
                returned.
                If the number of modes is greater than the max_modes_returned
                parameter, only the first max_modes_returned many modes (per a
                canonical ordering) are returned.
            weight_of_mode : Weight of a mode.
                If there are no data elements of finite weight greater than 0,
                the weight of the mode is 0.
                If no weights column is given, this is the number of appearances
                of each mode.
            total_weight : Sum of all weights in the weight column.
                This is the row count if no weights are given.
                If no weights column is given, this is the number of rows in
                the table with non-zero weight.
            mode_count : The number of distinct modes in the data.
                In the case that the data is very multimodal, this number may
                exceed max_modes_returned.


        :rtype: dict
        """
        return None


    @property
    @doc_stub
    def column_names(self):
        """
        Column identifications in the current frame.

        Returns the names of the columns of the current frame.

        Examples
        --------
        Given a Frame object, *my_frame* accessing a frame.
        To get the column names:

        .. code::

            >>> my_columns = my_frame.column_names
            >>> print my_columns

        Now, given there are three columns *col1*,
        *col2*, and *col3*, the result is:

        .. code::

            ["col1", "col2", "col3"]





        :returns: list of names of all the frame's columns
        :rtype: list
        """
        return None


    @doc_stub
    def column_summary_statistics(self, data_column, weights_column=None, use_population_variance=None):
        """
        Calculate multiple statistics for a column.

        Notes
        -----
        Sample Variance
            Sample Variance is computed by the following formula:

            .. math::

                \left( \frac{1}{W - 1} \right) * sum_{i} \
                \left(x_{i} - M \right) ^{2}

            where :math:`W` is sum of weights over valid elements of positive
            weight, and :math:`M` is the weighted mean.

        Population Variance
            Population Variance is computed by the following formula:

            .. math::

                \left( \frac{1}{W} \right) * sum_{i} \
                \left(x_{i} - M \right) ^{2}

            where :math:`W` is sum of weights over valid elements of positive
            weight, and :math:`M` is the weighted mean.

        Standard Deviation
            The square root of the variance.

        Logging Invalid Data
            A row is bad when it contains a NaN or infinite value in either
            its data or weights column.
            In this case, it contributes to bad_row_count; otherwise it
            contributes to good row count.

            A good row can be skipped because the value in its weight
            column is less than or equal to 0.
            In this case, it contributes to non_positive_weight_count, otherwise
            (when the weight is greater than 0) it contributes to
            valid_data_weight_pair_count.

        **Equations**

            .. code::

                bad_row_count + good_row_count = # rows in the frame
                positive_weight_count + non_positive_weight_count = good_row_count

            In particular, when no weights column is provided and all weights are 1.0:

            .. code::

                non_positive_weight_count = 0 and
                positive_weight_count = good_row_count

        Examples
        --------
        .. code::

            >>> stats = frame.column_summary_statistics('data column', 'weight column')



        :param data_column: The column to be statistically summarized.
            Must contain numerical data; all NaNs and infinite values are excluded
            from the calculation.
        :type data_column: unicode
        :param weights_column: (default=None)  Name of column holding weights of
            column values.
        :type weights_column: unicode
        :param use_population_variance: (default=None)  If true, the variance is calculated
            as the population variance.
            If false, the variance calculated as the sample variance.
            Because this option affects the variance, it affects the standard
            deviation and the confidence intervals as well.
            Default is false.
        :type use_population_variance: bool

        :returns: Dictionary containing summary statistics.
            The data returned is composed of multiple components\:

            |   mean : [ double | None ]
            |       Arithmetic mean of the data.
            |   geometric_mean : [ double | None ]
            |       Geometric mean of the data. None when there is a data element <= 0, 1.0 when there are no data elements.
            |   variance : [ double | None ]
            |       None when there are <= 1 many data elements. Sample variance is the weighted sum of the squared distance of each data element from the weighted mean, divided by the total weight minus 1. None when the sum of the weights is <= 1. Population variance is the weighted sum of the squared distance of each data element from the weighted mean, divided by the total weight.
            |   standard_deviation : [ double | None ]
            |       The square root of the variance. None when  sample variance is being used and the sum of weights is <= 1.
            |   total_weight : long
            |       The count of all data elements that are finite numbers. In other words, after excluding NaNs and infinite values.
            |   minimum : [ double | None ]
            |       Minimum value in the data. None when there are no data elements.
            |   maximum : [ double | None ]
            |       Maximum value in the data. None when there are no data elements.
            |   mean_confidence_lower : [ double | None ]
            |       Lower limit of the 95% confidence interval about the mean. Assumes a Gaussian distribution. None when there are no elements of positive weight.
            |   mean_confidence_upper : [ double | None ]
            |       Upper limit of the 95% confidence interval about the mean. Assumes a Gaussian distribution. None when there are no elements of positive weight.
            |   bad_row_count : [ double | None ]
            |       The number of rows containing a NaN or infinite value in either the data or weights column.
            |   good_row_count : [ double | None ]
            |       The number of rows not containing a NaN or infinite value in either the data or weights column.
            |   positive_weight_count : [ double | None ]
            |       The number of valid data elements with weight > 0. This is the number of entries used in the statistical calculation.
            |   non_positive_weight_count : [ double | None ]
            |       The number valid data elements with finite weight <= 0.
        :rtype: dict
        """
        return None


    @doc_stub
    def compute_misplaced_score(self, gravity):
        """


        :param gravity: Similarity measure for computing tension between 2 connected items
        :type gravity: float64

        :returns: 
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def copy(self, columns=None, where=None, name=None):
        """
        Create new frame from current frame.

        Copy frame or certain frame columns entirely or filtered.
        Useful for frame query.

        Examples
        --------
        Build a Frame from a csv file with 5 million rows of data; call the
        frame "cust":

        .. code::

            >>> my_frame = ta.Frame(source="my_data.csv")
            >>> my_frame.name("cust")

        Given the frame has columns *id*, *name*, *hair*, and *shoe*.
        Copy it to a new frame:

        .. code::

            >>> your_frame = my_frame.copy()

        Now we have two frames of data, each with 5 million rows.
        Checking the names:

        .. code::

            >>> print my_frame.name()
            >>> print your_frame.name()

        Gives the results:

        .. code::

            "cust"
            "frame_75401b7435d7132f5470ba35..."

        Now, let's copy *some* of the columns from the original frame:

        .. code::

            >>> our_frame = my_frame.copy(['id', 'hair'])

        Our new frame now has two columns, *id* and *hair*, and has 5 million
        rows.
        Let's try that again, but this time change the name of the *hair*
        column to *color*:

        .. code::

            >>> last_frame = my_frame.copy(('id': 'id', 'hair': 'color'))



        :param columns: (default=None)  If not None, the copy will only include the columns specified. If dict, the string pairs represent a column renaming, {source_column_name: destination_column_name}
        :type columns: str | list of str | dict
        :param where: (default=None)  If not None, only those rows for which the UDF evaluates to True will be copied.
        :type where: function
        :param name: (default=None)  Name of the copied frame
        :type name: str

        :returns: A new Frame of the copied data.
        :rtype: Frame
        """
        return None


    @doc_stub
    def correlation(self, data_column_names):
        """
        Calculate correlation for two columns of current frame.

        Notes
        -----
        This method applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame*, which contains the data

        .. code::

            >>> my_frame.inspect()

             idnum:int32   x1:float32   x2:float32   x3:float32   x4:float32  
           /-------------------------------------------------------------------/
                       0          1.0          4.0          0.0         -1.0  
                       1          2.0          3.0          0.0         -1.0  
                       2          3.0          2.0          1.0         -1.0  
                       3          4.0          1.0          2.0         -1.0  
                       4          5.0          0.0          2.0         -1.0  

        my_frame.correlation computes the common correlation coefficient (Pearson's) on the pair
        of columns provided.
        In this example, the *idnum* and most of the columns have trivial correlations: -1, 0, or +1.
        Column *x3* provides a contrasting coefficient of 3 / sqrt(3) = 0.948683298051 .

        .. code::

            >>> my_frame.correlation(["x1", "x2"])
               -1.0
            >>> my_frame.correlation(["x1", "x4"])
                0.0
            >>> my_frame.correlation(["x2", "x3"])
                -0.948683298051


        :param data_column_names: The names of 2 columns from which
            to compute the correlation.
        :type data_column_names: list

        :returns: Pearson correlation coefficient of the two columns.
        :rtype: dict
        """
        return None


    @doc_stub
    def correlation_matrix(self, data_column_names, matrix_name=None):
        """
        Calculate correlation matrix for two or more columns.

        Notes
        -----
        This method applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame*, which contains the data

        .. code::

            >>> my_frame.inspect()

             idnum:int32   x1:float32   x2:float32   x3:float32   x4:float32  
           /-------------------------------------------------------------------/
                       0          1.0          4.0          0.0         -1.0  
                       1          2.0          3.0          0.0         -1.0  
                       2          3.0          2.0          1.0         -1.0  
                       3          4.0          1.0          2.0         -1.0  
                       4          5.0          0.0          2.0         -1.0  

        my_frame.correlation_matrix computes the common correlation coefficient (Pearson's) on each pair
        of columns in the user-provided list.
        In this example, the *idnum* and most of the columns have trivial correlations: -1, 0, or +1.
        Column *x3* provides a contrasting coefficient of 3 / sqrt(3) = 0.948683298051 .
        The resulting table (specifying all columns) is

        .. code::

            >>> corr_matrix = my_frame.correlation_matrix(my_frame.column_names)
            >>> corr_matrix.inspect()

              idnum:float64       x1:float64        x2:float64        x3:float64   x4:float64  
           ------------------------------------------------------------------------------------
                        1.0              1.0              -1.0    0.948683298051          0.0  
                        1.0              1.0              -1.0    0.948683298051          0.0  
                       -1.0             -1.0               1.0   -0.948683298051          0.0  
             0.948683298051   0.948683298051   -0.948683298051               1.0          0.0  
                        0.0              0.0               0.0               0.0          1.0  



        :param data_column_names: The names of the columns from
            which to compute the matrix.
        :type data_column_names: list
        :param matrix_name: (default=None)  The name for the returned
            matrix Frame.
        :type matrix_name: unicode

        :returns: A Frame with the matrix of the correlation values for the columns.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def count(self, where):
        """
        Counts the number of rows which meet given criteria.

        :param where: |UDF| which evaluates a row to a boolean
        :type where: function

        :returns: number of rows for which the where |UDF| evaluated to True.
        :rtype: int
        """
        return None


    @doc_stub
    def covariance(self, data_column_names):
        """
        Calculate covariance for exactly two columns.

        Notes
        -----
        This method applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column named *obs*:

        .. code::

            >>> cov = my_frame.covariance(['col_0', 'col_1'])
            >>> print(cov)



        :param data_column_names: The names of two columns from which
            to compute the covariance.
        :type data_column_names: list

        :returns: Covariance of the two columns.
        :rtype: dict
        """
        return None


    @doc_stub
    def covariance_matrix(self, data_column_names, matrix_name=None):
        """
        Calculate covariance matrix for two or more columns.

        Notes
        -----
        This function applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame1*, which computes the covariance matrix for three
        numeric columns:

        .. code::

            >>> my_frame1.inspect()

              col_0:int64    col_1:int64   col_3:float64
            \--------------------------------------------\
                1            4             33.4
                2            5             43.7
                3            6             20.1

            >>> cov_matrix = my_frame1.covariance_matrix(['col_0', 'col_1', 'col_2'])
            >>> cov_matrix.inspect()

              col_0:float64    col_1:float64   col_3:float64
            \------------------------------------------------\
                 1.00             1.00            -6.65
                 1.00             1.00            -6.65
                 -6.65           -6.65            139.99

        Consider Frame *my_frame2*, which computes the covariance matrix for a single
        vector column:

        .. code::

            >>> my_frame2.inspect()

              State:unicode             Population_HISTOGRAM:vector
            \-------------------------------------------------------\
                Louisiana               [0.0, 1.0, 0.0, 0.0]
                Georgia                 [0.0, 1.0, 0.0, 0.0]
                Texas                   [0.0, 0.54, 0.46, 0.0]
                Florida                 [0.0, 0.83, 0.17, 0.0]

            >>> cov_matrix = my_frame2.covariance_matrix(['Population_HISTOGRAM'])
            >>> cov_matrix.inspect()

              Population_HISTOGRAM:vector
            \-------------------------------------\
              [0,  0.00000000,  0.00000000,    0]
              [0,  0.04709167, -0.04709167,    0]
              [0, -0.04709167,  0.04709167,    0]
              [0,  0.00000000,  0.00000000,    0]




        :param data_column_names: The names of the column from which to compute the matrix.
            Names should refer to a single column of type vector, or two or more
            columns of numeric scalars.
        :type data_column_names: list
        :param matrix_name: (default=None)  The name of the new
            matrix.
        :type matrix_name: unicode

        :returns: A matrix with the covariance values for the columns.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def cumulative_percent(self, sample_col):
        """
        Add column to frame with cumulative percent sum.

        A cumulative percent sum is computed by sequentially stepping through the
        rows, observing the column values and keeping track of the current percentage of the total sum
        accounted for at the current value.


        Notes
        -----
        This method applies only to columns containing numerical data.
        Although this method will execute for columns containing negative
        values, the interpretation of the result will change (for example,
        negative percentages).

        Examples
        --------
        Consider Frame *my_frame* accessing a frame that contains a single
        column named *obs*:

        .. code::

            >>> my_frame.inspect()

              obs:int32
            /-----------/
                 0
                 1
                 2
                 0
                 1
                 2

        The cumulative percent sum for column *obs* is obtained by:

        .. code::

            >>> my_frame.cumulative_percent('obs')

        The Frame *my_frame* now contains two columns *obs* and
        *obsCumulativePercentSum*.
        They contain the original data and the cumulative percent sum,
        respectively:

        .. code::

            >>> my_frame.inspect()

              obs:int32   obs_cumulative_percent:float64
            /--------------------------------------------/
                 0                             0.0
                 1                             0.16666666
                 2                             0.5
                 0                             0.5
                 1                             0.66666666
                 2                             1.0



        :param sample_col: The name of the column from which to compute
            the cumulative percent sum.
        :type sample_col: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def cumulative_sum(self, sample_col):
        """
        Add column to frame with cumulative percent sum.

        A cumulative sum is computed by sequentially stepping through the rows,
        observing the column values and keeping track of the cumulative sum for each value.

        Notes
        -----
        This method applies only to columns containing numerical data.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column named *obs*:

        .. code::

             >>> my_frame.inspect()

               obs:int32
             /-----------/
                  0
                  1
                  2
                  0
                  1
                  2

        The cumulative sum for column *obs* is obtained by:

        .. code::

            >>> my_frame.cumulative_sum('obs')

        The Frame *my_frame* accesses the original frame that now contains two
        columns, *obs* that contains the original column values, and
        *obsCumulativeSum* that contains the cumulative percent count:

        .. code::

            >>> my_frame.inspect()

              obs:int32   obs_cumulative_sum:int32
            /--------------------------------------/
                 0                          0
                 1                          1
                 2                          3
                 0                          3
                 1                          4
                 2                          6



        :param sample_col: The name of the column from which to compute
            the cumulative sum.
        :type sample_col: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def dot_product(self, left_column_names, right_column_names, dot_product_column_name, default_left_values=None, default_right_values=None):
        """
        Calculate dot product for each row in current frame.

        Calculate the dot product for each row in a frame using values from two
        equal-length sequences of columns.

        Dot product is computed by the following formula:

        The dot product of two vectors :math:`A=[a_1, a_2, ..., a_n]` and
        :math:`B =[b_1, b_2, ..., b_n]` is :math:`a_1*b_1 + a_2*b_2 + ...+ a_n*b_n`.
        The dot product for each row is stored in a new column in the existing frame.

        Notes
        -----
        If default_left_values or default_right_values are not specified, any null
        values will be replaced by zeros.

        Examples
        --------
        Calculate the dot product for a sequence of columns in Frame object *my_frame*:

        .. code::

             >>> my_frame.inspect()

               col_0:int32  col_1:float64  col_2:int32  col3:int32
             /-----------------------------------------------------/
               1            0.2            -2           5
               2            0.4            -1           6
               3            0.6             0           7
               4            0.8             1           8
               5            None            2           None

        Modify the frame by computing the dot product for a sequence of columns:

        .. code::

             >>> my_frame.dot_product(['col_0','col_1'], ['col_2', 'col_3'], 'dot_product')
             >>> my_frame.inspect()

               col_0:int32  col_1:float64 col_2:int32 col3:int32  dot_product:float64
             /------------------------------------------------------------------------/
               1            0.2           -2          5            -1.0
               2            0.4           -1          6             0.4
               3            0.6            0          7             4.2
               4            0.8            1          8            10.4
               5            None           2          None         10.0

        Modify the frame by computing the dot product with default values for nulls:

        .. only:: html

            .. code::

                 >>> my_frame.dot_product(['col_0','col_1'], ['col_2', 'col_3'], 'dot_product_2', [0.1, 0.2], [0.3, 0.4])
                 >>> my_frame.inspect()

                   col_0:int32  col_1:float64 col_2:int32 col3:int32  dot_product:float64  dot_product_2:float64
                 /--------------------------------------------------------------------------------------------/
                    1            0.2           -2          5            -1.0               -1.0
                    2            0.4           -1          6             0.4                0.4
                    3            0.6            0          7             4.2                4.2
                    4            0.8            1          8            10.4                10.4
                    5            None           2          None         10.0                10.08

        .. only:: latex

            .. code::

                 >>> my_frame.dot_product(['col_0','col_1'], ['col_2', 'col_3'],
                 ... 'dot_product_2', [0.1, 0.2], [0.3, 0.4])
                 >>> my_frame.inspect()

                   col_0  col_1    col_2  col3   dot_product  dot_product_2
                   int32  float64  int32  int32  float64      float64
                 /----------------------------------------------------------/
                    1     0.2      -2     5         -1.0         -1.0
                    2     0.4      -1     6          0.4          0.4
                    3     0.6       0     7          4.2          4.2
                    4     0.8       1     8         10.4          10.4
                    5     None      2     None      10.0          10.08

        Calculate the dot product for columns of vectors in Frame object *my_frame*:

        .. code::

             >>> my_frame.dot_product('col_4', 'col_5, 'dot_product')

             col_4:vector  col_5:vector  dot_product:float64
             /----------------------------------------------/
              [1, 0.2]     [-2, 5]       -1.0
              [2, 0.4]     [-1, 6]        0.4
              [3, 0.6]     [0,  7]        4.2
              [4, 0.8]     [1,  8]       10.4


        :param left_column_names: Names of columns used to create the left vector (A) for each row.
            Names should refer to a single column of type vector, or two or more
            columns of numeric scalars.
        :type left_column_names: list
        :param right_column_names: Names of columns used to create right vector (B) for each row.
            Names should refer to a single column of type vector, or two or more
            columns of numeric scalars.
        :type right_column_names: list
        :param dot_product_column_name: Name of column used to store the
            dot product.
        :type dot_product_column_name: unicode
        :param default_left_values: (default=None)  Default values used to substitute null values in left vector.
            Default is None.
        :type default_left_values: list
        :param default_right_values: (default=None)  Default values used to substitute null values in right vector.
            Default is None.
        :type default_right_values: list

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def download(self, n=100, offset=0, columns=None):
        """
        Download a frame from the server into client workspace.

        Copies an trustedanalytics Frame into a Pandas DataFrame.


        Examples
        --------
        Frame *my_frame* accesses a frame with millions of rows of data.
        Get a sample of 500 rows:

        .. code::

            >>> pandas_frame = my_frame.download( 500 )

        We now have a new frame accessed by a pandas DataFrame *pandas_frame*
        with a copy of the first 500 rows of the original frame.

        If we use the method with an offset like:

        .. code::

            >>> pandas_frame = my_frame.take( 500, 100 )

        We end up with a new frame accessed by the pandas DataFrame
        *pandas_frame* again, but this time it has a copy of rows 101 to 600 of
        the original frame.



        :param n: (default=100)  The number of rows to download to the client
        :type n: int
        :param offset: (default=0)  The number of rows to skip before copying
        :type offset: int
        :param columns: (default=None)  Column filter, the names of columns to be included (default is all columns)
        :type columns: list

        :returns: A new pandas dataframe object containing the downloaded frame data
        :rtype: pandas.DataFrame
        """
        return None


    @doc_stub
    def drop_columns(self, columns):
        """
        Remove columns from the frame.

        The data from the columns is lost.

        Notes
        -----
        It is not possible to delete all columns from a frame.
        At least one column needs to remain.
        If it is necessary to delete all columns, then delete the frame.

        Examples
        --------
        For this example, Frame object *my_frame* accesses a frame with
        columns *column_a*, *column_b*, *column_c* and *column_d*.

        .. only:: html

            .. code::

                >>> print my_frame.schema
                [("column_a", str), ("column_b", ta.int32), ("column_c", str), ("column_d", ta.int32)]

        .. only:: latex

            .. code::

                >>> print my_frame.schema
                [("column_a", str), ("column_b", ta.int32), ("column_c", str),
                ("column_d", ta.int32)]

        Eliminate columns *column_b* and *column_d*:

        .. code::

            >>> my_frame.drop_columns(["column_b", "column_d"])
            >>> print my_frame.schema
            [("column_a", str), ("column_c", str)]


        Now the frame only has the columns *column_a* and *column_c*.
        For further examples, see: ref:`example_frame.drop_columns`.




        :param columns: Column name OR list of column names to be removed from the frame.
        :type columns: list

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def drop_duplicates(self, unique_columns=None):
        """
        Remove duplicate vertex rows.

        Remove duplicate vertex rows, keeping only one vertex row per uniqueness
        criteria match.
        Edges that were connected to removed vertices are also automatically dropped.

        Examples
        --------
        Remove any rows that have the same data in column *b* as a previously
        checked row:

        .. code::

            >>> my_frame.drop_duplicates("b")

        The result is a frame with unique values in column *b*.

        Remove any rows that have the same data in columns *a* and *b* as a
        previously checked row:

        .. code::

            >>> my_frame.drop_duplicates([ "a", "b"] )

        The result is a frame with unique values for the combination of columns
        *a* and *b*.

        Remove any rows that have the whole row identical:

        .. code::

            >>> my_frame.drop_duplicates()

        The result is a frame where something is different in every row from every
        other row.
        Each row is unique.



        :param unique_columns: (default=None)  
        :type unique_columns: None

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def drop_rows(self, predicate):
        """
        Erase any row in the current frame which qualifies.

        Examples
        --------
        For this example, my_frame is a Frame object accessing a frame with
        lots of data for the attributes of ``lions``, ``tigers``, and
        ``ligers``.
        Get rid of the ``lions`` and ``tigers``:

        .. code::

            >>> my_frame.drop_rows(lambda row: row.animal_type == "lion" or
            ...    row.animal_type == "tiger")

        Now the frame only has information about ``ligers``.

        More information on a |UDF| can be found at :doc:`/ds_apir`.




        :param predicate: |UDF| which evaluates a row to a boolean; rows that answer True are dropped from the Frame
        :type predicate: function
        """
        return None


    @doc_stub
    def drop_vertices(self, predicate):
        """
        Delete rows that qualify.

        Parameters
        ----------
        predicate : |UDF|
            |UDF| or lambda which takes a row argument and evaluates
            to a boolean value.

        Examples
        --------
        Given VertexFrame object *my_vertex_frame* accessing a graph with lots
        of data for the attributes of ``lions``, ``tigers``, and ``ligers``.
        Get rid of the ``lions`` and ``tigers``:

        .. only:: html

            .. code::

                >>> my_vertex_frame.drop_vertices(lambda row: row.animal_type == "lion" or row.animal_type == "tiger")

        .. only:: latex

            .. code::

                >>> my_vertex_frame.drop_vertices(lambda row:
                ...     row.animal_type == "lion" or
                ...     row.animal_type == "tiger")

        Now the frame only has information about ``ligers``.

        More information on |UDF| can be found at :doc:`/ds_apir`



        :param predicate: |UDF| which evaluates a row (vertex) to a boolean; vertices that answer True are dropped from the Frame
        :type predicate: function
        """
        return None


    @doc_stub
    def ecdf(self, column, result_frame_name=None):
        """
        Builds new frame with columns for data and distribution.

        Generates the empirical cumulative distribution for the input column.

        Examples
        --------
        Consider the following sample data set in *frame* with actual data labels
        specified in the *labels* column and the predicted labels in the
        *predictions* column:

        .. code::

            >>> import trustedanalytics as ta
            >>> import pandas as p
            >>> f = ta.Frame(ta.Pandas(p.DataFrame([1, 3, 1, 0]), [('numbers', ta.int32)]))

            [==Job Progress...]

            >>> f.take(5)
            [[1], [3], [1], [0]]

            [==Job Progress...]

            >>> result = f.ecdf('numbers')
            >>> result.inspect()

              b:int32   b_ECDF:float64
            /--------------------------/
               1             0.2
               2             0.5
               3             0.8
               4             1.0



        :param column: The name of the input column containing sample.
        :type column: unicode
        :param result_frame_name: (default=None)  A name for the resulting frame which is created
            by this operation.
        :type result_frame_name: unicode

        :returns: A new Frame containing each distinct value in the sample and its corresponding ECDF value.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def entropy(self, data_column, weights_column=None):
        """
        Calculate the Shannon entropy of a column.

        The data column is weighted via the weights column.
        All data elements of weight <= 0 are excluded from the calculation, as are
        all data elements whose weight is NaN or infinite.
        If there are no data elements with a finite weight greater than 0,
        the entropy is zero.

        Examples
        --------
        Given a frame of coin flips, half heads and half tails, the entropy is simply ln(2):
        .. code::

            >>> print frame.inspect()

                      data:unicode  
                    /----------------/
                      H             
                      T             
                      H             
                      T             
                      H             
                      T             
                      H             
                      T             
                      H             
                      T             

            >>> print "Computed entropy:", frame.entropy("data")

                    Computed entropy: 0.69314718056

        If we have more choices and weights, the computation is not as simple.
        An on-line search for "Shannon Entropy" will provide more detail.

        .. code::

           >>> print frame.inspect()
                      data:int32   weight:int32  
                    -----------------------------
                               0              1  
                               1              2  
                               2              4  
                               4              8  

           >>> print "Computed entropy:", frame.entropy("data", "weight")

                    Computed entropy: 1.13691659183



        :param data_column: The column whose entropy is to be calculated.
        :type data_column: unicode
        :param weights_column: (default=None)  The column that provides weights (frequencies) for the entropy calculation.
            Must contain numerical data.
            Default is using uniform weights of 1 for all items.
        :type weights_column: unicode

        :returns: Entropy.
        :rtype: dict
        """
        return None


    @doc_stub
    def export_to_csv(self, folder_name, separator=None, count=None, offset=None):
        """
        Write current frame to HDFS in csv format.

        Export the frame to a file in csv format as a Hadoop file.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_csv('covarianceresults')



        :param folder_name: The HDFS folder path where the files
            will be created.
        :type folder_name: unicode
        :param separator: (default=None)  
        :type separator: None
        :param count: (default=None)  The number of records you want.
            Default, or a non-positive value, is the whole frame.
        :type count: int32
        :param offset: (default=None)  The number of rows to skip before exporting to the file.
            Default is zero (0).
        :type offset: int32

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def export_to_hbase(self, table_name, key_column_name=None, family_name=None):
        """
        Write current frame to HBase table.

        Table must exist in HBase.
        Export of Vectors is not currently supported.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_hbase('covarianceresults')



        :param table_name: The name of the HBase table that will contain the exported frame
        :type table_name: unicode
        :param key_column_name: (default=None)  The name of the column to be used as row key in hbase table
        :type key_column_name: unicode
        :param family_name: (default=None)  The family name of the HBase table that will contain the exported frame
        :type family_name: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def export_to_hive(self, table_name):
        """
        Write current frame to Hive table.

        Table must not exist in Hive.
        Export of Vectors is not currently supported.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_hive('covarianceresults')

        :param table_name: The name of the Hive table that will contain the exported frame
        :type table_name: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def export_to_jdbc(self, table_name, connector_type=None, url=None, driver_name=None, query=None):
        """
        Write current frame to JDBC table.

        Table will be created or appended to.
        Export of Vectors is not currently supported.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_jdbc('covarianceresults')



        :param table_name: JDBC table name
        :type table_name: unicode
        :param connector_type: (default=None)  (optional) JDBC connector type
        :type connector_type: unicode
        :param url: (default=None)  (optional) connection url (includes server name, database name, user acct and password
        :type url: unicode
        :param driver_name: (default=None)  (optional) driver name
        :type driver_name: unicode
        :param query: (default=None)  (optional) query for filtering. Not supported yet.
        :type query: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def export_to_json(self, folder_name, count=None, offset=None):
        """
        Write current frame to HDFS in JSON format.

        Export the frame to a file in JSON format as a Hadoop file.

        Examples
        --------
        Consider Frame *my_frame*:

        .. code::

            >>> my_frame.export_to_json('covarianceresults')



        :param folder_name: The HDFS folder path where the files
            will be created.
        :type folder_name: unicode
        :param count: (default=None)  The number of records you want.
            Default, or a non-positive value, is the whole frame.
        :type count: int32
        :param offset: (default=None)  The number of rows to skip before exporting to the file.
            Default is zero (0).
        :type offset: int32

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def filter(self, predicate):
        """
        <Missing Doc>

        :param predicate: |UDF| which evaluates a row to a boolean; vertices that answer False are dropped from the Frame
        :type predicate: function
        """
        return None


    @doc_stub
    def flatten_column(self, column, delimiter=None):
        """
        Spread data to multiple rows based on cell data.

        Splits cells in the specified column into multiple rows according to a string
        delimiter.
        New rows are a full copy of the original row, but the specified column only
        contains one value.
        The original row is deleted.

        Examples
        --------
        Given a data file::

            1-"solo,mono,single"
            2-"duo,double"

        The commands to bring the data into a frame, where it can be worked on:

        .. only:: html

            .. code::

                >>> my_csv = CsvFile("original_data.csv", schema=[('a', int32), ('b', str)], delimiter='-')
                >>> my_frame = Frame(source=my_csv)

        .. only:: latex

            .. code::

                >>> my_csv = CsvFile("original_data.csv", schema=[('a', int32),
                ... ('b', str)], delimiter='-')
                >>> my_frame = Frame(source=my_csv)

        Looking at it:

        .. code::

            >>> my_frame.inspect()

              a:int32   b:str
            /-------------------------------/
                1       solo, mono, single
                2       duo, double

        Now, spread out those sub-strings in column *b*:

        .. code::

            >>> my_frame.flatten_column('b')

        Check again:

        .. code::

            >>> my_frame.inspect()

              a:int32   b:str
            /------------------/
                1       solo
                1       mono
                1       single
                2       duo
                2       double



        :param column: The column to be flattened.
        :type column: unicode
        :param delimiter: (default=None)  The delimiter string.
            Default is comma (,).
        :type delimiter: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def get_error_frame(self):
        """
        Get a frame with error recordings.

        When a frame is created, another frame is transparently
        created to capture parse errors.

        Returns
        -------
        Frame : error frame object
            A new object accessing a frame that contains the parse errors of
            the currently active Frame or None if no error frame exists.



        """
        return None


    @doc_stub
    def group_by(self, group_by_columns, aggregation_arguments=None):
        """
        Create summarized frame.

        Creates a new frame and returns a Frame object to access it.
        Takes a column or group of columns, finds the unique combination of
        values, and creates unique rows with these column values.
        The other columns are combined according to the aggregation
        argument(s).

        Notes
        -----
        *   Column order is not guaranteed when columns are added
        *   The column names created by aggregation functions in the new frame
            are the original column name appended with the '_' character and
            the aggregation function.
            For example, if the original field is *a* and the function is
            *avg*, the resultant column is named *a_avg*.
        *   An aggregation argument of *count* results in a column named
            *count*.
        *   The aggregation function *agg.count* is the only full row
            aggregation function supported at this time.
        *   Aggregation currently supports using the following functions:

            *   avg
            *   count
            *   count_distinct
            *   max
            *   min
            *   stdev
            *   sum
            *   var (see glossary Bias vs Variance)

        Examples
        --------
        For setup, we will use a Frame *my_frame* accessing a frame with a
        column *a*:

        .. code::

            >>> my_frame.inspect()

              a:str
            /-------/
              cat
              apple
              bat
              cat
              bat
              cat

        Create a new frame, combining similar values of column *a*,
        and count how many of each value is in the original frame:

        .. code::

            >>> new_frame = my_frame.group_by('a', agg.count)
            >>> new_frame.inspect()

              a:str       count:int
            /-----------------------/
              cat             3
              apple           1
              bat             2

        In this example, 'my_frame' is accessing a frame with three columns,
        *a*, *b*, and *c*:

        .. code::

            >>> my_frame.inspect()

              a:int   b:str   c:float
            /-------------------------/
              1       alpha     3.0
              1       bravo     5.0
              1       alpha     5.0
              2       bravo     8.0
              2       bravo    12.0

        Create a new frame from this data, grouping the rows by unique
        combinations of column *a* and *b*.
        Average the value in *c* for each group:

        .. code::

            >>> new_frame = my_frame.group_by(['a', 'b'], {'c' : agg.avg})
            >>> new_frame.inspect()

              a:int   b:str   c_avg:float
            /-----------------------------/
              1       alpha     4.0
              1       bravo     5.0
              2       bravo    10.0

        For this example, we use *my_frame* with columns *a*, *c*, *d*,
        and *e*:

        .. code::

            >>> my_frame.inspect()

              a:str   c:int   d:float e:int
            /-------------------------------/
              ape     1       4.0     9
              ape     1       8.0     8
              big     1       5.0     7
              big     1       6.0     6
              big     1       8.0     5

        Create a new frame from this data, grouping the rows by unique
        combinations of column *a* and *c*.
        Count each group; for column *d* calculate the average, sum and minimum
        value.
        For column *e*, save the maximum value:

        .. only:: html

            .. code::

                >>> new_frame = my_frame.group_by(['a', 'c'], agg.count, {'d': [agg.avg, agg.sum, agg.min], 'e': agg.max})

                  a:str   c:int   count:int  d_avg:float  d_sum:float   d_min:float   e_max:int
                /-------------------------------------------------------------------------------/
                  ape     1       2          6.0          12.0          4.0           9
                  big     1       3          6.333333     19.0          5.0           7

        .. only:: latex

            .. code::

                >>> new_frame = my_frame.group_by(['a', 'c'], agg.count,
                ... {'d': [agg.avg, agg.sum, agg.min], 'e': agg.max})

                  a    c    count  d_avg  d_sum  d_min  e_max
                  str  int  int    float  float  float  int
                /---------------------------------------------/
                  ape  1    2      6.0    12.0   4.0    9
                  big  1    3      6.333  19.0   5.0    7


        For further examples, see :ref:`example_frame.group_by`.


        :param group_by_columns: Column name or list of column names
        :type group_by_columns: list
        :param aggregation_arguments: (default=None)  Aggregation function based on entire row, and/or dictionaries (one or more) of { column name str : aggregation function(s) }.
        :type aggregation_arguments: dict

        :returns: A new frame with the results of the group_by
        :rtype: Frame
        """
        return None


    @doc_stub
    def histogram(self, column_name, num_bins=None, weight_column_name=None, bin_type='equalwidth'):
        """
        Compute the histogram for a column in a frame.

        Compute the histogram of the data in a column.
        The returned value is a Histogram object containing 3 lists one each for:
        the cutoff points of the bins, size of each bin, and density of each bin.

        **Notes**

        The num_bins parameter is considered to be the maximum permissible number
        of bins because the data may dictate fewer bins.
        With equal depth binning, for example, if the column to be binned has 10
        elements with only 2 distinct values and the *num_bins* parameter is
        greater than 2, then the number of actual number of bins will only be 2.
        This is due to a restriction that elements with an identical value must
        belong to the same bin.

        Examples
        --------
        Consider the following sample data set\:

        .. code::

            >>> frame.inspect()

              a:unicode  b:int32
            /--------------------/
                a          2
                b          7
                c          3
                d          9
                e          1

        A simple call for 3 equal-width bins gives\:

        .. code::

            >>> hist = frame.histogram("b", num_bins=3)
            >>> print hist

            Histogram:
                cutoffs: cutoffs: [1.0, 3.6666666666666665, 6.333333333333333, 9.0],
                hist: [3, 0, 2],
                density: [0.6, 0.0, 0.4]


        Switching to equal depth gives\:

        .. code::

            >>> hist = frame.histogram("b", num_bins=3, bin_type='equaldepth')
            >>> print hist

            Histogram:
                cutoffs: [1, 2, 7, 9],
                hist: [1, 2, 2],
                density: [0.2, 0.4, 0.4]


        .. only:: html

               Plot hist as a bar chart using matplotlib\:

            .. code::

                >>> import matplotlib.pyplot as plt

                >>> plt.bar(hist.cutoffs[:1], hist.hist, width=hist.cutoffs[1] - hist.cutoffs[0])

        .. only:: latex

               Plot hist as a bar chart using matplotlib\:

            .. code::

                >>> import matplotlib.pyplot as plt

                >>> plt.bar(hist.cutoffs[:1], hist.hist, width=hist.cutoffs[1] - 
                ... hist.cutoffs[0])



        :param column_name: Name of column to be evaluated.
        :type column_name: unicode
        :param num_bins: (default=None)  Number of bins in histogram.
            Default is Square-root choice will be used
            (in other words math.floor(math.sqrt(frame.row_count)).
        :type num_bins: int32
        :param weight_column_name: (default=None)  Name of column containing weights.
            Default is all observations are weighted equally.
        :type weight_column_name: unicode
        :param bin_type: (default=equalwidth)  The type of binning algorithm to use: ["equalwidth"|"equaldepth"]
            Defaults is "equalwidth".
        :type bin_type: unicode

        :returns: histogram
                A Histogram object containing the result set.
                The data returned is composed of multiple components:
            cutoffs : array of float
                A list containing the edges of each bin.
            hist : array of float
                A list containing count of the weighted observations found in each bin.
            density : array of float
                A list containing a decimal containing the percentage of
                observations found in the total set per bin.
        :rtype: dict
        """
        return None


    @doc_stub
    def inspect(self, n=10, offset=0, columns=None, wrap='inspect_settings', truncate='inspect_settings', round='inspect_settings', width='inspect_settings', margin='inspect_settings', with_types='inspect_settings'):
        """
        Pretty-print of the frame data

        Essentially returns a string, but technically returns a RowInspection object which renders a string.
        The RowInspection object naturally converts to a str when needed, like when printed or when displayed
        by python REPL (i.e. using the object's __repr__).  If running in a script and want the inspect output
        to be printed, then it must be explicitly printed, then `print frame.inspect()`

        Examples
        --------
        Given a frame of data and a Frame to access it.
        To look at the first 4 rows of data:

        .. code::

            >>> my_frame.inspect(4)
           [#]    animal      name    age     weight
           =========================================
           [0]  human       George      8      542.5
           [1]  human       Ursula      6      495.0
           [2]  ape         Ape        41      400.0
           [3]  elephant    Shep        5     8630.0

        # For other examples, see :ref:`example_frame.inspect`.

        **Global Settings**

        If not specified, the arguments that control formatting receive default values from
        'trustedanalytics.inspect_settings'.  Make changes there to affect all calls to inspect.

        .. code::

            >>> import trustedanalytics as ta
            >>> ta.inspect_settings
            wrap             20
            truncate       None
            round          None
            width            80
            margin         None
            with_types    False
            >>> ta.inspect_settings.width = 120  # changes inspect to use 120 width globally
            >>> ta.inspect_settings.truncate = 16  # changes inspect to always truncate strings to 16 chars
            >>> ta.inspect_settings
            wrap             20
            truncate         16
            round          None
            width           120
            margin         None
            with_types    False
            >>> ta.inspect_settings.width = None  # return value back to default
            >>> ta.inspect_settings
            wrap             20
            truncate         16
            round          None
            width            80
            margin         None
            with_types    False
            >>> ta.inspect_settings.reset()  # set everything back to default
            >>> ta.inspect_settings
            wrap             20
            truncate       None
            round          None
            width            80
            margin         None
            with_types    False

        ..


        :param n: (default=10)  The number of rows to print.
        :type n: int
        :param offset: (default=0)  The number of rows to skip before printing.
        :type offset: int
        :param columns: (default=None)  Filter columns to be included.  By default, all columns are included
        :type columns: int
        :param wrap: (default=inspect_settings)  If set to 'stripes' then inspect prints rows in stripes; if set to an integer N, rows will be printed in clumps of N columns, where the columns are wrapped
        :type wrap: int or 'stripes'
        :param truncate: (default=inspect_settings)  If set to integer N, all strings will be truncated to length N, including a tagged ellipses
        :type truncate: int
        :param round: (default=inspect_settings)  If set to integer N, all floating point numbers will be rounded and truncated to N digits
        :type round: int
        :param width: (default=inspect_settings)  If set to integer N, the print out will try to honor a max line width of N
        :type width: int
        :param margin: (default=inspect_settings)  ('stripes' mode only) If set to integer N, the margin for printing names in a stripe will be limited to N characters
        :type margin: int
        :param with_types: (default=inspect_settings)  If set to True, header will include the data_type of each column
        :type with_types: bool

        :returns: An object which naturally converts to a pretty-print string
        :rtype: RowsInspection
        """
        return None


    @doc_stub
    def join(self, right, left_on, right_on=None, how='inner', name=None):
        """
        Join operation on one or two frames, creating a new frame.

        Create a new frame from a SQL JOIN operation with another frame.
        The frame on the 'left' is the currently active frame.
        The frame on the 'right' is another frame.
        This method takes a column in the left frame and matches its values
        with a column in the right frame.
        Using the default 'how' option ['inner'] will only allow data in the
        resultant frame if both the left and right frames have the same value
        in the matching column.
        Using the 'left' 'how' option will allow any data in the resultant
        frame if it exists in the left frame, but will allow any data from the
        right frame if it has a value in its column which matches the value in
        the left frame column.
        Using the 'right' option works similarly, except it keeps all the data
        from the right frame and only the data from the left frame when it
        matches.
        The 'outer' option provides a frame with data from both frames where
        the left and right frames did not have the same value in the matching
        column.

        Notes
        -----
        When a column is named the same in both frames, it will result in two
        columns in the new frame.
        The column from the *left* frame (originally the current frame) will be
        copied and the column name will have the string "_L" added to it.
        The same thing will happen with the column from the *right* frame,
        except its name has the string "_R" appended. The order of columns
        after this method is called is not guaranteed.

        It is recommended that you rename the columns to meaningful terms prior
        to using the ``join`` method.
        Keep in mind that unicode in column names will likely cause the
        drop_frames() method (and others) to fail!

        Examples
        --------
        For this example, we will use a Frame *my_frame* accessing a frame with
        columns *a*, *b*, *c*, and a Frame *your_frame* accessing a frame with
        columns *a*, *d*, *e*.
        Join the two frames keeping only those rows having the same value in
        column *a*:

        .. code::

            >>> print my_frame.inspect()

              a:unicode   b:unicode   c:unicode
            /--------------------------------------/
              alligator   bear        cat
              apple       berry       cantaloupe
              auto        bus         car
              mirror      frog        ball

            >>> print your_frame.inspect()

              b:unicode   c:int   d:unicode
            /-------------------------------------/
              berry        5218   frog
              blue            0   log
              bus           871   dog

            >>> joined_frame = my_frame.join(your_frame, 'b', how='inner')

        Now, joined_frame is a Frame accessing a frame with the columns *a*,
        *b*, *c_L*, *ci_R*, and *d*.
        The data in the new frame will be from the rows where column 'a' was
        the same in both frames.

        .. code::

            >>> print joined_frame.inspect()

              a:unicode   b:unicode     c_L:unicode   c_R:int64   d:unicode
            /-------------------------------------------------------------------/
              apple       berry         cantaloupe         5218   frog
              auto        bus           car                 871   dog

        More examples can be found in the :ref:`user manual
        <example_frame.join>`.



        :param right: Another frame to join with
        :type right: Frame
        :param left_on: Name of the column in the left frame used to match up the two frames.
        :type left_on: str
        :param right_on: (default=None)  Name of the column in the right frame used to match up the two frames. Default is the same as the left frame.
        :type right_on: str
        :param how: (default=inner)  How to qualify the data to be joined together.  Must be one of the following:  'left', 'right', 'inner', 'outer'.  Default is 'inner'
        :type how: str
        :param name: (default=None)  Name of the result grouped frame
        :type name: str

        :returns: A new frame with the results of the join
        :rtype: Frame
        """
        return None


    @property
    @doc_stub
    def last_read_date(self):
        """
        Last time this frame's data was accessed.



        :returns: Date string of the last time this frame's data was accessed
        :rtype: str
        """
        return None


    @doc_stub
    def loadhbase(self, table_name, schema, start_tag=None, end_tag=None):
        """
        Append data from an HBase table into an existing (possibly empty) FrameRDD

        Append data from an HBase table into an existing (possibly empty) FrameRDD

        :param table_name: hbase table name
        :type table_name: unicode
        :param schema: hbase schema as a list of tuples (columnFamily, columnName, dataType for cell value)
        :type schema: list
        :param start_tag: (default=None)  optional start tag for filtering
        :type start_tag: unicode
        :param end_tag: (default=None)  optional end tag for filtering
        :type end_tag: unicode

        :returns: the initial FrameRDD with the HBase data appended
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def loadhive(self, query):
        """
        Append data from a hive table into an existing (possibly empty) frame

        Append data from a hive table into an existing (possibly empty) frame

        :param query: Initial query to run at load time
        :type query: unicode

        :returns: the initial frame with the hive data appended
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def loadjdbc(self, table_name, connector_type=None, url=None, driver_name=None, query=None):
        """
        Append data from a JDBC table into an existing (possibly empty) frame

        Append data from a JDBC table into an existing (possibly empty) frame

        :param table_name: table name
        :type table_name: unicode
        :param connector_type: (default=None)  (optional) connector type
        :type connector_type: unicode
        :param url: (default=None)  (optional) connection url (includes server name, database name, user acct and password
        :type url: unicode
        :param driver_name: (default=None)  (optional) driver name
        :type driver_name: unicode
        :param query: (default=None)  (optional) query for filtering. Not supported yet.
        :type query: unicode

        :returns: the initial frame with the JDBC data appended
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the frame object.

        Change or retrieve frame object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_frame.name

            "csv_data"

            >>> my_frame.name = "cleaned_data"
            >>> my_frame.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def quantiles(self, column_name, quantiles):
        """
        New frame with Quantiles and their values.

        Calculate quantiles on the given column.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column *final_sale_price*:

        .. code::

            >>> my_frame.inspect()

              final_sale_price:int32
            /------------------------/
                        100
                        250
                         95
                        179
                        315
                        660
                        540
                        420
                        250
                        335

        To calculate 10th, 50th, and 100th quantile:

        .. code::

            >>> quantiles_frame = my_frame.quantiles('final_sale_price', [10, 50, 100])

        A new Frame containing the requested Quantiles and their respective values
        will be returned :

        .. code::

           >>> quantiles_frame.inspect()

             Quantiles:float64   final_sale_price_QuantileValue:float64
           /------------------------------------------------------------/
                    10.0                                     95.0
                    50.0                                    250.0
                   100.0                                    660.0




        :param column_name: The column to calculate quantiles.
        :type column_name: unicode
        :param quantiles: What is being requested.
        :type quantiles: list

        :returns: A new frame with two columns (float64): requested Quantiles and their respective values.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def rename_columns(self, names):
        """
        Rename columns for vertex frame.

        :param names: 
        :type names: None

        :returns: 
        :rtype: _Unit
        """
        return None


    @property
    @doc_stub
    def row_count(self):
        """
        Number of rows in the current frame.

        Counts all of the rows in the frame.

        Examples
        --------
        Get the number of rows:

        .. code::

            >>> my_frame.row_count

        The result given is:

        .. code::

            81734





        :returns: The number of rows in the frame
        :rtype: int
        """
        return None


    @property
    @doc_stub
    def schema(self):
        """
        Current frame column names and types.

        The schema of the current frame is a list of column names and
        associated data types.
        It is retrieved as a list of tuples.
        Each tuple has the name and data type of one of the frame's columns.

        Examples
        --------
        Given that we have an existing data frame *my_data*, create a Frame,
        then show the frame schema:

        .. code::

            >>> BF = ta.get_frame('my_data')
            >>> print BF.schema

        The result is:

        .. code::

            [("col1", str), ("col2", numpy.int32)]





        :returns: list of tuples of the form (<column name>, <data type>)
        :rtype: list
        """
        return None


    @doc_stub
    def sort(self, columns, ascending=True):
        """
        Sort the data in a frame.

        Sort a frame by column values either ascending or descending.

        Examples
        --------
        Sort a single column:

        .. code::

            >>> frame.sort('column_name')

        Sort a single column ascending:

        .. code::

            >>> frame.sort('column_name', True)

        Sort a single column descending:

        .. code::

            >>> frame.sort('column_name', False)

        Sort multiple columns:

        .. code::

            >>> frame.sort(['col1', 'col2'])

        Sort multiple columns ascending:

        .. code::

            >>> frame.sort(['col1', 'col2'], True)

        Sort multiple columns descending:

        .. code::

            >>> frame.sort(['col1', 'col2'], False)

        Sort multiple columns: 'col1' ascending and 'col2' descending:

        .. code::

            >>> frame.sort([ ('col1', True), ('col2', False) ])



        :param columns: Either a column name, a list of column names, or a list of tuples where each tuple is a name and an ascending bool value.
        :type columns: str | list of str | list of tuples
        :param ascending: (default=True)  True for ascending, False for descending.
        :type ascending: bool
        """
        return None


    @doc_stub
    def sorted_k(self, k, column_names_and_ascending, reduce_tree_depth=None):
        """
        Get a sorted subset of the data.

        Take a number of rows and return them
        sorted in either ascending or descending order.

        Sorting a subset of rows is more efficient than sorting the entire frame when
        the number of sorted rows is much less than the total number of rows in the frame.

        Notes
        -----
        The number of sorted rows should be much smaller than the number of rows
        in the original frame.

        In particular:

        #)  The number of sorted rows returned should fit in Spark driver memory.
            The maximum size of serialized results that can fit in the Spark driver is
            set by the Spark configuration parameter *spark.driver.maxResultSize*.
        #)  If you encounter a Kryo buffer overflow exception, increase the Spark
            configuration parameter *spark.kryoserializer.buffer.max.mb*.
        #)  Use Frame.sort() instead if the number of sorted rows is very large (in
            other words, it cannot fit in Spark driver memory).

        Examples
        --------
        These examples deal with the most recently-released movies in a private collection.
        Consider the movie collection already stored in the frame below:

        .. code::

            >>> big_frame.inspect(10)

              genre:str  year:int32   title:str
            /-----------------------------------/
              Drama        1957       12 Angry Men
              Crime        1946       The Big Sleep
              Western      1969       Butch Cassidy and the Sundance Kid
              Drama        1971       A Clockwork Orange
              Drama        2008       The Dark Knight
              Animation    2013       Frozen
              Drama        1972       The Godfather
              Animation    1994       The Lion King
              Animation    2010       Tangled
              Fantasy      1939       The Wonderful Wizard of Oz


        This example returns the top 3 rows sorted by a single column: 'year' descending:

        .. code::

            >>> topk_frame = big_frame.sorted_k(3, [ ('year', False) ])
            >>> topk_frame.inspect()

              genre:str  year:int32   title:str
            /-----------------------------------/
              Animation    2013       Frozen
              Animation    2010       Tangled
              Drama        2008       The Dark Knight


        This example returns the top 5 rows sorted by multiple columns: 'genre' ascending, then 'year' descending:

        .. code::

            >>> topk_frame = big_frame.sorted_k(5, [ ('genre', True), ('year', False) ])
            >>> topk_frame.inspect()

              genre:str  year:int32   title:str
            /-----------------------------------/
              Animation    2013       Frozen
              Animation    2010       Tangled
              Animation    1994       The Lion King
              Crime        1946       The Big Sleep
              Drama        2008       The Dark Knight

        This example returns the top 5 rows sorted by multiple columns: 'genre'
        ascending, then 'year' ascending.
        It also illustrates the optional tuning parameter for reduce-tree depth
        (which does not affect the final result).

        .. code::

            >>> topk_frame = big_frame.sorted_k(5, [ ('genre', True), ('year', True) ], reduce_tree_depth=1)
            >>> topk_frame.inspect()

              genre:str  year:int32   title:str
            /-----------------------------------/
              Animation    1994       The Lion King
              Animation    2010       Tangled
              Animation    2013       Frozen
              Crime        1946       The Big Sleep
              Drama        1972       The Godfather



        :param k: Number of sorted records to return.
        :type k: int32
        :param column_names_and_ascending: Column names to sort by, and true to sort column by ascending order,
            or false for descending order.
        :type column_names_and_ascending: list
        :param reduce_tree_depth: (default=None)  Advanced tuning parameter which determines the depth of the
            reduce-tree (uses Spark's treeReduce() for scalability.)
            Default is 2.
        :type reduce_tree_depth: int32

        :returns: A new frame with a subset of sorted rows from the original frame.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @property
    @doc_stub
    def status(self):
        """
        Current frame life cycle status.

        One of three statuses: Active, Dropped, Finalized
           Active:    Entity is available for use
           Dropped:   Entity has been dropped by user or by garbage collection which found it stale
           Finalized: Entity's data has been deleted

        Examples
        --------
        Given that we have an existing data frame *my_data*, create a Frame,
        then show the frame schema:

        .. code::

            >>> BF = ta.get_frame('my_data')
            >>> print BF.status

        The result is:

        .. code::

            u'Active'




        :returns: Status of the frame
        :rtype: str
        """
        return None


    @doc_stub
    def take(self, n, offset=0, columns=None):
        """
        Get data subset.

        Take a subset of the currently active Frame.

        Notes
        -----
        The data is considered 'unstructured', therefore taking a certain
        number of rows, the rows obtained may be different every time the
        command is executed, even if the parameters do not change.

        Examples
        --------
        Frame *my_frame* accesses a frame with millions of rows of data.
        Get a sample of 5000 rows:

        .. code::

            >>> my_data_list = my_frame.take( 5000 )

        We now have a list of data from the original frame.

        .. code::

            >>> print my_data_list

            [[ 1, "text", 3.1415962 ]
             [ 2, "bob", 25.0 ]
             [ 3, "weave", .001 ]
             ...]

        If we use the method with an offset like:

        .. code::

            >>> my_data_list = my_frame.take( 5000, 1000 )

        We end up with a new list, but this time it has a copy of the data from
        rows 1001 to 5000 of the original frame.



        :param n: The number of rows to copy to the client from the frame.
        :type n: int
        :param offset: (default=0)  The number of rows to skip before starting to copy
        :type offset: int
        :param columns: (default=None)  If not None, only the given columns' data will be provided.  By default, all columns are included
        :type columns: str | iterable of str

        :returns: A list of lists, where each contained list is the data for one row.
        :rtype: list
        """
        return None


    @doc_stub
    def tally(self, sample_col, count_val):
        """
        Count number of times a value is seen.

        A cumulative count is computed by sequentially stepping through the rows,
        observing the column values and keeping track of the number of times the specified
        *count_value* has been seen.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column *obs*:

        .. code::

            >>> my_frame.inspect()

              obs:int32
            /-----------/
                0
                1
                2
                0
                1
                2

        The cumulative count for column *obs* using *count_value = 1* is obtained by:

        .. code::

            >>> my_frame.tally('obs', '1')

        The Frame *my_frame* accesses a frame which now contains two columns *obs*
        and *obsCumulativeCount*.
        Column *obs* still has the same data and *obsCumulativeCount* contains the
        cumulative counts:

        .. code::

            >>> my_frame.inspect()

              obs:int32        obs_tally:int32
            /----------------------------------/
                 0                      0
                 1                      1
                 2                      1
                 0                      1
                 1                      2
                 2                      2



        :param sample_col: The name of the column from which to compute the cumulative count.
        :type sample_col: unicode
        :param count_val: The column value to be used for the counts.
        :type count_val: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def tally_percent(self, sample_col, count_val):
        """
        Compute a cumulative percent count.

        A cumulative percent count is computed by sequentially stepping through
        the rows, observing the column values and keeping track of the percentage of the
        total number of times the specified *count_value* has been seen up to
        the current value.

        Examples
        --------
        Consider Frame *my_frame*, which accesses a frame that contains a single
        column named *obs*:

        .. code::

            >>> my_frame.inspect()

              obs:int32
            /-----------/
                 0
                 1
                 2
                 0
                 1
                 2

        The cumulative percent count for column *obs* is obtained by:

        .. code::

            >>> my_frame.tally_percent('obs', 1)

        The Frame *my_frame* accesses the original frame that now contains two
        columns, *obs* that contains the original column values, and
        *obsCumulativePercentCount* that contains the cumulative percent count:

        .. code::

            >>> my_frame.inspect()

              obs:int32    obs_tally_percent:float64
            /----------------------------------------/
                 0                         0.0
                 1                         0.5
                 2                         0.5
                 0                         0.5
                 1                         1.0
                 2                         1.0



        :param sample_col: The name of the column from which to compute
            the cumulative sum.
        :type sample_col: unicode
        :param count_val: The column value to be used for the counts.
        :type count_val: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


    @doc_stub
    def top_k(self, column_name, k, weights_column=None):
        """
        Most or least frequent column values.

        Calculate the top (or bottom) K distinct values by count of a column.
        The column can be weighted.
        All data elements of weight <= 0 are excluded from the calculation, as are
        all data elements whose weight is NaN or infinite.
        If there are no data elements of finite weight > 0, then topK is empty.

        Examples
        --------
        For this example, we calculate the top 5 movie genres in a data frame:

        .. code::

            >>> top5 = frame.top_k('genre', 5)
            >>> top5.inspect()

              genre:str   count:float64
            /---------------------------/
              Drama        738278
              Comedy       671398
              Short        455728
              Documentary  323150
              Talk-Show    265180

        This example calculates the top 3 movies weighted by rating:

        .. code::

            >>> top3 = frame.top_k('genre', 3, weights_column='rating')
            >>> top3.inspect()

              movie:str      count:float64
            /------------------------------/
              The Godfather         7689.0
              Shawshank Redemption  6358.0
              The Dark Knight       5426.0

        This example calculates the bottom 3 movie genres in a data frame:

        .. code::

            >>> bottom3 = frame.top_k('genre', -3)
            >>> bottom3.inspect()

              genre:str   count:float64
            /---------------------------/
              Musical       26
              War           47
              Film-Noir    595




        :param column_name: The column whose top (or bottom) K distinct values are
            to be calculated.
        :type column_name: unicode
        :param k: Number of entries to return (If k is negative, return bottom k).
        :type k: int32
        :param weights_column: (default=None)  The column that provides weights (frequencies) for the topK calculation.
            Must contain numerical data.
            Default is 1 for all items.
        :type weights_column: unicode

        :returns: An object with access to the frame of data.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f0040ac4090>>
        """
        return None


    @doc_stub
    def unflatten_column(self, composite_key_column_names, delimiter=None):
        """
        Compacts data from multiple rows based on cell data.

        Groups together cells in all columns (less the composite key) using "," as string delimiter.
        The original rows are deleted.
        The grouping takes place based on a composite key created from cell values.
        The column datatypes are changed to string.

        Examples
        --------
        Given a data file::

            user1 1/1/2015 1 70
            user1 1/1/2015 2 60
            user2 1/1/2015 1 65

        The commands to bring the data into a frame, where it can be worked on:

        .. only:: html

            .. code::

                >>> my_csv = ta.CsvFile("original_data.csv", schema=[('a', str), ('b', str),('c', int32) ,('d', int32]))
                >>> my_frame = ta.Frame(source=my_csv)

        .. only:: latex

            .. code::

                >>> my_csv = ta.CsvFile("unflatten_column.csv", schema=[('a', str), ('b', str),('c', int32) ,('d', int32)])
                >>> my_frame = ta.Frame(source=my_csv)

        Looking at it:

        .. code::

            >>> my_frame.inspect()

              a:str        b:str       c:int32       d:int32
            /------------------------------------------------/
               user1       1/1/12015   1             70
               user1       1/1/12015   2             60
               user2       1/1/2015    1             65

        Unflatten the data using columns a & b:

        .. code::

            >>> my_frame.unflatten_column({'a','b'})

        Check again:

        .. code::

            >>> my_frame.inspect()

              a:str        b:str       c:str     d:str
            /-------------------------------------------/
               user1       1/1/12015   1,2       70,60
               user2       1/1/2015    1         65



        :param composite_key_column_names: Name of the column(s) to be used as keys
            for unflattening.
        :type composite_key_column_names: list
        :param delimiter: (default=None)  Separator for the data in the result columns.
            Default is comma (,).
        :type delimiter: unicode

        :returns: 
        :rtype: _Unit
        """
        return None


del doc_stub
del DocStubCalledError