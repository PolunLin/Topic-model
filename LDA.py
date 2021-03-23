import pandas as pd ## data io
import pickle 
# load data
import glob
import time as tm
import pdfplumber ## read pdf
import re ## clean data for regex
import argparse
## gensim 
import gensim
from gensim import corpora
import pyLDAvis.gensim # LDAvis
from datetime import datetime
import os


def Load_data(doc):
    with open(f'../data/LDA_data/{doc}', 'rb') as f:
         doc = pickle.load(f)
    return doc


def create_path(top_num,doc):

    today = datetime.now()
    h = str(today.hour)
    path = "../data/LDA_data/" + today.strftime('%Y%m%d')+ h + "_"+ str(doc)[:-4] +"_" +str(top_num) ## 2021032313_file_topum remove .pkl  
    os.mkdir(path)
    return path

def Train_LDA(LDA_data_path,doc,top_num,seed):

    dictionary =corpora.Dictionary(doc)  #透過gensim以text_data建立字典
    corpus = [dictionary.doc2bow(text) for text in doc]#語料庫

    pickle.dump(corpus,open(f'{LDA_data_path}/corpus.pkl','wb'))#將字典存下未來使用
    dictionary.save(f'{LDA_data_path}/dictionary.gensim')

    ldamodel = gensim.models.ldamodel.LdaModel(\
        corpus,num_topics = top_num ,id2word=dictionary,passes=15,random_state = seed)
    ldamodel.save(f'{LDA_data_path}/model5.gensim')

    topics = ldamodel.print_topics(num_words=4)
    for topic in topics:
        print(topic)
    return dictionary,corpus,ldamodel

def LDAvis(ldamodel,corpus,dictionary,LDA_data_path):

    lda_display = pyLDAvis.gensim.prepare(ldamodel,corpus,dictionary,sort_topics=False)
    pyLDAvis.save_html(lda_display, f'{LDA_data_path}/lda.html')
    pyLDAvis.display(lda_display)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
      description =__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--doc', help="tokenized document list data type pickle (folder:YOUR_DOC_NAME)", type=str, default = 'Step2_clean_data.pkl')
    # parser.add_argument('--LDA_data_path', help="Save LDA data (1, dictionary,2, corpus,3, ldamodel) path LDA_PATH/your_LDA_data", type=str, default = 'LDA_data')
    parser.add_argument('--top_num', help="Define your number of topic model", type=int, default = 5)
    parser.add_argument('--seed', help="Define your random state ",type=int, default = 12345)
    args = parser.parse_args()


    print(f"run LDA topic(num:{args.top_num}) model")
    doc = Load_data(args.doc)
    path = create_path(args.top_num,args.doc)
    dictionary,corpus,ldamodel = Train_LDA(path,doc,args.top_num,args.seed)
    LDAvis(ldamodel,corpus,dictionary,path)
