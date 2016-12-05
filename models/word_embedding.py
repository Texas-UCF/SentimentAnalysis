import spacy 
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd 

nlp = spacy.load('en')
get_labeled_text = lambda : pd.read_csv('../data/text_sentiment.csv')

# Encode in Term-Doc matrix (data,(row,col))
def sparse_td_matrix(df):
	text_to_index = dict()
	dok = dict()
	for i, row in df.iterrows():
		dok[i] = dict()
		for word in row['text'].split():
			text_to_index[word] = text_to_index.get(word, len(text_to_index))
			# print text_to_index
			dok[i][text_to_index[word]] = dok[i].get(text_to_index[word], 0) + 1
	coords = [(term, doc, count) for doc, term_dict in dok.items() for term, count in term_dict.items()]
	comp_list = zip(*coords)
	return csr_matrix((comp_list[2],(comp_list[0], comp_list[1])))

def tfidf_mat(mat):
	transformer = TfidfTransformer()
	return transformer.fit_transform(mat)

def label_mat(mat, df):
	coords = [(mat.shape[0], i, data) for i, data in enumerate(df['sentiment'])]
	labels = zip(*coords)
	label_col = csr_matrix(labels)
	print label_col.shape
	hstack([mat, label_col])

if __name__ == '__main__':
	text_df = get_labeled_text()
	mat = sparse_td_matrix(text_df)
	# print label_mat(mat, text_df)