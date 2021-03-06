
import re
import jieba
import gensim
from gensim import corpora, models
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def SentenceSegmentation(text):
	"""
	给定一段文本，将文本分割成若干句子。
	这里简单使用句号、问号、感叹号以及换行符进行分割。
	"""
	sentences = re.split(u'[\n。？！]', text)
	sentences = [sent for sent in sentences if len(sent) > 0]  # 去除只包含\n或空白符的句子
	return sentences
	
def LoadStopWords(stopfile):
	"""
	载入停用词文件
	"""
	stop_words = set() # 保存停用词集合
	fin = open(stopfile, 'r', encoding='utf-8', errors='ignore')
	for word in fin.readlines():
		stop_words.add(word.strip())
	fin.close()
	return stop_words

	
def WordSegmentation(text, stop_words):
	"""
	利用jieba分词工具来进行词分割
	同时过滤掉文本中的停用词
	"""
	jieba_list = jieba.cut(text)
	word_list = []
	for word in jieba_list:
		if word not in stop_words:
			word_list.append(word)
	return word_list

def GenDocument(filename):
	"""
	读入给定的文档，将文本进行预处理
	去除停用词
	"""
	document = []
	filename = '.\mongeostore_env\ch22\\'+ filename 
	fin = open(filename, 'r', encoding='utf-8', errors='ignore')
	sentences = []
	for line in fin.readlines():
		sentences.append(line.strip())
	fin.close()

	stop_words = LoadStopWords('.\mongeostore_env\ch22\stopwords.txt')
	
	for sent in sentences:
		results = jieba.cut(sent.strip())
		for item in results:
			if (not item in stop_words) and (not len(item.strip()) == 0):
				document.append(item)
	return document	

def TopicModeling(n):
	"""
	讲读入的文本利用话题模型LDA进行处理
	得出每个话题以及每个话题中对应的概率最高的词
	"""
	texts = []
	for i in range(10):
		doc = GenDocument(str(i + 1) + '.txt')
		texts.append(doc)
	
	#利用gensim将载入的文本文件构造成词-词频(term-frequency)矩阵
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	#将term-frequency矩阵作为输入，利用LDA进行话题分析
	lda = gensim.models.ldamodel.LdaModel(corpus, num_topics=n, id2word = dictionary, passes=20)
	
	topics = []
	for tid in range(n):
		wordDict = {}
		#选出每个话题中最具代表性的前15个词
		topicterms = lda.show_topic(tid, topn=15)
		for item in topicterms:
			(w, p) = item
			#由于LDA保留的每个词属于该话题的概率值p
			#该概率值本身较小，这里为了方便可视化，将概率p进一步放大
			wordDict[w] = (p*100)**2
		topics.append(wordDict)
	return topics
	
def GenWordCloud(wordDict):
	"""
	利用词云工具Word Cloud为每个话题生成词云
	"""
	#由于原始WordCloud不支持中文，这里需要载入中文字体文件simsun.ttc
	cloud = WordCloud(font_path='simsun.ttc', background_color='white', max_words=300, max_font_size=40, random_state=42)
	wordcloud = cloud.generate_from_frequencies(wordDict)
	plt.figure()
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.show()
	
def main():
	#设定话题数目为3
	numOfTopics = 3
	topics = TopicModeling(numOfTopics)
	for i in range(numOfTopics):
		GenWordCloud(topics[i])
		
main()