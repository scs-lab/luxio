import sys,os
import matplotlib.pyplot as plt

from .behavior_classifier import BehaviorClassifier
from luxio.common.configuration_manager import *
from luxio.mapper.models.common import *
from luxio.mapper.models.regression.forest.random_forest import RFERandomForestRegressor
from luxio.mapper.models.metrics import r2Metric, RelativeAccuracyMetric, RelativeErrorMetric
from luxio.mapper.models.transforms.transformer_factory import TransformerFactory
from luxio.mapper.models.transforms.log_transformer import LogTransformer
from luxio.mapper.models.transforms.chain_transformer import ChainTransformer
from luxio.mapper.models.dimensionality_reduction.dimension_reducer_factory import DimensionReducerFactory

from sklearn.preprocessing import MinMaxScaler, RobustScaler
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.cluster import KMeans

from sklearn.metrics import davies_bouldin_score

import pprint, warnings
pp = pprint.PrettyPrinter(depth=6)
pd.options.mode.chained_assignment = None

class StorageClassifier(BehaviorClassifier):
    def __init__(self, features, mandatory_features, output_vars, score_conf, dataset_path, random_seed=132415, n_jobs=4):
        super().__init__(features, mandatory_features, [], score_conf, dataset_path, random_seed, n_jobs)
        self.sslos_ = None #A dataframe containing: means, stds, ns

    def feature_selector(self, X, y):
        self.feature_selector_ = None
        self.feature_importances_ = np.array([1]*len(self.features)) / len(self.features)
        self.features_ = self.features
        self.named_feature_importances_ = pd.DataFrame([(feature, importance) for feature, importance in zip(self.features_, self.feature_importances_)])

    def fit(self, X:pd.DataFrame=None, k=None):
        # Initialize scoring data
        self.score_features_ = list(self.features_)
        self.score_feature_weights_ = pd.DataFrame(
            dict([(feature, weight) for feature, weight in zip(self.features_, self.feature_importances_)]),
            index=[0]
        )
        self._init_scoring()
        #Cluster data
        self.transform_ = MinMaxScaler().fit(X[self.score_features_])
        self.sslos_ = self.standardize(X)
        X_features = self.transform_.transform(self.sslos_[self.score_features_])
        if k is None:
            for k in [4, 6, 8, 10, 12, 15, 20]:
                self.model_ = KMeans(n_clusters=k)
                self.labels_ = self.model_.fit_predict(X_features)
                print(f"SCORE k={k}: {self.score(X_features, self.labels_)} {self.model_.inertia_}")
            k = int(input("Optimal k: "))
        self.model_ = KMeans(n_clusters=k)
        self.labels_ = self.model_.fit_predict(X_features)
        self.sslos_ = self._create_groups(self.sslos_, self.labels_)
        self.sslos_.rename(columns={"labels":"sslo_id"}, inplace=True)
        self.sslo_to_deployment_ = X
        self.sslo_to_deployment_.loc[:,"sslo_id"] = self.labels_
        return self

    def score(self, X:pd.DataFrame, labels:np.array) -> float:
        return davies_bouldin_score(X, labels)

    def analyze_classes(self, df=None, dir=None):
        super().analyze_classes(self.sslos_, 'sslo_id', df=df, dir=dir)

    def visualize(self, df, path=None):
        df = self.standardize(df)
        super().visualize(df, self.score_features_, n_iters=[1000])

    def get_magnitude(self, io_identity):
        return super().get_magnitude(io_identity, self.sslos_)

    def get_coverages(self, io_identifier:pd.DataFrame, sslos:pd.DataFrame=None) -> pd.DataFrame:
        """
        Get the extent to which an sslos is covered by each sslo
        sslos: Either the centroid of an app class or the signature of a unique application
        """
        if sslos is None:
            sslos = self.sslos_
        #Get the coverage between io_identifier and the sslos
        coverage = 1 - (sslos[self.score_names_] - io_identifier[self.score_names_].to_numpy())
        #Add features
        coverage.loc[:,self.features_] = sslos[self.features_].to_numpy()
        coverage.loc[:,'sslo_id'] = sslos['sslo_id']
        #Get the magnitude of the fitnesses
        coverage.loc[:,"magnitude"] = self.get_magnitude(coverage)
        return coverage
