import spacy 
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD, NMF
import pandas as pd 
import numpy as np 
from gensim.models import word2vec as w2v
import gensim
import pickle as pkl

nlp = spacy.load('en')
get_labeled_text = lambda : pd.read_csv('../data/text_sentiment.csv')

# Encode in Doc-Term matrix (data,(row,col))
def count_vectorizer(df):
	text_to_index = dict()
	dok = dict()
	for i, row in df.iterrows():
		dok[i] = dict()
		for word in row['text'].split():
			text_to_index[word] = text_to_index.get(word, len(text_to_index))
			dok[i][text_to_index[word]] = dok[i].get(text_to_index[word], 0) + 1
	coords = [(term, doc, count) for doc, term_dict in dok.items() for term, count in term_dict.items()]
	comp_list = zip(*coords)
	return csr_matrix((comp_list[2],(comp_list[0], comp_list[1]))).T


def tfidf_mat(mat):
	transformer = TfidfTransformer(sublinear_tf=True, use_idf=True)
	return transformer.fit_transform(mat)


def reduce_mat(mat):
	lsa = TruncatedSVD(n_components=100)
	return lsa.fit_transform(mat)


def reduce_mat_nonneg(mat):
	lsa = NMF(n_components=100)
	return lsa.fit_transform(mat)


def label_mat(mat, df):
	labels = np.resize(np.array(df['sentiment']), (len(df['sentiment']), 1))
	return hstack([mat, labels])


def train_w2v_model(df):
	model = w2v.Word2Vec(df['text'])
	print model.vocab
	model.save('w2v_model.bin')


def train_on_google_model(df):
	model = gensim.models.Word2Vec.load_word2vec_format('../data/GoogleNews-vectors-negative300.bin', binary=True)  
	doc_vectors = []
	for i, row in df.iterrows():
		doc_vector = np.average([model[word] for word in row['text'].split() if word in model], axis=0)
		doc_vectors.append(doc_vector)
	return np.vstack(tuple(doc_vectors))

if __name__ == '__main__':
	text_df = get_labeled_text()
	# mat = tfidf_mat(count_vectorizer(text_df))
	# label_mat(mat, text_df)
	# train_w2v_model(text_df)
	google_matrix = train_on_google_model(text_df)
	pkl.dump(google_matrix, open('../data/google_matrix.pkl', 'w'))
