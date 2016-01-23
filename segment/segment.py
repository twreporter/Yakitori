# -*- coding: utf-8 -*-

import json
import jieba

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
                       else: 
                           last_uni = seg  
                   else: 
                       result += seg 
                       result += ' '
                       last_uni = ' '
    return result 


def main():
    af  = open('../data/articles', 'r')
    sf  = open('/tmp/articles_seg', 'wr')
    for line in af: 
        ja = json.loads(line)
        for a in ja: 
            story = a['story']
            processed = segment(story)
            sf.write(processed.encode('utf-8'))

if __name__ == "__main__":
    main()

 
