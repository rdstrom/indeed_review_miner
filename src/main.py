import bs4 as bs
from bs4 import Comment
import time
import random
import re
import pandas as pd
import numpy as np
import urllib.request

review_df = pd.DataFrame()

review_star_dict = {
                    'width:3px': np.nan,
                    'width:15px': 1,
                    'width:27px': 2,
                    'width:39px': 3,
                    'width:51px': 4,
                    'width:63px': 5,
                    }

job_status_dict = {
                    ' Current Employee ' : True,
                    ' Former Employee ' : False
                    }

#Functions
def format_review_df(df):
    df['employeementStatus_flag'] = df['employeementStatus_flag'].replace(job_status_dict)
    df['reviewDate'] = df['reviewDate'].apply(lambda x: pd.to_datetime(x, infer_datetime_format=True, errors='coerce'))
    df['reviewRating_workLifeBal'] = df['reviewRating_workLifeBal'].replace(review_star_dict)
    df['reviewRating_payBenifits'] = df['reviewRating_payBenifits'].replace(review_star_dict)
    df['reviewRating_jobSecAdvance'] = df['reviewRating_jobSecAdvance'].replace(review_star_dict)
    df['reviewRating_management'] = df['reviewRating_management'].replace(review_star_dict)
    df['reviewRating_culture'] = df['reviewRating_culture'].replace(review_star_dict)
    return df

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

    #Review Date --Sometimes this returns location data which throws and error RS 2020-04-12
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
    
    #Review Sub Ratings (all in 1 list)
    for div in soup.find_all('div', class_ = 'cmp-SubRating'):
        for div in div.find_all('div', class_ = 'cmp-RatingStars-starsFilled'):
            print(div.get('style'))
            reviewSubAll_list.append(div.get('style'))
    
    #Splits list of all sub reviews into each catagory
    reviewRatingSub1_list = reviewSubAll_list[0::5]
    reviewRatingSub2_list = reviewSubAll_list[1::5]
    reviewRatingSub3_list = reviewSubAll_list[2::5]
    reviewRatingSub4_list = reviewSubAll_list[3::5]
    reviewRatingSub5_list = reviewSubAll_list[4::5]
 
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
                  reviewRatingSub1_list,
                  reviewRatingSub2_list,
                  reviewRatingSub3_list,
                  reviewRatingSub4_list,
                  reviewRatingSub5_list,
                  reviewBody_list,
                  helpfulReview_yes_list,
                  helpfulReview_no_list
                  )
    
    review_temp_df = pd.DataFrame(list(review_tuple))
    
    return review_temp_df

i = 0
end = 240
while i in range (0,end):
    url = ('https://www.indeed.com/cmp/John-Deere/reviews?start={0}').format(i)
    #url = ('https://www.indeed.com/cmp/JPMorgan-Chase/reviews?fcountry=ALL&start={0}').format(i)
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source,'lxml') 
    review_df = review_df.append(review_scrape(soup))
    i = i + 20
    time.sleep(random.randrange(10, 20))

review_df.columns = ['jobTitle', 
                      'employeementStatus_flag', 
                      'reviewDate', 
                      'reviewTitle',
                      'reviewRatingAll',
                      'reviewRating_workLifeBal',
                      'reviewRating_payBenifits',
                      'reviewRating_jobSecAdvance',
                      'reviewRating_management',
                      'reviewRating_culture',
                      'reviewBody',
                      'reviewHelpful_yes',
                      'reviewHelpful_no']

review_df_clean = format_review_df(review_df)
