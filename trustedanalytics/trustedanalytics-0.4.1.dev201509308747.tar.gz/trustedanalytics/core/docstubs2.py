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

# Auto-generated file for API static documentation stubs (2015-09-30T01:48:30.410859)
#
# **DO NOT EDIT**

from trustedanalytics.meta.docstub import doc_stub, DocStubCalledError



__all__ = ["CollaborativeFilteringModel", "KMeansModel", "LdaModel", "LibsvmModel", "LinearRegressionModel", "LogisticRegressionModel", "NaiveBayesModel", "PrincipalComponentsModel", "RandomForestClassifierModel", "RandomForestRegressorModel", "SvmModel", "drop_frames", "drop_graphs", "drop_models", "get_frame", "get_frame_names", "get_graph", "get_graph_names", "get_model", "get_model_names"]

@doc_stub
class CollaborativeFilteringModel(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Create a new Collaborative Filtering Recommend model.

        For details about Collaborative Filter Recommend modelling,
        see :ref:`Collaborative Filter <CollaborativeFilteringNewPlugin_Summary>`.

        :param name: (default=None)  User supplied name.
        :type name: unicode

        :returns: 
        :rtype: CollaborativeFilteringModel
        """
        raise DocStubCalledError("model:collaborative_filtering/new")


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the model object.

        Change or retrieve model object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_model.name

            "csv_data"

            >>> my_model.name = "cleaned_data"
            >>> my_model.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def recommend(self, name, top_k):
        """
        Collaborative Filtering Recommend (ALS/CGD) model.

        See :ref:`Collaborative Filtering Train
        <python_api/models/model-collaborative_filtering/train>` for more information.

        :param name: An entity name from the first column of the input frame
        :type name: unicode
        :param top_k: positive integer representing the top recommendations for the name
        :type top_k: int32

        :returns: See :ref:`Collaborative Filtering Train
            <python_api/models/model-collaborative_filtering/train>` for more information.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        """
        return None


    @doc_stub
    def train(self, frame, user_col_name, item_col_name, rating_col_name, evaluation_function=None, num_factors=None, max_iterations=None, convergence_threshold=None, regularization=None, bias_on=None, min_value=None, max_value=None, learning_curve_interval=None, cgd_iterations=None):
        """
        Collaborative filtering (ALS/CGD) model

        :param frame: 
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param user_col_name: Name of the user column from input data
        :type user_col_name: unicode
        :param item_col_name: Name of the item column from input data
        :type item_col_name: unicode
        :param rating_col_name: Name of the rating column from input data
        :type rating_col_name: unicode
        :param evaluation_function: (default=None)  ALS/CGD
        :type evaluation_function: unicode
        :param num_factors: (default=None)  Size of the desired factors (default is 3)
        :type num_factors: int32
        :param max_iterations: (default=None)  Max number of iterations for Giraph
        :type max_iterations: int32
        :param convergence_threshold: (default=None)  float value between 0 .. 1
        :type convergence_threshold: float64
        :param regularization: (default=None)  float value between 0 .. 1 
        :type regularization: float32
        :param bias_on: (default=None)  bias on/off switch 
        :type bias_on: bool
        :param min_value: (default=None)  minimum edge weight value
        :type min_value: float32
        :param max_value: (default=None)  minimum edge weight value
        :type max_value: float32
        :param learning_curve_interval: (default=None)  iteration interval to output learning curve
        :type learning_curve_interval: int32
        :param cgd_iterations: (default=None)  custom argument for CGD learning curve output interval (default: every iteration)
        :type cgd_iterations: int32

        :returns: Execution result summary for Giraph
        :rtype: dict
        """
        return None



@doc_stub
class KMeansModel(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Create a 'new' instance of a k-means model.

        k-means [1]_ is an unsupervised algorithm used to partition
        the data into 'k' clusters.
        Each observation can belong to only one cluster, the cluster with the nearest
        mean.
        The k-means model is initialized, trained on columns of a frame, and used to
        predict cluster assignments for a frame.
        This model runs the MLLib implementation of k-means [2]_ with enhanced
        features, computing the number of elements in each cluster during training.
        During predict, it computes the distance of each observation from its cluster
        center and also from every other cluster center.

        .. rubric:: footnotes

        .. [1] https://en.wikipedia.org/wiki/K-means_clustering
        .. [2] https://spark.apache.org/docs/1.3.0/mllib-clustering.html#k-means

        :param name: (default=None)  Name for the model.
        :type name: unicode

        :returns: 
        :rtype: KMeansModel
        """
        raise DocStubCalledError("model:k_means/new")


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the model object.

        Change or retrieve model object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_model.name

            "csv_data"

            >>> my_model.name = "cleaned_data"
            >>> my_model.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def predict(self, frame, observation_columns=None):
        """
        Predict the cluster assignments for the data points.

        Examples
        --------
        .. only:: html

            .. code::

                >>> my_model = ta.KMeansModel(name='MyKmeansModel')
                >>> my_model.train(my_frame, ['name_of_observation_column1', 'name_of_observation_column2'],[2.0, 5.0] 3, 10, 0.0002, "random")
                >>> new_frame = my_model.predict(my_frame)

        .. only:: latex

            .. code::

                >>> my_model = ta.KMeansModel(name='MyKmeansModel')
                >>> my_model.train(my_frame, ['name_of_observation_column1',
                ... 'name_of_observation_column2'],[2.0, 5.0] 3, 10, 0.0002, "random")
                >>> new_frame = my_model.predict(my_frame)




        :param frame: A frame whose labels are to be predicted.
            By default, predict is run on the same columns over which the model is
            trained.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param observation_columns: (default=None)  Column(s) containing the observations
            whose clusters are to be predicted.
            Default is to predict the clusters over columns the KMeans model was trained on.
            The columns are scaled using the same values used when training the
            model.
        :type observation_columns: list

        :returns: A new frame consisting of the existing columns of the frame
            and new columns.
            The data returned is composed of multiple components\:

            |   **double** : *'k' columns*
            |       Squared distance of each point to every cluster center.
            |   **int** : *predicted_cluster*
            |       The cluster assignment.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        """
        return None


    @doc_stub
    def publish(self):
        """
        Creates a scoring engine tar file.



        :returns: The HDFS path to the tar file.
        :rtype: dict
        """
        return None


    @doc_stub
    def train(self, frame, observation_columns, column_scalings, k=None, max_iterations=None, epsilon=None, initialization_mode=None):
        """
        Creates k-means model from trained frame.

        Upon training the 'k' cluster centers are computed.

        Examples
        --------
        .. only:: html

            .. code::

                >>> my_model = ta.KMeansModel(name='MyKMeansModel')
                >>> my_model.train(train_frame, ['name_of_observation_column1', 'name_of_observation_column2'],[1.0,2.0] 3, 10, 0.0002, "random")

        .. only:: latex

            .. code::

                >>> my_model = ta.KMeansModel(name='MyKMeansModel')
                >>> my_model.train(train_frame, ['name_of_observation_column1',
                ... 'name_of_observation_column2'],[1.0,2.0] 3, 10, 0.0002, "random")


        :param frame: A frame to train the model on.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param observation_columns: Columns containing the
            observations.
        :type observation_columns: list
        :param column_scalings: Column scalings for each of the observation columns.
            The scaling value is multiplied by the corresponding value in the
            observation column.
        :type column_scalings: list
        :param k: (default=None)  Desired number of clusters.
            Default is 2.
        :type k: int32
        :param max_iterations: (default=None)  Number of iterations for which the algorithm should run.
            Default is 20.
        :type max_iterations: int32
        :param epsilon: (default=None)  Distance threshold within which we consider k-means to have converged.
            Default is 1e-4.
        :type epsilon: float64
        :param initialization_mode: (default=None)  The initialization technique for the algorithm.
            It could be either "random" or "k-means||".
            Default is "k-means||".
        :type initialization_mode: unicode

        :returns: The data returned is composed of multiple components\:

            |   **dict** : *cluster_size*
            |       Cluster size.
            |   **int** : *ClusterId*
            |       Number of elements in the cluster 'ClusterId'.
            |   **double** : *within_set_sum_of_squared_error*
            |       Sum of squared error for the model.
        :rtype: dict
        """
        return None



@doc_stub
class LdaModel(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Creates Latent Dirichlet Allocation model

        |LDA| is a commonly-used algorithm for topic modeling, but,
        more broadly, is considered a dimensionality reduction technique.
        For more detail see :ref:`LDA <LdaNewPlugin_Summary>`.

        :param name: (default=None)  User supplied name.
        :type name: unicode

        :returns: 
        :rtype: LdaModel
        """
        raise DocStubCalledError("model:lda/new")


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the model object.

        Change or retrieve model object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_model.name

            "csv_data"

            >>> my_model.name = "cleaned_data"
            >>> my_model.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def predict(self, document):
        """
        Predict conditional probabilities of topics given document.

        Predicts conditional probabilities of topics given document using trained Latent Dirichlet Allocation model.
        The input document is represented as a list of strings

        Examples
        --------

        Inspect the input frame:

        .. code::
            >>> frame.inspect()

            doc_id:unicode   word_id:unicode   word_count:int64
            \-------------------------------------------------------\
              nytimes          harry                            3
              nytimes          economy                         35
              nytimes          jobs                            40
              nytimes          magic                            1
              nytimes          realestate                      15
              nytimes          movies                           6
              economist        economy                         50
              economist        jobs                            35
              economist        realestate                      20
              economist        movies                           1

        .. code::

            >>> my_model = ta.LdaModel()
            >>> results = my_model.train(frame, 'doc_id', 'word_id', 'word_count', max_iterations = 3, num_topics = 2)
            >>> prediction = model.predict(['harry', 'secrets', 'magic', 'harry', 'chamber' 'test'])

        The variable *prediction* is a dictionary with three keys:

        .. code::

            >>> topics_given_doc = results['topics_given_doc']
            >>> new_words_percentage = results['new_words_percentage']
            >>> new_words_count = results['new_words_count']
            >>> print(prediction)

            {u'topics_given_doc': [0.04150190747884333, 0.7584980925211566], u'new_words_percentage': 20.0, u'new_words_count': 1}



        :param document: Document whose topics are to be predicted. 
        :type document: list

        :returns: Dictionary containing predicted topics.
            The data returned is composed of multiple components\:

            |   **list of doubles** | *topics_given_doc*
            |       List of conditional probabilities of topics given document.
            |   **int** : *new_words_count*
            |       Count of new words in test document not present in training set.
            |   **double** | *new_words_percentage*
            |       Percentage of new words in test document.
        :rtype: dict
        """
        return None


    @doc_stub
    def publish(self):
        """
        Creates a scoring engine tar file.

        Creates a tar file with the trained Latent Dirichlet Allocation model.
        The tar file is used as input to the scoring engine to predict the conditional topic
        probabilities for a document.



        :returns: The HDFS path to the tar file.
        :rtype: dict
        """
        return None


    @doc_stub
    def train(self, frame, document_column_name, word_column_name, word_count_column_name, max_iterations=None, alpha=None, beta=None, convergence_threshold=None, evaluate_cost=None, num_topics=None):
        """
        Creates Latent Dirichlet Allocation model

        See the discussion about `Latent Dirichlet Allocation at Wikipedia. <http://en.wikipedia.org/wiki/Latent_Dirichlet_allocation>`__

        Examples
        --------

        Inspect the input frame:

        .. code::
            >>> frame.inspect()

            doc_id:unicode   word_id:unicode   word_count:int64
            \-------------------------------------------------------\
              nytimes          harry                            3
              nytimes          economy                         35
              nytimes          jobs                            40
              nytimes          magic                            1
              nytimes          realestate                      15
              nytimes          movies                           6
              economist        economy                         50
              economist        jobs                            35
              economist        realestate                      20
              economist        movies                           1

        .. code::

            >>> my_model = ta.LdaModel()
            >>> results = my_model.train(frame, 'doc_id', 'word_id', 'word_count', max_iterations = 3, num_topics = 2)

        The variable *results* is a dictionary with four keys:

        .. code::

            >>> topics_given_doc = results['topics_given_doc']
            >>> word_given_topics = results['word_given_topics']
            >>> topics_given_word = results['topics_given_word']
            >>> report = results['report']


        Inspect the results:

        .. code::
            >>> print("conditional probability of topics given document")
            >>> topics_given_doc.inspect()

             doc_id:unicode         topic_probabilities:vector(2)
            \--------------------------------------------------------------\
              nytimes           [0.6411692639409163, 0.3588307360590836]
              economist        [0.8729037921033002, 0.12709620789669976]
              harrypotter      [0.04037038771254577, 0.9596296122874542]

            >>> print("conditional probability of word given topics")
            >>> word_given_topics.inspect()

             word_id:unicode          topic_probabilities:vector(2)
            \-----------------------------------------------------------------\
              jobs                [0.310153576632259, 0.15771353529047744]
              realestate        [0.19982350094988224, 0.026879558761907126]
              secrets           [0.002344603492542889, 0.16832490819830945]
              magic             [0.015459535145939628, 0.16833906458965853]
              chamber           [0.008569051106470452, 0.10657403682025736]
              economy            [0.4842227935973047, 0.06458045349269073]
              harry             [0.019215463609876204, 0.23279687893102033]
              movies            [0.03728831237906273, 0.008577561181278793]

            >>> print("conditional probability of topics given word")
            >>> topics_given_word.inspect()

             word_id:unicode         topic_probabilities:vector(2)
            \----------------------------------------------------------------\
              chamber           [0.060256136055438406, 0.9397438639445616]
              movies             [0.797036385540048, 0.2029636144599522]
              secrets           [0.008569949938887081, 0.9914300500611131]
              magic              [0.0704558957152857, 0.9295441042847143]
              harry             [0.06424184587002194, 0.9357581541299779]
              realestate        [0.8666980184047205, 0.13330198159527962]
              jobs              [0.6285123369605498, 0.37148766303945036]
              economy            [0.8664742287086458, 0.1335257712913541]

        View the report:

        .. code::

            >>> print report

            ======Graph Statistics======
            Number of vertices: 11 (doc: 3, word: 8)
            Number of edges: 32

            ======LDA Configuration======
            numTopics: 2
            alpha: 0.100000
            beta: 0.100000
            convergenceThreshold: 0.001000
            maxIterations: 3
            evaluateCost: false

            ======Learning Progress======
            iteration = 1	maxDelta = 0.677352
            iteration = 2	maxDelta = 0.173309
            iteration = 3	maxDelta = 0.181216



        :param frame: Input frame data.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param document_column_name: Column Name for documents.
            Column should contain a str value.
        :type document_column_name: unicode
        :param word_column_name: Column name for words.
            Column should contain a str value.
        :type word_column_name: unicode
        :param word_count_column_name: Column name for word count.
            Column should contain an int32 or int64 value.
        :type word_count_column_name: unicode
        :param max_iterations: (default=None)  The maximum number of iterations that the algorithm will execute.
            The valid value range is all positive int.
            Default is 20.
        :type max_iterations: int32
        :param alpha: (default=None)  The hyperparameter for document-specific distribution over topics.
            Mainly used as a smoothing parameter in Bayesian inference.
            Larger value implies that documents are assumed to cover all topics
            more uniformly; smaller value implies that documents are more
            concentrated on a small subset of topics.
            Valid value range is all positive float.
             Default is 0.1.
        :type alpha: float32
        :param beta: (default=None)  The hyperparameter for word-specific distribution over topics.
            Mainly used as a smoothing parameter in Bayesian inference.
            Larger value implies that topics contain all words more uniformly and
            smaller value implies that topics are more concentrated on a small
            subset of words.
            Valid value range is all positive float.
            Default is 0.1.
        :type beta: float32
        :param convergence_threshold: (default=None)  The amount of change in LDA model parameters that will be tolerated
            at convergence.
            If the change is less than this threshold, the algorithm exits
            before it reaches the maximum number of supersteps.
            Valid value range is all positive float and 0.0.
            Default is 0.001.
        :type convergence_threshold: float32
        :param evaluate_cost: (default=None)  "True" means turn on cost evaluation and "False" means turn off
            cost evaluation.
            It's relatively expensive for LDA to evaluate cost function.
            For time-critical applications, this option allows user to turn off cost
            function evaluation.
            Default is "False".
        :type evaluate_cost: bool
        :param num_topics: (default=None)  The number of topics to identify in the LDA model.
            Using fewer topics will speed up the computation, but the extracted topics
            might be more abstract or less specific; using more topics will
            result in more computation but lead to more specific topics.
            Valid value range is all positive int.
            Default is 10.
        :type num_topics: int32

        :returns: The data returned is composed of multiple components\:

            |   **Frame** : *topics_given_doc*
            |       Conditional probabilities of topic given document.
            |   **Frame** : *word_given_topics*
            |       Conditional probabilities of word given topic.
            |   **Frame** : *topics_given_word*
            |       Conditional probabilities of topic given word.
            |   **str** : *report*
            |       The configuration and learning curve report for Latent Dirichlet
            Allocation as a multiple line str.
        :rtype: dict
        """
        return None



@doc_stub
class LibsvmModel(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Create a 'new' instance of a Support Vector Machine model.

        Support Vector Machine [1]_ is a supervised algorithm used to
        perform binary classification.
        A support vector machine constructs a high dimensional hyperplane which is
        said to achieve a good separation when a hyperplane has the largest distance to
        the nearest training-data point of any class. This model runs the
        LIBSVM [2]_ [3]_ implementation of SVM.
        The LIBSVM model is initialized, trained on columns of a frame, used to
        predict the labels of observations in a frame and used to test the predicted
        labels against the true labels.
        During testing, labels of the observations are predicted and tested against
        the true labels using built-in binary Classification Metrics.

        .. rubric: footnotes

        .. [1] https://en.wikipedia.org/wiki/Support_vector_machine
        .. [2] https://www.csie.ntu.edu.tw/~cjlin/libsvm/
        .. [3] https://en.wikipedia.org/wiki/LIBSVM

        :param name: (default=None)  User supplied name.
        :type name: unicode

        :returns: 
        :rtype: LibsvmModel
        """
        raise DocStubCalledError("model:libsvm/new")


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the model object.

        Change or retrieve model object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_model.name

            "csv_data"

            >>> my_model.name = "cleaned_data"
            >>> my_model.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def predict(self, frame, observation_columns=None):
        """
        New frame with new predicted label column.

        Predict the labels for a test frame and create a new frame revision with
        existing columns and a new predicted label's column.

        Examples
        --------

        .. only:: html

            .. code::

                >>> my_model = ta.LibsvmModel(name='mySVM')
                >>> my_model.train(train_frame, 'name_of_label_column',['name_of_observation_column1'])
                >>> predicted_frame = my_model.predict(predict_frame, ['predict_for_observation_column'])

        .. only:: latex

            .. code::

                >>> my_model = ta.LibsvmModel(name='mySVM')
                >>> my_model.train(train_frame, 'name_of_label_column',
                ... ['name_of_observation_column1'])
                >>> predicted_frame = my_model.predict(predict_frame,
                ... ['predict_for_observation_column'])



        :param frame: A frame whose labels are to be predicted.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param observation_columns: (default=None)  Column(s) containing the observations whose labels are to be
            predicted.
            Default is the columns the LIBSVM model was trained on.
        :type observation_columns: list

        :returns: A new frame containing the original frame's columns and a column
            *predicted_label* containing the score calculated for each observation.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        """
        return None


    @doc_stub
    def publish(self):
        """
        Creates a scoring engine tar file.

        The HDFS path to the tar file.



        :returns: 
        :rtype: dict
        """
        return None


    @doc_stub
    def score(self, vector):
        """
        Calculate the prediction label for a single observation.

        Examples
        --------

        .. only:: html

            .. code::

                >>> my_model = ta.LibsvmModel(name='mySVM')
                >>> my_model.train(train_frame, 'name_of_label_column',['name_of_observation_column1'])
                >>> predicted_label = my_model.score([-0.79798,   -0.0256669,    0.234375,   0.0140301,   -0.282051,    0.025012])

        .. only:: latex

            .. code::

                >>> my_model = ta.LibsvmModel(name='mySVM')
                >>> my_model.train(train_frame, 'name_of_label_column',
                ... ['name_of_observation_column1'])
                >>> predicted_label = my_model.score([-0.79798,   -0.0256669,    0.234375,   0.0140301,   -0.282051,    0.025012])



        :param vector: 
        :type vector: None

        :returns: Predicted label.
        :rtype: dict
        """
        return None


    @doc_stub
    def test(self, frame, label_column, observation_columns=None):
        """
        Predict test frame labels and return metrics.

        Predict the labels for a test frame and run classification
        metrics on predicted and target labels.

        Examples
        --------
        .. only:: html

            .. code::

                >>> my_model = ta.LibsvmModel(name='mySVM')
                >>> my_model.train(train_frame, 'name_of_label_column',['List_of_observation_column/s'])
                >>> metrics = my_model.test(test_frame, 'name_of_label_column',['List_of_observation_column/s'])

                >>> metrics.f_measure
                0.66666666666666663

                >>> metrics.recall
                0.5

                >>> metrics.accuracy
                0.75

                >>> metrics.precision
                1.0

                >>> metrics.confusion_matrix

                              Predicted
                            _pos_ _neg__
                Actual  pos |  1     1
                        neg |  0     2


        .. only:: latex

            .. code::

                >>> my_model = ta.LibsvmModel(name='mySVM')
                >>> my_model.train(train_frame, 'name_of_label_column',
                ... ['List_of_observation_column/s'])
                >>> metrics = my_model.test(test_frame, 'name_of_label_column',
                ... ['List_of_observation_column/s'])

                >>> metrics.f_measure
                0.66666666666666663

                >>> metrics.recall
                0.5

                >>> metrics.accuracy
                0.75

                >>> metrics.precision
                1.0

                >>> metrics.confusion_matrix

                              Predicted
                            _pos_ _neg__
                Actual  pos |  1     1
                        neg |  0     2




        :param frame: A frame whose labels are to be predicted.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param label_column: Column containing the actual label for each
            observation.
        :type label_column: unicode
        :param observation_columns: (default=None)  Column(s) containing the observations whose
            labels are to be predicted and tested.
            Default is to test over the columns the LIBSVM model
            was trained on.
        :type observation_columns: list

        :returns: Object with binary classification metrics.
            The data returned is composed of multiple components\:

            |  **double** : *accuracy*
            |      The degree of correctness of the test frame labels.
            |  **table** : *confusion_matrix*
            |     A specific table layout that allows visualization of the performance of the
            test.
            |  **double** : *f_measure*
            |     A measure of a test's accuracy.
            It considers both the precision and the recall of the test to compute the score.
            |  **double** : *precision*
            |     The degree to which the correctness of the label is expressed.
            |  **double** : *recall*
            |      The fraction of relevant instances that are retrieved.
        :rtype: dict
        """
        return None


    @doc_stub
    def train(self, frame, label_column, observation_columns, svm_type=2, kernel_type=2, weight_label=None, weight=None, epsilon=0.001, degree=3, gamma=None, coef=0.0, nu=0.5, cache_size=100.0, shrinking=1, probability=0, nr_weight=1, c=1.0, p=0.1):
        """
        Train LIBSVM model.

        Creating a LIBSVM Model using the observation column and label column of the
        train frame.

        Examples
        --------
        .. only:: html

            .. code::

                >>> my_model = ta.LibsvmModel(name='mySVM')
                >>> my_model.train(train_frame, 'name_of_label_column',['List_of_observation_column/s'], epsilon=0.001, degree=3, gamma=0.11, coef=0.0, nu=0.5, cache_size=100.0, shrinking=1, probability=0, c=1.0, p=0.1, nr_weight=1, svm_type=2, kernel_type=2)

        .. only:: latex

            .. code::

                >>> my_model = ta.LibsvmModel(name='mySVM')
                >>> my_model.train(train_frame, 'name_of_label_column',
                ... ['List_of_observation_column/s'],
                ... epsilon=0.001, degree=3, gamma=0.11, coef=0.0, nu=0.5,
                ... cache_size=100.0, shrinking=1, probability=0, c=1.0, p=0.1,
                ... nr_weight=1, svm_type=2, kernel_type=2)



        :param frame: A frame to train the model on.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param label_column: Column name containing the label for each
            observation.
        :type label_column: unicode
        :param observation_columns: Column(s) containing the
            observations.
        :type observation_columns: list
        :param svm_type: (default=2)  Set type of SVM.
            Default is one-class SVM.

            |   0 -- C-SVC
            |   1 -- nu-SVC
            |   2 -- one-class SVM
            |   3 -- epsilon-SVR
            |   4 -- nu-SVR
        :type svm_type: int32
        :param kernel_type: (default=2)  Specifies the kernel type to be used in the algorithm.
            Default is RBF.

            |   0 -- linear: u\'\*v
            |   1 -- polynomial: (gamma*u\'\*v + coef0)^degree
            |   2 -- radial basis function: exp(-gamma*|u-v|^2)
            |   3 -- sigmoid: tanh(gamma*u\'\*v + coef0)
        :type kernel_type: int32
        :param weight_label: (default=None)  Default is (Array[Int](0))
        :type weight_label: list
        :param weight: (default=None)  Default is (Array[Double](0.0))
        :type weight: list
        :param epsilon: (default=0.001)  Set tolerance of termination criterion
        :type epsilon: float64
        :param degree: (default=3)  Degree of the polynomial kernel function ('poly').
            Ignored by all other kernels.
        :type degree: int32
        :param gamma: (default=None)  Kernel coefficient for 'rbf', 'poly' and 'sigmoid'.
            Default is 1/n_features.
        :type gamma: float64
        :param coef: (default=0.0)  Independent term in kernel function.
            It is only significant in 'poly' and 'sigmoid'.
        :type coef: float64
        :param nu: (default=0.5)  Set the parameter nu of nu-SVC, one-class SVM,
            and nu-SVR.
        :type nu: float64
        :param cache_size: (default=100.0)  Specify the size of the kernel
            cache (in MB).
        :type cache_size: float64
        :param shrinking: (default=1)  Whether to use the shrinking heuristic.
            Default is 1 (true).
        :type shrinking: int32
        :param probability: (default=0)  Whether to enable probability estimates.
            Default is 0 (false).
        :type probability: int32
        :param nr_weight: (default=1)  NR Weight
        :type nr_weight: int32
        :param c: (default=1.0)  Penalty parameter c of the error term.
        :type c: float64
        :param p: (default=0.1)  Set the epsilon in loss function of epsilon-SVR.
        :type p: float64

        :returns: 
        :rtype: _Unit
        """
        return None



@doc_stub
class LinearRegressionModel(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Create a 'new' instance of a Linear Regression model.

        Linear Regression [1]_ is used to model the relationship between a scalar
        dependent variable and one or more independent variables.
        The Linear Regression model is initialized, trained on columns of a frame and
        used to predict the value of the dependent variable given the independent
        observations of a frame.
        This model runs the MLLib implementation of Linear Regression [2]_ with the
        SGD [3]_ optimizer.
                        
        .. rubric:: footnotes

        .. [1] https://en.wikipedia.org/wiki/Linear_regression
        .. [2] https://spark.apache.org/docs/1.3.0/mllib-linear-methods.html#linear-least-squares-lasso-and-ridge-regression
        .. [3] https://en.wikipedia.org/wiki/Stochastic_gradient_descent

        :param name: (default=None)  User supplied name.
        :type name: unicode

        :returns: 
        :rtype: LinearRegressionModel
        """
        raise DocStubCalledError("model:linear_regression/new")


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the model object.

        Change or retrieve model object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_model.name

            "csv_data"

            >>> my_model.name = "cleaned_data"
            >>> my_model.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def predict(self, frame, observation_columns=None):
        """
        Make new frame with column for label prediction.

        Predict the labels for a test frame and create a new frame revision with
        existing columns and a new predicted value column.

        Examples
        --------

        .. only:: html

            .. code::

                >>> my_model = ta.LinearRegressionModel(name='LinReg')
                >>> my_model.train(train_frame, 'name_of_label_column',['name_of_observation_column(s)'])
                >>> my_model.predict(predict_frame, ['name_of_observation_column(s)'])

        .. only:: latex

            .. code::

                >>> my_model = ta.LinearRegressionModel(name='LinReg')
                >>> my_model.train(train_frame, 'name_of_label_column', ['name_of_observation_column(s)'])
                >>> my_model.predict(predict_frame, ['name_of_observation_column(s)'])



        :param frame: A frame whose labels are to be predicted.
            By default, predict is run on the same columns over which the model is
            trained.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param observation_columns: (default=None)  Column(s) containing the observations
            whose labels are to be predicted.
            Default is the labels the model was trained on.
        :type observation_columns: list

        :returns: Frame containing the original frame's columns and a column with the predicted value.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        """
        return None


    @doc_stub
    def train(self, frame, label_column, observation_columns, intercept=None, num_iterations=None, step_size=None, reg_type=None, reg_param=None, mini_batch_fraction=None):
        """
        Build linear regression model.

        Creating a Linear Regression Model using the observation column and label column of the train frame.

        Examples
        --------

        .. only:: html

            .. code::

                >>> my_model = ta.LinearRegressionModel(name='LinReg')
                >>> my_model.train(train_frame, 'name_of_label_column',['name_of_observation_column(s)'],false, 50, 1.0, "L1", 0.02, 1.0)

        .. only:: latex

            .. code::

                >>> my_model = ta.LinearRegressionModel(name='LinReg')
                >>> my_model.train(train_frame, 'name_of_label_column', ['name_of_observation_column(s)'],
                ...  false, 50, 1.0, "L1", 0.02, 1.0)



        :param frame: A frame to train the model on.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param label_column: Column name containing the label
            for each observation.
        :type label_column: unicode
        :param observation_columns: Column(s) containing the
            observations.
        :type observation_columns: list
        :param intercept: (default=None)  The algorithm adds an intercept.
            Default is true.
        :type intercept: bool
        :param num_iterations: (default=None)  Number of iterations.
            Default is 100.
        :type num_iterations: int32
        :param step_size: (default=None)  Step size for optimizer.
            Default is 1.0.
        :type step_size: int32
        :param reg_type: (default=None)  Regularization L1 or L2.
            Default is L2.
        :type reg_type: unicode
        :param reg_param: (default=None)  Regularization parameter.
            Default is 0.01.
        :type reg_param: float64
        :param mini_batch_fraction: (default=None)  Mini batch fraction parameter.
            Default is 1.0.
        :type mini_batch_fraction: float64

        :returns: 
        :rtype: _Unit
        """
        return None



@doc_stub
class LogisticRegressionModel(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Create a 'new' instance of logistic regression model.

        Logistic Regression [1]_ is a widely used supervised binary and multi-class classification algorithm.
        The Logistic Regression model is initialized, trained on columns of a frame, predicts the labels
        of observations, and tests the predicted labels against the true labels.
        This model runs the MLLib implementation of Logistic Regression [2]_, with enhanced features |EM|
        trained model summary statistics; Covariance and Hessian matrices; ability to specify the frequency
        of the train and test observations.
        Testing performance can be viewed via built-in binary and multi-class Classification Metrics.
        It also allows the user to select the optimizer to be used - L-BFGS [3]_ or SGD [4]_.

        .. rubric:: footnotes

        .. [1] https://en.wikipedia.org/wiki/Logistic_regression
        .. [2] https://spark.apache.org/docs/1.3.0/mllib-linear-methods.html#logistic-regression
        .. [3] https://en.wikipedia.org/wiki/Limited-memory_BFGS
        .. [4] https://en.wikipedia.org/wiki/Stochastic_gradient_descent
            

        :param name: (default=None)  User supplied name.
        :type name: unicode

        :returns: 
        :rtype: LogisticRegressionModel
        """
        raise DocStubCalledError("model:logistic_regression/new")


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the model object.

        Change or retrieve model object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_model.name

            "csv_data"

            >>> my_model.name = "cleaned_data"
            >>> my_model.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def predict(self, frame, observation_columns=None):
        """
        Predict labels for data points using trained logistic regression model.

        Predict the labels for a test frame using trained logistic regression model,
                      and create a new frame revision with existing columns and a new predicted label's column.

        Examples
        --------

        .. only:: html

            .. code::

                >>> my_model = ta.LogisticRegressionModel(name='LogReg')
                >>> my_model.train(train_frame, 'name_of_observation_column', 'name_of_label_column', num_classes=2, optimizer="LBFGS"))
                >>> my_model.predict(predict_frame, ['predict_for_observation_column'])

        .. only:: latex

            .. code::

                >>> my_model = ta.LogisticRegressionModel(name='LogReg')
                >>> my_model.train(train_frame, 'name_of_observation_column',
                ... 'name_of_label_column', num_classes=2, optimizer="LBFGS"))
                >>> my_model.predict(predict_frame, ['predict_for_observation_column'])



        :param frame: A frame whose labels are to be predicted.
            By default, predict is run on the same columns over which the model is
            trained.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param observation_columns: (default=None)  Column(s) containing the observations
            whose labels are to be predicted.
            Default is the labels the model was trained on.
        :type observation_columns: list

        :returns: Frame containing the original frame's columns and a column with the predicted label.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        """
        return None


    @doc_stub
    def test(self, frame, label_column, observation_columns=None):
        """
        Predict test frame labels using trained logistic regression model, and show metrics.

        Predict the labels for a test frame and run classification metrics on predicted and target labels.

        Examples
        --------
        .. only:: html

            .. code::

                >>> my_model = ta.LogisticRegressionModel(name='LogReg')
                >>> my_model.train(train_frame, 'name_of_observation_column', 'name_of_label_column')
                >>> metrics = my_model.test(test_frame, 'name_of_label_column','name_of_observation_column')

                >>> metrics.f_measure
                0.66666666666666663

                >>> metrics.recall
                0.5

                >>> metrics.accuracy
                0.75

                >>> metrics.precision
                1.0

                >>> metrics.confusion_matrix

                              Predicted
                            _pos_ _neg__
                Actual  pos |  1     1
                        neg |  0     2

        .. only:: latex

            .. code::

                >>> my_model = ta.LogisticRegressionModel(name='LogReg')
                >>> my_model.train(train_frame, 'name_of_observation_column',
                ... 'name_of_label_column')
                >>> metrics = my_model.test(test_frame, 'name_of_label_column',
                ... 'name_of_observation_column')

                >>> metrics.f_measure
                0.66666666666666663

                >>> metrics.recall
                0.5

                >>> metrics.accuracy
                0.75

                >>> metrics.precision
                1.0

                >>> metrics.confusion_matrix

                              Predicted
                            _pos_ _neg__
                Actual  pos |  1     1
                        neg |  0     2




        :param frame: Frame whose labels are to be
            predicted.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param label_column: Column containing the actual
            label for each observation.
        :type label_column: unicode
        :param observation_columns: (default=None)  Column(s) containing the observations
            whose labels are to be predicted and tested.
            Default is to test over the columns the SVM model
            was trained on.
        :type observation_columns: list

        :returns: An object with binary classification metrics.
            The data returned is composed of multiple components\:

            | **double** : *accuracy*
            | **table** : *confusion_matrix*
            | **double** : *f_measure*
            | **double** : *precision*
            | **double** : *recall*
        :rtype: dict
        """
        return None


    @doc_stub
    def train(self, frame, label_column, observation_columns, frequency_column=None, num_classes=2, optimizer='LBFGS', compute_covariance=True, intercept=True, feature_scaling=False, threshold=0.5, reg_type='L2', reg_param=0.0, num_iterations=100, convergence_tolerance=0.0001, num_corrections=10, mini_batch_fraction=1.0, step_size=1):
        """
        Build logistic regression model.

        Creating a Logistic Regression Model using the observation column and
        label column of the train frame.

        Examples
        --------
        Train logistic regression model using Limited-memory-BFGS.

        In the example below, the flag for computing the covariance matrix is enabled.
        When the covariance matrix is enabled, the summary table contains additional
        statistics about the quality of the trained model.

        .. only:: html

            .. code::

                >>> my_model = ta.LogisticRegressionModel(name='LogReg')
                >>> metrics = my_model.train(train_frame, 'name_of_label_column', ['obs1', 'obs2'], 'frequency_column', num_classes=2, optimizer='LBFGS', compute_covariance=True)

                >>> metrics.num_features
                2

                >>> metrics.num_classes
                2

                >>> metrics.summary_table

                            coefficients  degrees_freedom  standard_errors  wald_statistic   p_value
                intercept      0.924574                1         0.013052       70.836965    0.000000e+00
                obs1           0.405374                1         0.005793       69.973643    1.110223e-16
                obs2           0.707372                1         0.006709      105.439358    0.000000e+00

                >>> metrics.covariance_matrix.inspect()

                intercept:float64        obs1:float64        obs1:float64
                -------------------------------------------------------------
                0.000170358314027   1.85520616189e-05   3.60362435109e-05
                1.85520616189e-05   3.35615519594e-05   1.51513099821e-05
                3.60362435109e-05   1.51513099821e-05   4.50080801085e-05

        .. only:: latex

            .. code::

                >>> my_model = ta.LogisticRegressionModel(name='LogReg')
                >>> my_model.train(train_frame,'name_of_label_column', ['obs1', 'obs2'], 'frequency_column',
                ... num_classes=2, optimizer='LBFGS', compute_covariance=True)

                >>> metrics.num_features
                2

                >>> metrics.num_classes
                2

                >>> metrics.summary_table

                            coefficients  degrees_freedom  standard_errors  wald_statistic   p_value
                intercept      0.924574                1         0.013052       70.836965    0.000000e+00
                obs1           0.405374                1         0.005793       69.973643    1.110223e-16
                obs2           0.707372                1         0.006709      105.439358    0.000000e+00

                >>> metrics.covariance_matrix.inspect()

                intercept:float64        obs1:float64        obs1:float64
                -------------------------------------------------------------
                0.000170358314027   1.85520616189e-05   3.60362435109e-05
                1.85520616189e-05   3.35615519594e-05   1.51513099821e-05
                3.60362435109e-05   1.51513099821e-05   4.50080801085e-05


        :param frame: A frame to train the model on.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param label_column: Column name containing the label for each
            observation.
        :type label_column: unicode
        :param observation_columns: Column(s) containing the
            observations.
        :type observation_columns: list
        :param frequency_column: (default=None)  Optional column containing the frequency of
            observations.
        :type frequency_column: unicode
        :param num_classes: (default=2)  Number of classes
        :type num_classes: int32
        :param optimizer: (default=LBFGS)  Set type of optimizer.
            | LBFGS - Limited-memory BFGS.
            | LBFGS supports multinomial logistic regression.
            | SGD - Stochastic Gradient Descent.
            | SGD only supports binary logistic regression.
        :type optimizer: unicode
        :param compute_covariance: (default=True)  Compute covariance matrix for the
            model.
        :type compute_covariance: bool
        :param intercept: (default=True)  Add intercept column to training
            data.
        :type intercept: bool
        :param feature_scaling: (default=False)  Perform feature scaling before training
            model.
        :type feature_scaling: bool
        :param threshold: (default=0.5)  Threshold for separating positive predictions from
            negative predictions.
        :type threshold: float64
        :param reg_type: (default=L2)  Set type of regularization
            | L1 - L1 regularization with sum of absolute values of coefficients
            | L2 - L2 regularization with sum of squares of coefficients
        :type reg_type: unicode
        :param reg_param: (default=0.0)  Regularization parameter
        :type reg_param: float64
        :param num_iterations: (default=100)  Maximum number of iterations
        :type num_iterations: int32
        :param convergence_tolerance: (default=0.0001)  Convergence tolerance of iterations for L-BFGS.
            Smaller value will lead to higher accuracy with the cost of more
            iterations.
        :type convergence_tolerance: float64
        :param num_corrections: (default=10)  Number of corrections used in LBFGS update.
            Default is 10.
            Values of less than 3 are not recommended;
            large values will result in excessive computing time.
        :type num_corrections: int32
        :param mini_batch_fraction: (default=1.0)  Fraction of data to be used for each SGD
            iteration
        :type mini_batch_fraction: float64
        :param step_size: (default=1)  Initial step size for SGD.
            In subsequent steps, the step size decreases by stepSize/sqrt(t)
        :type step_size: int32

        :returns: An object with a summary of the trained model.
            The data returned is composed of multiple components\:

            | **int** : *numFeatures*
            |   Number of features in the training data
            | **int** : *numClasses*
            |   Number of classes in the training data
            | **table** : *summaryTable*
            |   A summary table composed of:
            | **Frame** : *CovarianceMatrix (optional)*
            |   Covariance matrix of the trained model.
            The covariance matrix is the inverse of the Hessian matrix for the trained model.
            The Hessian matrix is the second-order partial derivatives of the model's log-likelihood function.
        :rtype: dict
        """
        return None



@doc_stub
class NaiveBayesModel(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Create a 'new' instance of a Naive Bayes model

        Naive Bayes [1]_ is a probabilistic classifier with strong
        independence assumptions between features.
        It computes the conditional probability distribution of each feature given label,
        and then applies Bayes' theorem to compute the conditional probability
        distribution of a label given an observation, and use it for prediction.
        The Naive Bayes model is initialized, trained on columns of a frame, and used
        to predict the value of the dependent variable given the independent
        observations of a frame.
        This model runs the MLLib implementation of Naive Bayes [2]_.

        .. rubric:: footnotes

        .. [1] https://en.wikipedia.org/wiki/Naive_Bayes_classifier
        .. [2] https://spark.apache.org/docs/1.3.0/mllib-naive-bayes.html

        :param name: (default=None)  User supplied name.
        :type name: unicode

        :returns: 
        :rtype: NaiveBayesModel
        """
        raise DocStubCalledError("model:naive_bayes/new")


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the model object.

        Change or retrieve model object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_model.name

            "csv_data"

            >>> my_model.name = "cleaned_data"
            >>> my_model.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def predict(self, frame, observation_columns=None):
        """
        Predict labels for data points using trained Naive Bayes model.

        Predict the labels for a test frame using trained Naive Bayes model,
              and create a new frame revision with existing columns and a new predicted label's column.

        Examples
        --------

        .. only:: html

            .. code::

                >>> my_model = ta.NaiveBayesModel(name='naivebayesmodel')
                >>> my_model.train(train_frame, 'name_of_label_column',['name_of_observation_column(s)'])
                >>> output = my_model.predict(predict_frame, ['name_of_observation_column(s)'])
                >>> output.inspect(5)

                      Class:int32   Dim_1:int32   Dim_2:int32   Dim_3:int32   predicted_class:float64
                    -----------------------------------------------------------------------------------
                                0             1             0             0                       0.0
                                1             0             1             0                       1.0
                                1             0             2             0                       1.0
                                2             0             0             1                       2.0
                                2             0             0             2                       2.0

        .. only:: latex

            .. code::

                >>> my_model = ta.NaiveBayesModel(name='naivebayesmodel')
                >>> my_model.train(train_frame, 'name_of_label_column', ['name_of_observation_column(s)'])
                >>> output = my_model.predict(predict_frame, ['name_of_observation_column(s)'])
                >>> output.inspect(5)

                      Class:int32   Dim_1:int32   Dim_2:int32   Dim_3:int32   predicted_class:float64
                    -----------------------------------------------------------------------------------
                                0             1             0             0                       0.0
                                1             0             1             0                       1.0
                                1             0             2             0                       1.0
                                2             0             0             1                       2.0
                                2             0             0             2                       2.0



        :param frame: A frame whose labels are to be predicted.
            By default, predict is run on the same columns over which the model is
            trained.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param observation_columns: (default=None)  Column(s) containing the
            observations whose labels are to be predicted.
            By default, we predict the labels over columns the NaiveBayesModel
            was trained on.
        :type observation_columns: list

        :returns: Frame containing the original frame's columns and a column with the predicted label.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        """
        return None


    @doc_stub
    def train(self, frame, label_column, observation_columns, lambda_parameter=None):
        """
        Train a Naive Bayes model.

        Train a NaiveBayesModel using the observation column, label column of the train
        frame and an optional lambda value.

        Examples
        --------

        .. only:: html

            .. code::

                >>> my_model = ta.NaiveBayesModel(name='naivebayesmodel')
                >>> my_model.train(train_frame, 'name_of_label_column',['name_of_observation_column(s)'],0.9)

        .. only:: latex

            .. code::

                >>> my_model = ta.NaiveBayesModel(name='naivebayesmodel')
                >>> my_model.train(train_frame, 'name_of_label_column',['name_of_observation_column(s)'],0.9)



        :param frame: A frame to train the model on.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param label_column: Column containing the label for each
            observation.
        :type label_column: unicode
        :param observation_columns: Column(s) containing the
            observations.
        :type observation_columns: list
        :param lambda_parameter: (default=None)  Additive smoothing parameter
            Default is 1.0.
        :type lambda_parameter: float64

        :returns: 
        :rtype: _Unit
        """
        return None



@doc_stub
class PrincipalComponentsModel(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Create a 'new' instance of a Principal Components model.

        Principal component analysis [1]_ is a statistical algorithm
        that converts possibly correlated features to linearly uncorrelated variables
        called principal components.
        The number of principal components is less than or equal to the number of
        original variables.
        This implementation of computing Principal Components is done by Singular
        Value Decomposition [2]_ of the data, providing the user with an option to
        mean center the data.
        The Principal Components model is initialized; trained on
        specifying the observation columns of the frame and the number of components;
        used to predict principal components.
        The MLLib Singular Value Decomposition [3]_ implementation has been used for
        this, with additional features to 1) mean center the data during train and
        predict and 2) compute the t-squared index during prediction.

        .. rubric:: footnotes

        .. [1] https://en.wikipedia.org/wiki/Principal_component_analysis
        .. [2] https://en.wikipedia.org/wiki/Singular_value_decomposition
        .. [3] https://spark.apache.org/docs/1.3.0/mllib-dimensionality-reduction.html

        :param name: (default=None)  User supplied name.
        :type name: unicode

        :returns: 
        :rtype: PrincipalComponentsModel
        """
        raise DocStubCalledError("model:principal_components/new")


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the model object.

        Change or retrieve model object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_model.name

            "csv_data"

            >>> my_model.name = "cleaned_data"
            >>> my_model.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def predict(self, frame, mean_centered=True, t_squared_index=False, observation_columns=None, c=None, name=None):
        """
        Predict using principal components model.

        Predicting on a dataframe's columns using a Principal Components Model.

        :param frame: Frame whose principal components
            are to be computed.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param mean_centered: (default=True)  Option to mean center the columns.
            Default is true
        :type mean_centered: bool
        :param t_squared_index: (default=False)  Indicator for whether the t-square
            index is to be computed.
            Default is false.
        :type t_squared_index: bool
        :param observation_columns: (default=None)  List of observation column name(s)
            to be used for prediction.
            Default is the list of column name(s) used to train
            the model.
        :type observation_columns: list
        :param c: (default=None)  The number of principal components
            to be predicted.
            Default is the count used to train the model.
        :type c: int32
        :param name: (default=None)  The name of the output frame
            generated by predict.
        :type name: unicode

        :returns: A frame with existing columns and 'c' additional columns containing
            the projections of V on the frame and an additional column storing the t-square-index value if requested.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        """
        return None


    @doc_stub
    def publish(self):
        """
        Creates a scoring engine tar file.

        Creates a tar file with the trained Principal Components Model.
        The tar file is used as input to the scoring engine to compute the principal components and
        t-squared index of the observation.



        :returns: The HDFS path to the tar file.
        :rtype: dict
        """
        return None


    @doc_stub
    def train(self, frame, observation_columns, mean_centered=True, k=None):
        """
        Build principal components model.

        Creating a Principal Components Model using the observation columns.

        :param frame: A frame to train the model
            on.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param observation_columns: List of column(s) containing
            the observations.
        :type observation_columns: list
        :param mean_centered: (default=True)  Option to mean center the
            columns
        :type mean_centered: bool
        :param k: (default=None)  Principal component count.
            Default is the number of observation columns
        :type k: int32

        :returns: Values of the  principal components model object storing\:

            |   principal components count used to train the model,
            |   the list of observation columns on which the model was trained,
            |   the singular values vector and the vFactor matrix stored as an array of double values.
        :rtype: dict
        """
        return None



@doc_stub
class RandomForestClassifierModel(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Create a 'new' instance of a Random Forest Classifier model.

        Random Forest [1]_ is a supervised ensemble learning algorithm
        which can be used to perform binary and multi-class classification.
        The Random Forest Classifier model is initialized, trained on columns of a
        frame, used to predict the labels of observations in a frame, and tests the
        predicted labels against the true labels.
        This model runs the MLLib implementation of Random Forest [2]_.
        During training, the decision trees are trained in parallel.
        During prediction, each tree's prediction is counted as vote for one class.
        The label is predicted to be the class which receives the most votes.
        During testing, labels of the observations are predicted and tested against the true labels
        using built-in binary and multi-class Classification Metrics.

        .. rubric:: footnotes

        .. [1] https://en.wikipedia.org/wiki/Random_forest
        .. [2] https://spark.apache.org/docs/1.3.0/mllib-ensembles.html
         

        :param name: (default=None)  User supplied name.
        :type name: unicode

        :returns: 
        :rtype: RandomForestClassifierModel
        """
        raise DocStubCalledError("model:random_forest_classifier/new")


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the model object.

        Change or retrieve model object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_model.name

            "csv_data"

            >>> my_model.name = "cleaned_data"
            >>> my_model.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def predict(self, frame, observation_columns=None):
        """
        Predict the labels for the data points.

        :param frame: A frame whose labels are to be predicted.
            By default, predict is run on the same columns over which the model is
            trained.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param observation_columns: (default=None)  Column(s) containing the observations whose labels are to be predicted.
            By default, we predict the labels over columns the RandomForestModel
            was trained on. 
        :type observation_columns: list

        :returns: A new frame consisting of the existing columns of the frame and
            a new column with predicted label for each observation.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        """
        return None


    @doc_stub
    def publish(self):
        """
        Creates a scoring engine tar file.

        Creates a tar file with the trained Random Forest Classifier Model
        The tar file is used as input to the scoring engine to predict the class of an observation.



        :returns: The HDFS path to the tar file.
        :rtype: dict
        """
        return None


    @doc_stub
    def test(self, frame, label_column, observation_columns=None):
        """
        Predict test frame labels and return metrics.

        Predict the labels for a test frame and run classification metrics on predicted
        and target labels.

        :param frame: The frame whose labels are to be predicted
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param label_column: Column containing the true labels of the observations
        :type label_column: unicode
        :param observation_columns: (default=None)  Column(s) containing the observations whose labels are to be predicted.
            By default, we predict the labels over columns the RandomForest was trained on.
        :type observation_columns: list

        :returns: An object with classification metrics.
            The data returned is composed of multiple components\:

            |  **double** : *accuracy*
            |  **table** : *confusion_matrix*
            |  **double** : *f_measure*
            |  **double** : *precision*
            |  **double** : *recall*
        :rtype: dict
        """
        return None


    @doc_stub
    def train(self, frame, label_column, observation_columns, num_classes=2, num_trees=1, impurity='gini', max_depth=4, max_bins=100, seed=-246156022, categorical_features_info=None, feature_subset_category=None):
        """
        Build Random Forests Classifier model.

        Creating a Random Forests Classifier Model using the observation columns and label column.

        :param frame: A frame to train the model on.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param label_column: Column name containing the label for each observation.
        :type label_column: unicode
        :param observation_columns: Column(s) containing the observations.
        :type observation_columns: list
        :param num_classes: (default=2)  Number of classes for classification.
        :type num_classes: int32
        :param num_trees: (default=1)  Number of tress in the random forest.
        :type num_trees: int32
        :param impurity: (default=gini)  Criterion used for information gain calculation.
            Supported values "gini" or "entropy"
        :type impurity: unicode
        :param max_depth: (default=4)  Maximum depth of the tree.
        :type max_depth: int32
        :param max_bins: (default=100)  Maximum number of bins used for
            splitting features.
        :type max_bins: int32
        :param seed: (default=-246156022)  Random seed for bootstrapping and
            choosing feature subsets
        :type seed: int32
        :param categorical_features_info: (default=None)  
        :type categorical_features_info: None
        :param feature_subset_category: (default=None)  Number of features to consider for splits at each node.
            Supported values\: "auto","all","sqrt","log2","onethird".
        :type feature_subset_category: unicode

        :returns: Values of the Random Forest Classifier model object storing\:

            |  the list of observation columns on which the model was trained,
            |  the column name containing the labels of the observations,
            |  the number of classes,
            |  the number of decision trees in the random forest,
            |  the number of nodes in the random forest,
            |  the map storing arity of categorical features,
            |  the criterion used for information gain calculation,
            |  the maximum depth of the tree,
            |  the maximum number of bins used for splitting features,
            |  the random seed used for bootstrapping and choosing feature subset.

        :rtype: dict
        """
        return None



@doc_stub
class RandomForestRegressorModel(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Create a 'new' instance of a Random Forest Regressor model.

        Random Forest [1]_ is a supervised ensemble learning algorithm
        used to perform regression.
        A Random Forest Regressor model is initialized, trained on columns of a frame,
        and used to predict the value of each observation in the frame.
        This model runs the MLLib implementation of Random Forest [2]_.
        During training, the decision trees are trained in parallel.
        During prediction, the average over-all tree's predicted value is the predicted
        value of the random forest.

        .. rubric:: footnotes

        .. [1] https://en.wikipedia.org/wiki/Random_forest
        .. [2] https://spark.apache.org/docs/1.3.0/mllib-ensembles.html

        :param name: (default=None)  User supplied name.
        :type name: unicode

        :returns: 
        :rtype: RandomForestRegressorModel
        """
        raise DocStubCalledError("model:random_forest_regressor/new")


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the model object.

        Change or retrieve model object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_model.name

            "csv_data"

            >>> my_model.name = "cleaned_data"
            >>> my_model.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def predict(self, frame, observation_columns=None):
        """
        Predict the values for the data points.

        :param frame: A frame whose labels are to be predicted.
            By default, predict is run on the same columns over which the model is
            trained.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param observation_columns: (default=None)  Column(s) containing the observations whose labels are to be predicted.
            By default, we predict the labels over columns the Random Forest model
            was trained on. 
        :type observation_columns: list

        :returns: A new frame consisting of the existing columns of the frame and
            a new column with predicted value for each observation.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        """
        return None


    @doc_stub
    def publish(self):
        """
        Creates a scoring engine tar file.

        Creates a tar file with the trained Random Forest Regressor Model
        The tar file is used as input to the scoring engine to predict the value of an observation.



        :returns: The HDFS path to the tar file.
        :rtype: dict
        """
        return None


    @doc_stub
    def train(self, frame, label_column, observation_columns, num_trees=1, impurity='variance', max_depth=4, max_bins=100, seed=574743065, categorical_features_info=None, feature_subset_category=None):
        """
        Build Random Forests Regressor model.

        Creating a Random Forests Regressor Model using the observation columns and label column.

        :param frame: A frame to train the model on
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param label_column: Column name containing the label for each observation
        :type label_column: unicode
        :param observation_columns: Column(s) containing the observations
        :type observation_columns: list
        :param num_trees: (default=1)  Number of tress in the random forest
        :type num_trees: int32
        :param impurity: (default=variance)  Criterion used for information gain calculation. Supported values "variance"
        :type impurity: unicode
        :param max_depth: (default=4)  Maximum depth of the tree
        :type max_depth: int32
        :param max_bins: (default=100)  Maximum number of bins used for splitting features
        :type max_bins: int32
        :param seed: (default=574743065)  Random seed for bootstrapping and choosing feature subsets
        :type seed: int32
        :param categorical_features_info: (default=None)  
        :type categorical_features_info: None
        :param feature_subset_category: (default=None)  Number of features to consider for splits at each node. Supported values "auto", "all", "sqrt","log2", "onethird"
        :type feature_subset_category: unicode

        :returns: Values of the Random Forest Classifier model object storing\:

            |  the list of observation columns on which the model was trained,
            |  the column name containing the labels of the observations,
            |  the number of decision trees in the random forest,
            |  the number of nodes in the random forest,
            |  the map storing arity of categorical features,
            |  the criterion used for information gain calculation,
            |  the maximum depth of the tree,
            |  the maximum number of bins used for splitting features,
            |  the random seed used for bootstrapping and choosing feature subset.
        :rtype: dict
        """
        return None



@doc_stub
class SvmModel(object):
    """
    Auto-generated to contain doc stubs for static program analysis
    """


    def __init__(self, name=None):
        """
            Create a 'new' instance of a Support Vector Machine model.

        Support Vector Machine [1]_ is a supervised algorithm used to
        perform binary classification.
        A Support Vector Machine constructs a high dimensional hyperplane which is
        said to achieve a good separation when a hyperplane has the largest distance
        to the nearest training-data point of any class.
        This model runs the MLLib implementation of SVM [2]_ with SGD [3]_ optimizer.
        The SVMWithSGD model is initialized, trained on columns of a frame, used to
        predict the labels of observations in a frame, and tests the predicted labels
        against the true labels.
        During testing, labels of the observations are predicted and tested against
        the true labels using built-in binary Classification Metrics.

        .. rubric:: footnotes

        .. [1] https://en.wikipedia.org/wiki/Support_vector_machine
        .. [2] https://spark.apache.org/docs/1.3.0/mllib-linear-methods.html
        .. [3] https://en.wikipedia.org/wiki/Stochastic_gradient_descent

        :param name: (default=None)  User supplied name.
        :type name: unicode

        :returns: 
        :rtype: SvmModel
        """
        raise DocStubCalledError("model:svm/new")


    @property
    @doc_stub
    def name(self):
        """
        Set or get the name of the model object.

        Change or retrieve model object identification.
        Identification names must start with a letter and are limited to
        alphanumeric characters and the ``_`` character.


        Examples
        --------

        .. code::

            >>> my_model.name

            "csv_data"

            >>> my_model.name = "cleaned_data"
            >>> my_model.name

            "cleaned_data"



        """
        return None


    @doc_stub
    def predict(self, frame, observation_columns=None):
        """
        Make new frame with additional column for predicted label.

        Predict the labels for a test frame and create a new frame revision with
        existing columns and a new predicted label's column.

        Examples
        --------
        .. only:: html

            .. code::

                >>> my_model = ta.SvmModel(name='mySVM')
                >>> my_model.train(train_frame, ['name_of_observation_column1'], 'name_of_label_column')
                >>> predicted_frame = my_model.predict(predict_frame, ['predict_for_observation_column'])

        .. only:: latex

            .. code::

                >>> my_model = ta.SvmModel(name='mySVM')
                >>> my_model.train(train_frame, ['name_of_observation_column1'],
                ... 'name_of_label_column')
                >>> predicted_frame = my_model.predict(predict_frame,
                ... ['predict_for_observation_column'])



        :param frame: A frame whose labels are to be predicted.
            By default, predict is run on the same columns over which the model is
            trained.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param observation_columns: (default=None)  Column(s) containing the observations
            whose labels are to be predicted.
            Default is the labels the model was trained on.
        :type observation_columns: list

        :returns: A frame containing the original frame's columns and a column with the
            predicted label.
        :rtype: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        """
        return None


    @doc_stub
    def test(self, frame, label_column, observation_columns=None):
        """
        Predict test frame labels and return metrics.

        Predict the labels for a test frame and run classification metrics on predicted
        and target labels.

        Examples
        --------
        .. only:: html

            .. code::

                >>> my_model = ta.SvmModel(name='mySVM')
                >>> my_model.train(train_frame, ['name_of_observation_column'], 'name_of_label_column')
                >>> metrics = my_model.test(test_frame, 'name_of_label_column',['name_of_observation_column'])

                >>> metrics.f_measure
                0.66666666666666663

                >>> metrics.recall
                0.5

                >>> metrics.accuracy
                0.75

                >>> metrics.precision
                1.0

                >>> metrics.confusion_matrix

                              Predicted
                            _pos_ _neg__
                Actual  pos |  1     1
                        neg |  0     2


        .. only:: latex

            .. code::

                >>> my_model = ta.SvmModel(name='mySVM')
                >>> my_model.train(train_frame, ['name_of_observation_column'],
                ... 'name_of_label_column')
                >>> metrics = my_model.test(test_frame, 'name_of_label_column',
                ... ['name_of_observation_column'])

                >>> metrics.f_measure
                0.66666666666666663

                >>> metrics.recall
                0.5

                >>> metrics.accuracy
                0.75

                >>> metrics.precision
                1.0

                >>> metrics.confusion_matrix

                              Predicted
                            _pos_ _neg__
                Actual  pos |  1     1
                        neg |  0     2




        :param frame: Frame whose labels are to be
            predicted.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param label_column: Column containing the actual
            label for each observation.
        :type label_column: unicode
        :param observation_columns: (default=None)  Column(s) containing the observations
            whose labels are to be predicted and tested.
            Default is to test over the columns the SVM model
            was trained on.
        :type observation_columns: list

        :returns: An object with binary classification metrics.
            The data returned is composed of multiple components\:

            |  **double** : *accuracy*
            |  **table** : *confusion_matrix*
            |  **double** : *f_measure*
            |  **double** : *precision*
            |  **double** : *recall*
        :rtype: dict
        """
        return None


    @doc_stub
    def train(self, frame, label_column, observation_columns, intercept=None, num_iterations=None, step_size=None, reg_type=None, reg_param=None, mini_batch_fraction=None):
        """
        Train SVM model.

        Creating a SVM Model using the observation column and label column of the train frame.

        Examples
        --------
        .. only:: html

            .. code::

                >>> my_model = ta.SvmModel(name='mySVM')
                >>> my_model.train(train_frame, ['name_of_observation_column'], 'name_of_label_column', false, 50, 1.0, "L1", 0.02, 1.0)

        .. only:: latex

            .. code::

                >>> my_model = ta.SvmModel(name='mySVM')
                >>> my_model.train(train_frame, ['name_of_observation_column'],
                ... 'name_of_label_column', false, 50, 1.0, "L1", 0.02, 1.0)



        :param frame: A frame to train the model on.
        :type frame: <bound method AtkEntityType.__name__ of <trustedanalytics.rest.jsonschema.AtkEntityType object at 0x7f5df7066350>>
        :param label_column: Column name containing the label
            for each observation.
        :type label_column: unicode
        :param observation_columns: Column(s) containing the
            observations.
        :type observation_columns: list
        :param intercept: (default=None)  The algorithm adds an intercept.
            Default is true.
        :type intercept: bool
        :param num_iterations: (default=None)  Number of iterations.
            Default is 100.
        :type num_iterations: int32
        :param step_size: (default=None)  Step size for optimizer.
            Default is 1.0.
        :type step_size: int32
        :param reg_type: (default=None)  Regularization L1 or L2.
            Default is L2.
        :type reg_type: unicode
        :param reg_param: (default=None)  Regularization parameter.
            Default is 0.01.
        :type reg_param: float64
        :param mini_batch_fraction: (default=None)  Mini batch fraction parameter.
            Default is 1.0.
        :type mini_batch_fraction: float64

        :returns: 
        :rtype: _Unit
        """
        return None


@doc_stub
def drop_frames(items):
    """
    Deletes the frame on the server.

    :param items: Either the name of the frame object to delete or the frame object itself
    :type items: [ str | frame object | list [ str | frame objects ]]
    """
    return None

@doc_stub
def drop_graphs(items):
    """
    Deletes the graph on the server.

    :param items: Either the name of the graph object to delete or the graph object itself
    :type items: [ str | graph object | list [ str | graph objects ]]
    """
    return None

@doc_stub
def drop_models(items):
    """
    Deletes the model on the server.

    :param items: Either the name of the model object to delete or the model object itself
    :type items: [ str | model object | list [ str | model objects ]]
    """
    return None

@doc_stub
def get_frame(identifier):
    """
    Get handle to a frame object.

    :param identifier: Name of the frame to get
    :type identifier: str | int

    :returns: frame object
    :rtype: Frame
    """
    return None

@doc_stub
def get_frame_names():
    """
    Retrieve names for all the frame objects on the server.

    :returns: List of names
    :rtype: list
    """
    return None

@doc_stub
def get_graph(identifier):
    """
    Get handle to a graph object.

    :param identifier: Name of the graph to get
    :type identifier: str | int

    :returns: graph object
    :rtype: Graph
    """
    return None

@doc_stub
def get_graph_names():
    """
    Retrieve names for all the graph objects on the server.

    :returns: List of names
    :rtype: list
    """
    return None

@doc_stub
def get_model(identifier):
    """
    Get handle to a model object.

    :param identifier: Name of the model to get
    :type identifier: str | int

    :returns: model object
    :rtype: Model
    """
    return None

@doc_stub
def get_model_names():
    """
    Retrieve names for all the model objects on the server.

    :returns: List of names
    :rtype: list
    """
    return None


del doc_stub