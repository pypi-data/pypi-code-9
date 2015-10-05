#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2015, IBM Corp.
# All rights reserved.
#
# Distributed under the terms of the BSD Simplified License.
#
# The full license is in the LICENSE file, distributed with this software.
#-----------------------------------------------------------------------------

"""
In-Database KMeans.
Copies the interface of sklearn.cluster.KMeans
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import dict
from builtins import str
from future import standard_library
standard_library.install_aliases()

from lazy import lazy
import pandas as pd

import ibmdbpy
from ibmdbpy.exceptions import IdaKMeansError
import six

class KMeans(object):
    """
    The K-means algorithm is the most widely used clustering algorithm that uses
    an explicit distance measure to partition the data set into clusters.

    The main concept of the K-means algorithm is to represent each cluster by the
    vector of mean attribute values of all training instances for numeric attributes
    and by the vector of modal (most frequent) values for nominal attributes that
    are assigned to that cluster. This cluster representation is called cluster center.

    The KMeans class provides an interface for using the KMEANS
    and PREDICT_KMEANS IDAX methods of dashDB/DB2.
    """
    def __init__(self, n_clusters=3, modelname = None, max_iter = 5, distance = "euclidean",
                 random_state = 12345, idbased = False, statistics = None):
        """Constructor for KMeans clustering.

        Parameters
        ----------

        n_cluster : int, optional, default: 3
            The number of cluster centers.
            Range : > 2

        modelname : str, optional
            The name of the clustering model that is to be build.
            not given, it will be generated automatically. If the parameter
            corresponds to an existing model in the database, it will be
            replaced during the fitting step.

        max_iter : int, > 1 and <= 1000, default = 5
            The maximum number of iterations that are to be done.

        distance : str, default: "euclidean"
            The distance function.
            Allowed values are "euclidean" and "norm_euclidean".

        random_state : int, default: 12345
            The random seed for the generator.

        idbased : bool, optional, default: False
            Specifies that the random seed for the generator is based on the
            value of the id column.

        statistics : str, optional
            Indicates the statistics that are to be collected.

            Allowed values are: 'none', 'columns', 'values:n', and 'all':
                * If statistics='none' is specified, no statistics are collected.
                * If statistics='columns' is specified, statistics on the columns of the input table are collected, for example, mean values.
                * If statistics='values:n' is specified, and if n is a positive number, statistics on the columns and the column values are collected.
                    Up to <n> column value statistics are collected.
                        * If a nominal column contains more than <n> values, only the <n> most frequent column statistics are kept.
                        * If a numeric column contains more than <n> values, the values are discretized, and the statistics are collected on the discretized values.
                * statistics=all is identical to statistics=values:100.

        Attributes
        ----------
        centers
            TODO

        cluster_centers_
            TODO

        withinss
            TODO

        size_clusters
            TODO

        inertia_
            TODO


        Returns
        -------
            The KMeans object, ready to be used for fitting and prediction

        Examples
        --------
        >>> idadb = IdaDataBase("DASHDB")
        >>> idadf = IdaDataFrame(idadb, "IRIS", indexer = "ID")
        >>> kmeans = KMeans(3) # clustering with 3 clusters
        >>> kmeans.fit(idadf)
        >>> kmeans.predict(idadf)

        Notes
        -----
        Inner parameters of the model can be printed and modified using respectively
        get_params and set_params. But we recommend creating a new KMeans model
        instead of modifying it.
        """
        self.modelname = modelname
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.distance = distance
        self.random_state = random_state
        self.idbased = idbased
        self.statistics = statistics

        # Get set at fit step
        self._idadb = None
        self._idadf = None
        self._column_id = None
        self.incolumn = None
        self.coldeftype = None
        self.coldefrole = None
        self.colPropertiesTable = None

        # Get set at predict step
        self.outtable = None

    @lazy
    def labels_(self):
        """
