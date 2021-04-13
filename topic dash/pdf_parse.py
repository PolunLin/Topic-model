
import pdfplumber
import string
import re
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import pickle


ws = WS("../../../data")
pos = POS("../../../data")
# ner = NER("..data")
with open('../../../data/dictionary/custom_dic.pkl', 'rb') as f:
    dictionary = pickle.load(f)

def pdf_paser(path):
    '''萃取pdf中的文字。
    
    parameters
    ----------
    path: str
        the path of PDF file
    
    Returns
    -------
    page_string: str
        string of pdf file
    '''
    with pdfplumber.open(path) as pdf:
        page_string = ""
        for page in pdf.pages:
            page_string =page_string + "\n" + page.extract_text()
    return page_string


def str_count(text):
    '''找出字串中的中英文、空格、數字、標點符號個數，同時判斷文本是否為錯誤文本、cid文本。
    
    parameters
    ----------
    text : string
        string of pdf file
    
    Returns
    -------
    doc_type : int
        the type of pdf file
    
    '''
    count_en = count_dg = count_sp = count_zh = count_pu = 0
    a = re.findall(r'\(cid:\d+\)', text)
    count_cid = 0
    doc_type = -1
    if len(a)>10:
        count_cid = 1
    else:
        for s in text:
            if s in string.ascii_letters: # 英文
                count_en += 1
            elif s.isdigit():  # 数字
                count_dg += 1
            elif s.isspace():  # 空格
                count_sp += 1
            elif s.isalpha():  # 中文，除了英文之外，剩下的字符认为就是中文
                count_zh += 1
            else:              # 特殊字符
                count_pu += 1
    if len(text)<100:
        doc_type = 0
    elif count_cid ==1:
        doc_type = 1
    elif count_zh/(count_en+0.001) <1 : # 中英比例
        doc_type = 2
    else :
        doc_type =3
    return doc_type
        

def segment_para(text):
    '''
    透過pdf的編寫特性(中文的段落分隔符號+空白字元+換行)，切出段落。
    
    
    parameters
    ----------
    text: string
        string of pdf file
    
    Returns
    -------
    seg_text : list
        The lists of paragraphs

    ''' 
    seg_text = []
    docu = re.split(r"[。!?;]\s\n\s?",text)
    dell = re.findall(r"[。!?;]\s\n\s?",text)
    dell.append("")
    for sen,delll in zip(docu,dell):
        seg_text.append(sen +delll)
    return seg_text


def remove_white(text):
    '''移除空白字元、移除換行字元。
    
    parameters
    ----------
    text: string
        string of pdf file
    
    Returns
    -------
    cl_doc: list
        lists of clean documents
    
    '''
    cl_doc =[]
    for para in text:
        para = re.sub("\n",'',para)
        para = re.sub(" +",' ',para) 
        para = para.strip()
        cl_doc.append(para)
    return cl_doc


def segment_word(cl_doc):
    '''透過CKIP套件進行斷詞
    
    parameters
    ----------
    cl_doc: list
        lists of clean documents
    
    Returns
    -------
    word_sentence_list: list
        lists of tokens of documents
    
    
    '''
    word_sentence_list = ws(cl_doc,coerce_dictionary = dictionary)
    return word_sentence_list
def pos_word(word_sentence_list):
    '''透過CKIP套件進行詞性萃取
    
    parameters
    ----------
    word_sentence_list: list
        lists of tokens of documents
    
    Returns
    -------
    pos_sentence_list: list
        lists of POS of documents
    
    
    '''
    pos_sentence_list = pos(word_sentence_list)
    return pos_sentence_list