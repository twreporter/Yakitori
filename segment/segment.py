# -*- coding: utf-8 -*-

import json
import jieba
from collections import defaultdict
from pprint import pprint
from gensim import corpora, models, similarities
punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…／''')
def segment(full_str):
    last_set = 0
    result = ''
    for i, x in enumerate(full_str):
        if x in punct:
           sentence = full_str[last_set:i]
           last_set = i+1
           last_uni = ''
           if sentence:
               segs = jieba.cut(sentence, cut_all=False)
               for seg in segs:
                   if len(seg) < 2:
                       if last_uni:
                           seg = last_uni + seg
                       last_uni = seg
                   else:
                       last_uni = ''
                   if len(seg) >=2 :
                       result += seg
                       result += ' '
    return result

def make_dictionary(documents):
    texts = [[word for word in document.lower().split()] for document in documents ]
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
              for text in texts]
    dictionary = corpora.Dictionary(texts)
    print(dictionary)
    return dictionary


def main():
    af  = open('../data/articles', 'r')
    sf  = open('/tmp/articles_seg', 'wr')
    documents = []
    for line in af:
        ja = json.loads(line)
        for a in ja:
            story = a['story']
            print story
            processed = segment(story)
            documents.append(processed)
            sf.write(processed.encode('utf-8')+"\n")
    sf.close()
    dictionary = make_dictionary(documents)
    corpus = [dictionary.doc2bow(document.split()) for document in documents]
    corpora.MmCorpus.serialize('/tmp/twreporter.mm', corpus)
    tfidf = models.tfidfmodel.TfidfModel(corpus=corpus)
    index = similarities.MatrixSimilarity(tfidf[corpus])
    doc = "希特勒《我的奮鬥》─不是禁書，也不再是禁忌"
    query = segment(doc.decode('utf-8'))
    vec_bow = dictionary.doc2bow(query.split())
    print vec_bow
    vec_tfidf  = tfidf[vec_bow]
    sims = index[vec_tfidf] 
    print(list(enumerate(sims))) 
    #model=models.LsiModel
    #topic_model = model(tfidf[corpus], id2word=dictionary, num_topics=20)
    #for topic in topic_model.print_topics():
    #    print  topic[0]
    #    print  topic[1].encode('utf-8')
    #    print  '\n'



if __name__ == "__main__":
    main()


