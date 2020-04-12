import bs4 as bs
from bs4 import Comment
import re
import pandas as pd
import urllib.request

#source_link = "https://www.indeed.com/cmp/JPMorgan-Chase/reviews?fcountry=ALL&start={0}".format(loop_num)
source = urllib.request.urlopen('https://www.indeed.com/cmp/JPMorgan-Chase/reviews?fcountry=US').read()
soup = bs.BeautifulSoup(source,'lxml') 

def review_scrape(soup):
    
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
        reviewJobTitle_list.append(div.find('meta').get("content", None))

    #Review Date
    for div in soup.find_all('div', class_ = 'cmp-Review-author'):
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
            
            
    review_tuple = zip(
                  reviewJobTitle_list,
                  reviewEmployementStatus_list,
                  reviewDate_list,
                  reviewTitle_list,
                  reviewRatingAll_list,
                  reviewBody_list,
                  helpfulReview_yes_list,
                  helpfulReview_no_list
                  )
    
    return review_tuple

review_tuple = review_scrape(soup)

#Create Df
review_df = pd.DataFrame(list(review_tuple))

#Clean Pipe -- Should just turn this to a Bool Value
review_df[1] = review_df[1].apply(lambda x: re.sub(r'[^\w]', ' ', x))
review_df[1] = review_df[1].replace(' Current Employee ', True)
review_df[1] = review_df[1].replace(' Former Employee ', False)
review_df[2] = review_df[2].apply(lambda x: pd.to_datetime(x, infer_datetime_format=True))
