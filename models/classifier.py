from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.cross_validation import KFold
from word_embedding import get_labeled_text, sparse_td_matrix, tfidf_mat, reduce_mat
import numpy as np 

model = MultinomialNB()

def validate_model():
	text_df = get_labeled_text()

	# mat = sparse_td_matrix(text_df)
	mat = tfidf_mat(sparse_td_matrix(text_df))
	# mat = reduce_mat(tfidf_mat(sparse_td_matrix(text_df)))

	labels = np.array(text_df['sentiment'])
	kf = KFold(mat.shape[0], n_folds=10, shuffle=True)

	for train, test in kf:
		model.fit(mat[train], labels[train])
		print model.score(mat[test], labels[test])

if __name__ == '__main__':
	validate_model()