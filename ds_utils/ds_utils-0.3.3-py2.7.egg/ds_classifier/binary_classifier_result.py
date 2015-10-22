import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
from sklearn.metrics import roc_curve, auc


class BinaryClassifierResult:
    """
    Some useful methods for looking at the results of a binary classifier
    """
    def __init__(self, classifier_df):
        """
        Results of the binary classifier are represented as a DataFrame
        with a probability column (probability of signal) and
        a truth column (TRUE/FALSE or 1/0 for signal/background)
        :param classifier_df: DataFrame of results from classifier
        """
        if not isinstance(classifier_df, pd.DataFrame):
            raise ValueError("Error: 'classifier_df' must be a pandas DataFrame")

        if 'probability' not in classifier_df.columns or 'truth' not in classifier_df.columns:
            raise ValueError("DataFrame for {0} must have columns for 'probability' and 'truth'".format(self.__class__))

        # If truth is not a boolean, make it so
        if classifier_df.truth.dtype in [np.int32, np.int64]:
            classifier_df.truth = classifier_df.truth.astype(np.bool)

        self._classifier_df = classifier_df

    def accuracy(self, cutoff=0.5):
        """
        Get the accuracy of the classifier
        :param cutoff: all entries with probability >= cutoff will be predicted as signal
        :return: accuracy at the provided cutoff
        """
        return ((self._classifier_df.probability >= cutoff) == self._classifier_df.truth).mean()

    def precision(self, cutoff=0.5):
        """
        Get the precision of the classifier
        :param cutoff: all entries with probability >= cutoff will be predicted as signal
        :return: precision at the provided cutoff
        """
        predicted_signal = self._classifier_df.probability >= cutoff

        # if we didn't say anything was signal, 100% :)
        if not predicted_signal.any():
            return 1

        return self._classifier_df.truth[predicted_signal].mean()

    def recall(self, cutoff=0.5):
        """
        Get the recall of the classifier
        :param cutoff: all entries with probability >= cutoff will be predicted as signal
        :return: recall at the provided cutoff
        """
        # if there are no rows that have signal, then you didn't miss any
        if not self._classifier_df.truth.any():
            return 1

        return (self._classifier_df.probability[self._classifier_df.truth] >= cutoff).mean()

    def plot_apr(self, img_file=None):
        """
        Plots accuracy, precision, and recall
        :param img_file: file name to save img to, set to None to not save a file
        """
        fig, (acc, pre, rec) = plt.subplots(3, 1)

        self._plot_stat(self.accuracy, acc, 'Accuracy')
        self._plot_stat(self.precision, pre, 'Precision')
        self._plot_stat(self.recall, rec, 'Recall')
        fig.subplots_adjust(hspace=0.5)

        if img_file is not None:
            plt.savefig(img_file)
        plt.show()

    def _plot_stat(self, stat_fn, ax, title):
        """
        Puts the plot of a statistic vs the probability cutoff on axes
        :param stat_fn: function for the statistic to plot
        :param ax: matplotlib axis
        :param title: title of the plot
        """
        sorted_prob = sorted(self._classifier_df.probability)
        sorted_prob = [0] + sorted_prob + [1]
        values = []
        for cutoff in sorted_prob:
            values.append(stat_fn(cutoff))

        ax.plot(sorted_prob, values)
        ax.set_ylim(0, 1)
        ax.set_title(title)

    def plot_roc(self, img_file=None):
        """
        Plots ROC curve
        :param img_file: file name to save img to, set to None to not save a file
        """
        false_pos, true_pos, _ = roc_curve(self._classifier_df.truth, self._classifier_df.probability)
        roc_auc = auc(false_pos, true_pos)

        pl.clf()
        pl.plot(false_pos, true_pos, label='ROC curve (area = %0.2f)' % roc_auc)
        pl.plot([0, 1], [0, 1], 'k--')
        pl.xlim([0.0, 1.0])
        pl.ylim([0.0, 1.0])
        pl.xlabel('False Positive Rate')
        pl.ylabel('True Positive Rate')
        pl.title('ROC')
        pl.legend(loc="lower right")

        if img_file is not None:
            pl.savefig(img_file)
        pl.show()

    def get_confusion(self, cutoff=0.5):
        """
        Computes counts of true positives, false positives,
        true negatives, and false negatives at a
        given cutoff probability
        :param cutoff: prediction cutoff probability
        :return: dict containing elements of confusion matrix
        """
        tp = ((self._classifier_df.probability > cutoff) & self._classifier_df.truth).sum()
        fp = ((self._classifier_df.probability > cutoff) & ~self._classifier_df.truth).sum()
        tn = ((self._classifier_df.probability < cutoff) & ~self._classifier_df.truth).sum()
        fn = ((self._classifier_df.probability < cutoff) & self._classifier_df.truth).sum()
        return dict(true_pos=tp, false_pos=fp, true_neg=tn, false_neg=fn)

    def plot_confusion_matrix(self, cutoff=0.5, img_file=None):
        """
        Plots the confusion matrix at a given cutoff
        :param cutoff:  prediction cutoff probability
        :param img_file: file name to save img to, set to None to not save a file
        """
        confusion = self.get_confusion(cutoff)
        tp = confusion['true_pos']
        fp = confusion['false_pos']
        tn = confusion['true_neg']
        fn = confusion['false_neg']

        plt.matshow(np.array([[tn, fn], [fp, tp]]), cmap=plt.cm.get_cmap('Blues'))

        plt.title('Confusion Matrix')
        tick_marks = np.array([0, 1])
        plt.xticks(tick_marks, np.array(['Background', 'Signal']))
        plt.yticks(tick_marks, np.array(['Predicted Background', 'Predicted Signal']))

        plt.text(0, 0, str(tn), fontsize=14)
        plt.text(1, 0, str(fn), fontsize=14)
        plt.text(0, 1, str(fp), fontsize=14)
        plt.text(1, 1, str(tp), fontsize=14)

        if img_file is not None:
            plt.savefig(img_file)
        plt.show()
