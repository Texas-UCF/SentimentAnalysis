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
import pickle as pkl

text_df = get_labeled_text()
labels = np.array(text_df['sentiment'])
doc_term_mat = tfidf_mat(count_vectorizer(text_df))
lsa_mat = reduce_mat(doc_term_mat)
google_matrix = pkl.load(open('../data/google_matrix.pkl', 'rb'))

def validate_nb_model(mat=doc_term_mat):
	model = MultinomialNB()
	kf = KFold(mat.shape[0], n_folds=10, shuffle=True)
	for train, test in kf:
		model.fit(mat[train], labels[train])
		print model.score(mat[test], labels[test])


def validate_rocchio_model(mat=lsa_mat, subtract=False):
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
	def __init__(self, subtract=False):
		super(Rocchio, self).__init__()
		self.subtract = subtract

	def fit(self, X, y):
		if self.subtract:
			self.pos = np.sum(X[y==True]).reshape(1,-1)
			self.pos += np.sum(-1 * X[y==False]).reshape(1,-1)
			self.neg = np.sum(X[y==False]).reshape(1,-1)
			self.neg += np.sum(-1 * X[y==True]).reshape(1,-1)

		else:
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
	print "Rocchio W2V"
	validate_rocchio_model(google_matrix, subtract=True)

	print "NB"
	validate_nb_model()

	print "Rocchio"
	validate_rocchio_model()

	print "KNN"
	validate_knn_model()
