import re
import os, sys

from django.utils.safestring import mark_safe

PWD = os.getenv('PWD')

os.chdir(PWD)
sys.path.insert(0, os.getenv('PWD'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")

import django

django.setup()

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from college.models import College

import nltk

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

from reviews.models import Review
from obito.constants import academics, placements, infrastructure


# Making the class for review sentiment analysis

class Analysis:

    def __init__(self, college):
        self.reviews = Review.objects.filter(college=college)

    def invoke(self):
        quadrants = []

        for s in self.reviews:
            quadrants = []

            self.lowercase(s)
            self.sanitization(s)
            reviews = self.splitting(s)

            a_list = self.academic(reviews)
            p_list = self.placement(reviews)
            i_list = self.infrastructure(reviews)

            if (len(reviews) > 0):
                # review.append(s.comment)

                if (len(a_list) > 0):
                    a_pos, a_neg, a_neu, a_compound = self.a_analysis(a_list)
                else:
                    a_pos, a_neg, a_neu, a_compound = 0, 0, 0, 0

                if (len(p_list) > 0):
                    p_pos, p_neg, p_neu, p_compound = self.p_analysis(p_list)
                else:
                    p_pos, p_neg, p_neu, p_compound = 0, 0, 0, 0

                if (len(i_list) > 0):
                    i_pos, i_neg, i_neu, i_compound = self.i_analysis(i_list)
                else:
                    i_pos, i_neg, i_neu, i_compound = 0, 0, 0, 0

                quadrant = [
                    {"statements": reviews, "metric": "PLACEMENT", "negative": p_neg, "positive": p_pos, "neutral": p_neu, "compound": p_compound},
                    {"statements": reviews, "metric": "ACADEMICS", "negative": a_neg, "positive": a_pos, "neutral": a_neu, "compound": a_compound},
                    {"statements": reviews, "metric": "INFRASTRUCTURE", "negative": i_neg, "positive": i_pos, "neutral": i_neu, "compound": i_compound}
                ]

                quadrants.append(quadrant)

            s.quadrants = quadrants
            print(f'Saved Quadrants for: {s.college.full_name}')
            s.save()

        return quadrants

    def lowercase(self, s):
        s.comment = s.comment.lower()
        s.save()

    def sanitization(self, s):
        try:
            s.comment = s.comment.replace("\n", " ")
            s.comment = s.comment.replace("\r", " ")
            s.comment = s.comment.replace("\t", " ")
            s.save()
        except:
            pass

    def splitting(self, s):
        lst = []
        regex = re.compile(r' [\w.()]{1,2}\.')
        rep = regex.sub(" ", s.comment)
        lst.extend(rep.split("."))
        reviews = [i for i in lst if i != '']
        return reviews

    def a_analysis(self, reviews):

        lst = [sid.polarity_scores(review) for review in reviews]
        pos_list = [score['pos'] for score in lst]
        neg_list = [score['neg'] for score in lst]
        neu_list = [score['neu'] for score in lst]
        compound_list = [score['compound'] for score in lst]

        pos = sum(pos_list) / len(pos_list)
        neg = sum(neg_list) / len(neg_list)
        neu = sum(neu_list) / len(neu_list)
        compound = sum(compound_list) / len(compound_list)

        return pos, neg, neu, compound

    def p_analysis(self, reviews):

        lst = [sid.polarity_scores(review) for review in reviews]
        pos_list = [score['pos'] for score in lst]
        neg_list = [score['neg'] for score in lst]
        neu_list = [score['neu'] for score in lst]
        compound_list = [score['compound'] for score in lst]

        pos = sum(pos_list) / len(pos_list)
        neg = sum(neg_list) / len(neg_list)
        neu = sum(neu_list) / len(neu_list)
        compound = sum(compound_list) / len(compound_list)

        return pos, neg, neu, compound

    def i_analysis(self, reviews):

        lst = [sid.polarity_scores(review) for review in reviews]
        pos_list = [score['pos'] for score in lst]
        neg_list = [score['neg'] for score in lst]
        neu_list = [score['neu'] for score in lst]
        compound_list = [score['compound'] for score in lst]

        pos = sum(pos_list) / len(pos_list)
        neg = sum(neg_list) / len(neg_list)
        neu = sum(neu_list) / len(neu_list)
        compound = sum(compound_list) / len(compound_list)

        return pos, neg, neu, compound

    def academic(self, reviews):
        a_list = []
        for l in reviews:
            for word in academics:
                if (l.find(word) != -1):
                    a_list.append(l)
                    break
        return a_list

    def placement(self, reviews):
        p_list = []
        for l in reviews:
            for word in placements:
                if (l.find(word) != -1):
                    p_list.append(l)
                    break
        return p_list

    def infrastructure(self, reviews):
        i_list = []
        for l in reviews:
            for word in infrastructure:
                if (l.find(word) != -1):
                    i_list.append(l)
                    break
        return i_list
