from __future__ import division
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.cross_validation import KFold
from sklearn.preprocessing import normalize
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics.pairwise import cosine_similarity
from word_embedding import get_labeled_text, count_vectorizer, tfidf_mat, reduce_mat, reduce_mat_nonneg
import numpy as np 

text_df = get_labeled_text()
labels = np.array(text_df['sentiment'])
doc_term_mat = tfidf_mat(count_vectorizer(text_df))
lsa_mat = reduce_mat(doc_term_mat)

def validate_nb_model(mat=doc_term_mat):
	model = MultinomialNB()
	kf = KFold(mat.shape[0], n_folds=10, shuffle=True)
	for train, test in kf:
		model.fit(mat[train], labels[train])
		print model.score(mat[test], labels[test])


def validate_rocchio_model(mat=lsa_mat):
	model = Rocchio()
	kf = KFold(mat.shape[0], n_folds=10, shuffle=True)
	for train, test in kf:
		model.fit(mat[train], labels[train])
		print model.score(mat[test], labels[test])


def validate_knn_model(mat=lsa_mat):
	model = KNeighborsClassifier()
	kf = KFold(mat.shape[0], n_folds=10, shuffle=True)
	for train, test in kf:
		model.fit(mat[train], labels[train])
		print model.score(mat[test], labels[test])


class Rocchio(object):
	def __init__(self):
		super(Rocchio, self).__init__()

	def fit(self, X, y):
		self.pos = normalize(np.sum(X[y==True], axis=0).reshape(1,-1))
		self.neg = normalize(np.sum(X[y==False], axis=0).reshape(1,-1))

		self.pos = normalize(self.pos)
		self.neg = normalize(self.neg)

	def score(self, X, y):
		normX = normalize(X)
		pos_sim = np.dot(normX, self.pos.T)
		neg_sim = np.dot(normX, self.neg.T)
		prediction = pos_sim > neg_sim
		compare = prediction.T==y.T
		score = np.sum(compare) / compare.shape[1]
		return score


if __name__ == '__main__':
	print "NB"
	validate_nb_model()

	print "Rocchio"
	validate_rocchio_model()

	print "KNN"
	validate_knn_model()
