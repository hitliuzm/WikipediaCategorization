import os
import numpy as np
import languageProcess as lp
from gensim import corpora,similarities,models
from gensim.models import LsiModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class LSIsimilarity:
    def __init__(self):
        self.articles=[]
        #path = '/home/kdane/Desktop/Computationaltools/WikipediaCategorization-master/WikipediaCategorization-master/Baseline/plaindata1'
        path = '../Baseline/plaindata'
        self.categories=os.listdir(path)
        #Save all base articles in an array of arrays
        for cat in self.categories:
            filepath = path+"/"+cat+"/AA/wiki_00"
            self.articles += [lp.languageProcess(filepath).getWords()]
     #This function will train the model only once and then it will simply load the model from memory and  perform comparison.
    def display(self, category, sim_value):
        if(sim_value < 0):
            sim_value*=-1
        print(category, " -->",sim_value*100 , "%")

    def compare(self, quary):
        #Check if the dictionary/corpus/index is already created if so load it donot create a new one
        if (os.path.exists("dictionary1.dict")):
            dictionary1 = corpora.Dictionary.load("dictionary1.dict")
            corpus1 = corpora.MmCorpus("corpus.mm1")
            index1 = similarities.MatrixSimilarity.load('myindex.index')
         #If the dictionary/corpus/index is not already created create a new one and save it.
        else:
            dictionary1 = corpora.Dictionary(self.articles)
            dictionary1.save("dictionary1.dict")
            corpus1 = [dictionary1.doc2bow(text) for text in self.articles]
            corpora.MmCorpus.serialize("corpus.mm1", corpus1)
            tfidf = models.TfidfModel(corpus1)
            corpus_tfidf = tfidf[corpus1]
            lsi = models.LsiModel(corpus_tfidf, id2word=dictionary1, num_topics=27)
            index1 = similarities.MatrixSimilarity(lsi[corpus1])
            index1.save('myindex.index')
        #Compute the tf*idf/lsi/and index
        tfidf = models.TfidfModel(corpus1)
        corpus_tfidf = tfidf[corpus1]
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary1, num_topics=27)
        #Vectorize your quary doc with ur dictionary
        self.quary_path=dictionary1.doc2bow(quary.lower().split())
        vec_lsi = lsi[self.quary_path]
        #Compute similarity of the quary document to base articles(model)
        sims = index1[vec_lsi]
        sims=list(enumerate(sims))
        #Visualize the result in percentage for better readability
        for i in range(0, len(self.categories)):
            self.display(self.categories[i],sims[i][1])
            #print(self.categories[i], " -->",sims[i][1]*100 , "%")