o        Returns the corresponding labels for each ID.
        """
        try:
            return self.predict(self._idadf, self._column_id)
        except:
            raise AttributeError(str(self.__class__) + " object has no attribute 'labels_'")

    def get_params(self):
        """
        Returns the parameters of the Kmeans clustering.
        """
        params = dict()
        params['modelname'] = self.modelname
        params['n_clusters'] = self.n_clusters
        params['max_iter'] = self.max_iter
        params['distance'] = self.distance
        params['random_state'] = self.random_state
        params['idbased'] = self.idbased
        params['statistics'] = self.statistics

        params['incolumn'] = self.incolumn
        params['coldeftype'] = self.coldeftype
        params['coldefrole'] = self.coldefrole
        params['colPropertiesTable'] = self.colPropertiesTable

        params['outtable'] = self.outtable
        return params

    def set_params(self, **params):
        """
        Changes parameters of the Kmeans clustering.
        """
        if not params:
            # Simple optimisation to gain speed (inspect is slow)
            return self
        valid_params = self.get_params()
        for key, value in six.iteritems(params):
            if key not in valid_params:
                raise ValueError('Invalid parameter %s for estimator %s' %
                                     (key, self.__class__.__name__))
            setattr(self, key, value)
        return self

    def fit(self, idadf, column_id="ID", incolumn=None, coldeftype=None,
            coldefrole=None, colPropertiesTable=None, verbose=False):
        """
        Uses the KMEANS stored procedure to build a K-means clustering model
        that clusters the input data into k centers.

        Parameters
        ----------
        idadf : IdaDataFrame
            The name of the input IdaDataFrame.

        column_id : str, default: "ID"
            The column of the input IdaDataFrame that identifies a unique
            instance ID.

        incolumn : dict, optional
            The columns of the input table that have specific properties, which
            are separated by a semi-colon (;).
            Each column is succeeded by one or more of the following properties:
                * By type nominal (':nom') or by type continuous (':cont'). By default, numerical types are continuous, and all other types nominal.
                * By role ':id', ':target', ':input', or ':ignore'.

            If this parameter is not specified, all columns of the input table
            have default properties.

        coldeftype : dict, optional
            The default type of the input table columns.
            Allowed values are 'nom' and 'cont'.
            If the parameter is not specified, numeric columns are continuous,
            and all other columns are nominal.

        coldefrole : dict, optional
            The default role of the input table columns.
            Allowed values are 'input' and 'ignore'.
            If the parameter is not specified, all columns are input columns.

        colPropertiesTable : idaDataFrame, optional
            The input IdaDataFrame where properties of the columns of the input
            IdaDataFrame (idadf) are stored.
            If this parameter is not specified, the column properties of the
            input table column properties are detected automatically.

        verbose : bool, default: False
            Verbosity mode.

        """
        if not type(idadf).__name__ == 'IdaDataFrame':
            raise TypeError("Argument should be an IdaDataFrame")

        idadf._idadb._check_procedure("KMEANS", "KMeans")

        # Check the ID
        if column_id not in idadf.columns:
            raise ValueError("No id columns is available in IdaDataFrame:" + column_id +
                             ". Either create a new ID column using add_column_id function" +
                             " or give the name of a column that can be used as ID")

        self._idadb = idadf._idadb
        self._idadf = idadf
        self._column_id = column_id

        # Check or create a model name
        if self.modelname is None:
            self.modelname = idadf._idadb._get_valid_modelname('KMEANS_')
        elif " " in self.modelname:
            raise ValueError("Space in model name is not allowed")
        else:
            if idadf._idadb.exists_model(self.modelname):
                idadf._idadb.drop_model(self.modelname)

        # Create a temporay view
        idadf.internal_state._create_view()
        tmp_view_name = idadf.internal_state.current_state

        try:
            # TODO: outtable is optional but this does not match with the doc
            # Defect to declare
            idadf._idadb._call_stored_procedure("IDAX.KMEANS ",
                                                model = self.modelname,
                                                intable = tmp_view_name,
                                                k = self.n_clusters,
                                                maxiter = self.max_iter,
                                                #outtable = self.outtable_fit,
                                                distance = self.distance,
                                                id = self._column_id,
                                                randseed = self.random_state,
                                                statistics = self.statistics,
                                                idbased = self.idbased,
                                                incolumn = self.incolumn,
                                                coldeftype = self.coldeftype,
                                                coldefrole = self.coldefrole,
                                                colPropertiesTable = self.colPropertiesTable)

        except:
            raise
        finally:
            idadf.internal_state._delete_view()
            idadf.commit()

        result = self._retrieve_KMeans_Model(self.modelname, verbose)
        self.centers = result['centers']
        self.cluster_centers_ = result['centers'].values
        self.withinss = result['withinss']
        self.size_clusters = result['size']
        self.inertia_ = sum(self.withinss)

        if verbose is True:
            self.describe()

        return

    def predict(self, idadf, column_id=None, outtable = None):
        """
        Applies the K-means clustering model to new data.

        Parameters
        ----------
        idadf : IdaDataFrame
            IdaDataFrame to be used as input.

        column_id : str
            The column of the input table that identifies a unique instance ID.
            Default: the same id column that is specified in the stored procedure to build the model.

        outtable : str
            The name of the output table where the assigned clusters are stored.
            If this parameter is not specified, it is generated automatically.
            If the parameter corresponds to an existing table in the database,
            it will be replaced.

        Returns
        -------
        IdaDataFrame
            IdaDataFrame containing the closest cluster for each datapoints
            referenced by their ID.
        """
        if not type(idadf).__name__ == 'IdaDataFrame':
            raise TypeError("Argument should be an IdaDataFrame")

        # Check the ID
        if column_id is None:
            column_id = self._column_id
        if column_id not in idadf.columns:
            raise ValueError("No id columns is available in IdaDataFrame:" + column_id +
                             ". Either create a new ID column using add_column_id function" +
                             " or give the name of a column that can be used as ID")

        if self._idadb is None:
            raise IdaKMeansError("No KMeans model was trained before")


        if outtable is None:
            outtable = idadf._idadb._get_valid_modelname('PREDICT_KMEANS_')
        else:
            outtable = ibmdbpy.utils.check_tablename(self.outtable)
            if idadf._idadb.exists_table(outtable):
                idadf._idadb.drop_table(outtable)

        self.outtable = outtable
        # Create a temporay view
        idadf.internal_state._create_view()
        tmp_view_name = idadf.internal_state.current_state
        try:
            idadf._idadb._call_stored_procedure("IDAX.PREDICT_KMEANS ",
                                                 model = self.modelname,
                                                 intable = tmp_view_name,
                                                 id = column_id,
                                                 outtable = self.outtable
                                                 )
        except:
            raise
        finally:
            idadf.internal_state._delete_view()
            idadf._idadb.commit()

        self.labels_ = ibmdbpy.IdaDataFrame(idadf._idadb, outtable, indexer=column_id)
        return self.labels_

    def fit_predict(self, idadf, column_id="ID", incolumn=None, coldeftype=None,
                    coldefrole=None, colPropertiesTable=None, outtable = None,
                    verbose=False):
        """
        Convenience function for fitting the model and use it to make
        prediction on the same dataset. Please Refer to fit and predict
        documentation for explanation about attributes.
        """
        self.fit(idadf, column_id, incolumn, coldeftype, coldefrole,
                 colPropertiesTable, verbose)
        return self.predict(idadf, column_id, outtable)

    def describe(self):
        """
        Returns a description of Kmeans clustering, if a prediction was made,
        otherwise, return the parameters of the model
        """
        if self._idadb is None:
            return self.get_params
        else:
            print("KMeans clustering with " + str(self.n_clusters) +
            " clusters of sizes " + ', '.join([str(x) for x in self.size_clusters]))
            print()
            print("Cluster means: ")
            print(self.centers)
            print()
            print("Within cluster sum of squares by cluster:")
            print(self.withinss)
            try:
                self._idadb._call_stored_procedure("IDAX.PRINT_MODEL ", model = self.modelname)
            except:
                raise
            return

    def _retrieve_KMeans_Model(self, modelname, verbose = False):
        """
        Retrieves informations about the model for printing to the user.
        KMEANS IDAX functions stores its result in 4 tables:
            * <MODELNAME>_MODEL
            * <MODELNAME>_COLUMNS
            * <MODELNAME>_COLUMN_STATISTICS
            * <MODELNAME>_CLUSTERS

        Parameters
        ----------
        modelname : str
            The name of the model to Retrieve.

        verbose : bol, default: False
            Verbosity mode.
        """
        modelname = ibmdbpy.utils.check_tablename(modelname)

        if self._idadb is None:
            raise IdaKMeansError("No KMeans model was trained before")

        model_main = self._idadb.ida_query('SELECT * FROM "' +
        self._idadb.current_schema + '"."' + modelname + '_MODEL"')
        model_main.columns = [x.upper() for x in model_main.columns]

        col_info = self._idadb.ida_query('SELECT * FROM "' +
        self._idadb.current_schema + '"."' + modelname + '_COLUMNS"',)
        col_info.columns = [x.upper() for x in col_info.columns]

        col_stats = self._idadb.ida_query('SELECT * FROM "' +
        self._idadb.current_schema + '"."' + modelname + '_COLUMN_STATISTICS"')
        col_stats.columns = [x.upper() for x in col_stats.columns]

        km_out_stat = self._idadb.ida_query('SELECT * FROM "' +
        self._idadb.current_schema + '"."' + modelname + '_CLUSTERS"')
        km_out_stat.columns = [x.upper() for x in km_out_stat.columns]

        k = model_main.iloc[0][3]
        distance = model_main.iloc[0][2]
        cont_cols = col_info.loc[(col_info['USAGETYPE'] == 'active') & (col_info['OPTYPE'] == 'continuous'), ['COLUMNNAME']]
        cat_cols = col_info.loc[(col_info['USAGETYPE'] == 'active') & (col_info['OPTYPE'] == 'categorical'), ['COLUMNNAME']]

        columns = []
        for x in col_stats['COLUMNNAME'].values:
            if x not in columns:
                columns.append(x)

        clusters = km_out_stat['CLUSTERID'].values
        clusters.sort()

        cluster_centers = []
        for cluster in clusters:
            tmp = [cluster]
            for column in columns:
                if column in cont_cols.values:
                    tmp.append(col_stats.loc[(col_stats['CLUSTERID'] == cluster) & (col_stats['COLUMNNAME'] == column)]['MEAN'].values[0])
                elif column in cat_cols.values:
                    tmp.append(col_stats.loc[(col_stats['CLUSTERID'] == cluster) & (col_stats['COLUMNNAME'] == column)]['MODE'].values[0])
                else:
                    raise TypeError("Unexpected column category")
            cluster_centers.append(tmp)

        centers = pd.DataFrame([tuple(x) for x in cluster_centers])
        centers.columns = ['CLUSTERID'] + columns

        if verbose is True:
            print("MODEL")
            print(model_main)
            print("COLUMNS")
            print(col_info)
            print("COLUMNS_STATISTICS")
            print(col_stats)
            print("CLUSTERS")
            print(km_out_stat)

        result = dict()
        result['withinss'] = km_out_stat['WITHINSS'].values
        result['size'] = km_out_stat['SIZE'].values
        result['relsize'] = km_out_stat['RELSIZE'].values
        result['distance'] = distance

        result['k'] = k
        result['centers'] = centers

        return result