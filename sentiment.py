from __future__ import division
import urllib
import csv
from string import punctuation

#Sentiment analysis code from http://nealcaren.web.unc.edu/an-introduction-to-text-analysis-with-python-part-3/ 

#get sentiment dictionaries

def getSentiment(text):
    files=['negative.txt','positive.txt']

    pos_sent = open("positive.txt").read()
    positive_words=pos_sent.split('\n')
    positive_counts=[]

    neg_sent = open('negative.txt').read()
    negative_words=neg_sent.split('\n')
    negative_counts=[]

    #get text to analyse

    positive_counter=0
    negative_counter=0

    for p in list(punctuation):
        text=text.replace(p,'').lower()

    words = text.split(' ')
    word_count=len(words)
    for word in words:
        if word in positive_words:
            positive_counter=positive_counter+1
        elif word in negative_words:
            negative_counter=negative_counter+1
        
    positive_count = positive_counter/word_count
    negative_count = negative_counter/word_count

    output={"positive":positive_count,"negative":negative_count}
    return output