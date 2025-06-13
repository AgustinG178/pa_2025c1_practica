from modules.text_vectorizer import TextVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted


class ClaimsClassifier(BaseEstimator, ClassifierMixin):
    
    def __init__(self):
        pass

    def fit(self, X, y):
        # X, y = check_X_y(X, y, accept_sparse=True) #No lo puedo usar con strings
        self.encoder_ = LabelEncoder()
        y = self.encoder_.fit_transform(y)
        pipe = Pipeline([
            ('vectorizer', TextVectorizer()),
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(max_depth=20, max_features='log2', n_estimators=10))
        ])
        self.clf_ = pipe.fit(X, y)
        if self.clf_:
            self.is_fitted_ = True
        return self
    
    def predict(self, X):
        check_is_fitted(self)
        # X = check_array(X, accept_sparse=True)
        return self.encoder_.inverse_transform(self.clf_.predict(X))
    
    def clasificar(self, X):
        """Clasifica una lista de reclamos
        Args:
            X (List): Lista de reclamos a clasificar, el formato de cada reclamo debe ser un string
        Returns:
            clasificación: Lista con las clasificaciones de los reclamos, el formato de cada clasificación es un string
            los valores posibles dependen de las etiquetas en y usadas en el entrenamiento
        """
        return self.predict(X)