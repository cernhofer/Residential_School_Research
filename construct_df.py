import pandas as pd 



if __name__ == "__main__":
	sent_df = pd.read_csv("joined2.csv")
	ind_df = pd.read_csv("trans_sent_num.csv", encoding = "ISO-8859-1")
	ind_df = ind_df.rename(columns = {'name':'ID'})
	abuse_df = pd.DataFrame(columns = ['ID', 'abuse'])

	full = pd.read_csv("transcript_fullset.csv")

	ID = 1
	abuse_count = 0
	sent_count = 0
	for index, row in sent_df.iterrows():
		if int(row['ID']) == ID:
			sent_count += 1
			abuse_count += row["abuse"]
		else:
			abuse_df.set_value(ID, 'abuse', abuse_count/sent_count)
			abuse_df.set_value(ID, 'ID', ID)
			sent_count = 1
			abuse_count = 0
			ID = int(row["ID"])


	result_df = pd.merge(ind_df, abuse_df, on=['ID'])

	final_df = pd.merge(full, result_df, on=['ID'] )

	final_df.to_csv('final_data.csv')