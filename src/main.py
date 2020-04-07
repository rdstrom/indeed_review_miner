import bs4 as bs
from bs4 import Comment
import urllib.request

source = urllib.request.urlopen('https://www.indeed.com/cmp/JPMorgan-Chase/reviews?fcountry=US').read()
soup = bs.BeautifulSoup(source,'lxml') 

#Storage Lists
reviewJobTitle_list = []
reviewEmployementStatus_list = []
reviewDate_list = []
reviewTitle_list = []
reviewRatingAll_list = []

reviewSubAll_list = []
reviewRatingSub1_list = []
reviewRatingSub2_list = []
reviewRatingSub3_list = []
reviewRatingSub4_list = []
reviewRatingSub5_list = []

reviewBody_list = []

helpfulReview_all_list = []
helpfulReview_yes_list = []
helpfulReview_no_list = []



#Review Job Title
for div in soup.find_all('div', class_ = 'cmp-Review-author'):
    reviewJobTitle_list.append(div)

#Review Date
for div in soup.find_all('div', class_ = 'cmp-Review-author'):
    print(div)
    reviewDate_list.append(div.find_all(string=lambda text: isinstance(text, Comment))[2].next_element.strip())

#Current/Former Employee
for div in soup.find_all('div', class_ = 'cmp-Review-author'):
    reviewEmployementStatus_list.append(div.find_all(string=lambda text: isinstance(text, Comment))[0].next_element.strip())
    
#Review Title
for div in soup.find_all('div', class_ = 'cmp-Review-title'):
    reviewTitle_list.append(div.text) 
        for comment in div.find_all(text=lambda text: isinstance(text, Comment) and text in comments_to_search_for):
        print(comment.next_element.strip())
    
#Review Rating All
for div in soup.find_all('div', class_ = 'cmp-ReviewRating-text'):
    reviewRatingAll_list.append(div.text)
    
#Review Sub Ratings (remove top 1 the assign every 5 per catagory)
for div in soup.find_all('div', class_ = 'cmp-RatingStars-starsFilled'):
    reviewSubAll_list.append(div.get('style'))
    #Need lambda to use .get('style'), then use regex to return numeric value
    
#itemprop="reviewBody"

for span in soup.find_all('span', itemprop = 'reviewBody'):
    reviewBody_list.append(span.text)

#Helpful Review - Yes/No #This needs work

for button in soup.find_all('button', class_ = 'icl-Button icl-Button--tertiary icl-Button--sm icl-Button--group'):
    try:
        helpfulReview_all_list.append(button.find('span', class_ = 'cmp-StatelessReviewFeedbackButtons-count').text)
    except:
        helpfulReview_all_list.append(0)
        
#This is a janky way of handling this
for i in range(0,len(helpfulReview_all_list)):
    if (i+1)%2 == 0:
        helpfulReview_no_list.append(helpfulReview_all_list[i])
    else:
        helpfulReview_yes_list.append(helpfulReview_all_list[i])