#This is a document about Education, I copied it from wikipedia.
quary_edu="Effective education is a learning experience.Education brings about an inherent and permanent change in a person's thinking and capacity to do things.Many people have a superficial concept of education; equating it with doing a particular course or obtaining a particular qualification.Qualifications and courses however do not always equate with effective education.People can undertake courses without any significant permanent change People can achieve qualifications without changing How Good is a Qualification? There's no escaping the fact that good learning takes time.Reading a book and understanding what you read, does not mean that you have been educated or permanently changedif you don't integrate what you read into your attitudes and memory. Similarly, attending a course and hearing a lecture doesn't mean you have changed or been educated.Real education is very different to just having access to (or being exposed to) information about something. Real education embeds things into one's brain, and anyone who understands learning will understand that this comes from repeated exposure and use of information or skills.Sadly, in today's world, people want to fast track everything: but learning is something that cannot usually be fast tracked.Shorter courses simply mean that less is learnt."
#This is a document from Wikipedia about universe
quary_uni="The Universe is all of space and time[a] and their contents,[10] including planets, stars, galaxies, and all other forms of matter and energy. While the spatial size of the entire Universe is still unknown,[3] it is possible to measure the observable universe.The earliest scientific models of the Universe were developed by ancient Greek and Indian philosophers and were geocentric, placing Earth at the centre of the Universe.[11][12] Over the centuries, more precise astronomical observations led Nicolaus Copernicus to develop the heliocentric model with the Sun at the centre of the Solar System. In developing the law of universal gravitation, Sir Isaac Newton built upon Copernicus' work as well as observations by Tycho Brahe and Johannes Kepler's laws of planetary motion. Further observational improvements led to the realization that our Sun is one of hundreds of billions of stars in a galaxy we call the Milky Way, which is one of at least hundreds of billions of galaxies in the Universe. Many of the stars in our galaxy have planets. At the largest scale galaxies are distributed uniformly and the same in all directions, meaning that the Universe has neither an edge nor a center. At smaller scales, galaxies are distributed in clusters and superclusters which form immense filaments and voids in space, creating a vast foam-like structure.[13] Discoveries in the early 20th century have suggested that the Universe had a beginning and that space has been expanding since then,[14] and is currently still expanding at an increasing rate.[15]The Big Bang theory is the prevailing cosmological description of the development of the Universe. Under this theory, space and time emerged together 13.799±0.021 billion years ago[2] with a fixed amount of energy and matter that has become less dense as the Universe has expanded. After an initial accelerated expansion at around 10−32 seconds, and the separation of the four known fundamental forces, the Universe gradually cooled and continued to expand, allowing the first subatomic particles and simple atoms to form. Dark matter gradually gathered forming a foam-like structure of filaments and voids under the influence of gravity. Giant clouds of hydrogen and helium were gradually drawn to the places where dark matter was most dense, forming the first galaxies, stars, and everything else seen today. It is possible to see objects that are now further away than 13.799 billion light-years because space itself has expanded, and it is still expanding today. This means that objects which are now up to 46 billion light years away can still be seen in their distant past, because in the past when their light was emitted, they were much closer to the Earth. From studying the movement of galaxies, we know that the universe contains much more matter than we can detect in usual ways. This unseen matter is known as dark matter [16] (dark means that there is a wide range of strong indirect evidence that it exists, but we have not yet detected it directly). The Lambda-CDM model is the most widely accepted model of our universe. It suggests that about 69.2%±1.2% [2015] of the mass and energy in the universe is a scalar field known as dark energy which is responsible for the current expansion of space, and about 25.8% [2015] is dark matter.[17] Ordinary matter is therefore only 4.9% [2015] of the physical universe.[17] Stars, planets, and visible gas clouds only form about 6% of ordinary matter, or about 0.3% of the entire universe.[18] There are many competing hypotheses about the ultimate fate of the universe and about what, if anything, preceded the Big Bang, while other physicists and philosophers refuse to speculate, doubting that information about prior states will ever be accessible. Some physicists have suggested various multiverse hypotheses, in which the Universe might be one among many universes that likewise exist.[3][19][20]"
quart_sport="Sport (British English) or sports (American English) includes all forms of competitive physical activity or games which,[1] through casual or organised participation, aim to use, maintain or improve physical ability and skills while providing enjoyment to participants, and in some cases, entertainment for spectators.[2] Hundreds of sports exist, from those between single contestants, through to those with hundreds of simultaneous participants, either in teams or competing as individuals. In certain sports such as racing, many contestants may compete, simultaneously or consecutively, with one winner; in others, the contest (a match) is between two sides, each attempting to exceed the other. Some sports allow a tie game; others provide tie-breaking methods to ensure one winner and one loser. A number of contests may be arranged in a tournament producing a champion. Many sports leagues make an annual champion by arranging games in a regular sports season, followed in some cases by playoffs. Sport is generally recognised as system of activities which are based in physical athleticism or physical dexterity, with the largest major competitions such as the Olympic Games admitting only sports meeting this definition,[3] and other organisations such as the Council of Europe using definitions precluding activities without a physical element from classification as sports.[2] However, a number of competitive, but non-physical, activities claim recognition as mind sports. The International Olympic Committee (through ARISF) recognises both chess and bridge as bona fide sports, and SportAccord, the international sports federation association, recognises five non-physical sports: bridge, chess, draughts (checkers), Go and xiangqi,[4][5] and limits the number of mind games which can be admitted as sports.[1] Sport is usually governed by a set of rules or customs, which serve to ensure fair competition, and allow consistent adjudication of the winner. Winning can be determined by physical events such as scoring goals or crossing a line first. It can also be determined by judges who are scoring elements of the sporting performance, including objective or subjective measures such as technical performance or artistic impression. Records of performance are often kept, and for popular sports, this information may be widely announced or reported in sport news. Sport is also a major source of entertainment for non-participants, with spectator sport drawing large crowds to sport venues, and reaching wider audiences through broadcasting. Sport betting is in some cases severely regulated, and in some cases is central to the sport."
lsa =LSIsimilarity()
print("This a bout education quary-------------------------------------------------------------------------------")
lsa.compare(quary_edu)
print("This a bout universe quary-------------------------------------------------------------------------------")
lsa.compare(quary_uni)
print("This a bout Sport quary-------------------------------------------------------------------------------")
lsa.compare(quart_sport)
