import pandas as pd
import nltk

abuse_words = ['abus', 'hit', 'beat', 'beaten', 'rape', 'punish', 'strap', 'sexual', 'physical', 'sex', 'touch', 'fondl', 'hurt', 'cri', ]


def get_abuse_count(text):
	p_stemmer = nltk.stem.PorterStemmer()
	word_count = 0
	abuse_count = 0
	for word in text.split():
		word = p_stemmer.stem(word)
		if word not in nltk.corpus.stopwords.words('english'):
			word_count += 1
			if word in abuse_words:
				abuse_count += 1


	if abuse_count > 0:
		to_return = abuse_count/word_count
	else:
		to_return = abuse_count

	return to_return


if __name__ == "__main__":
	df = pd.read_csv("transcripts2.csv", encoding = "ISO-8859-1")
	df['abuse_count'] = pd.Series()

	for index, row in df.iterrows():
		df['abuse_count'][index] = get_abuse_count(row['language_content'])


	#print(df)

	full = pd.read_csv("transcript_fullset.csv")

	df = df.rename(columns = {'name':'ID'})

	final_df = pd.merge(full, df, on=['ID'] )

	final_df.to_csv('final_data3.csv')

	#print(final_df)

