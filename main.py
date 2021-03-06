
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[164]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[165]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[166]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    lineList = [line.rstrip('\n') for line in open('university_towns.txt')]
    
    state_town = []
    
    for i in lineList:
        if 'edit' in i:
            state = i[:-6].strip()
            
        elif '(' in i:
            town = i.partition('(')[0].strip()
            state_town.append([state, town])
        else:
            town = i.strip()
            state_town.append([state,town])
        
    x = pd.DataFrame(state_town, columns=["State", "RegionName"])
            
    return x
get_list_of_university_towns()


# In[167]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    GDP = pd.read_excel('gdplev.xls', skiprows=219)
    
    t = GDP[9926.1]
    
    for i in range(len(t)-1):
        if t.iloc[i+1] < t.iloc[i] and t.iloc[i+2] < t.iloc[i+1]:
            return GDP.iloc[i,4]
    

get_recession_start()


# In[168]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    GDP = pd.read_excel('gdplev.xls', skiprows=219)
    
    x = GDP.index[GDP['1999q4'] == get_recession_start()]
    t = GDP.iloc[x[0]:]
    
    t = t[9926.1]
    
    #return GDP.iloc[30:,4:7]
    for i in range(len(t)-1):
        if t.iloc[i+1] > t.iloc[i] and t.iloc[i+2] > t.iloc[i+1]:
            return GDP.iloc[i+36,4]
    
    
    
get_recession_end()


# In[169]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
   
    return '2009q2'
    
get_recession_bottom()


# In[170]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    house = pd.read_csv('City_Zhvi_AllHomes.csv')
    
    house = house.drop(house.columns[[0] + list(range(3,51))], axis=1)
    
    qLabels = []
    
    final = pd.DataFrame(house[['State', 'RegionName']])
    final = final.replace(states)
    
    for i in range(2000,2016):
        qLabels.append(str(i) + 'q1')
        qLabels.append(str(i) + 'q2')
        qLabels.append(str(i) + 'q3')
        qLabels.append(str(i) + 'q4')
    
    for i in qLabels:
        if 'q1' in i:
            z = i[:-2]
            
            final[i] = house[[z+'-01', z+'-02', z+'-03']].mean(axis=1)
        
        elif 'q2' in i:
            z = i[:-2]
            
            final[i] = house[[z+'-04', z+'-05', z+'-06']].mean(axis=1)
            
        elif 'q3' in i:
            z = i[:-2]
            
            final[i] = house[[z+'-07', z+'-08', z+'-09']].mean(axis=1)
            
        else:
            z = i[:-2]
            
            final[i] = house[[z+'-10', z+'-11', z+'-12']].mean(axis=1)
    yr = 2016
    
    final[str(yr) + 'q1'] = house[[str(yr) + '-01', str(yr) + '-02', str(yr) + '-03']].mean(axis = 1)
    final[str(yr) + 'q2'] = house[[str(yr) + '-04', str(yr) + '-05', str(yr) + '-06']].mean(axis = 1)
    final[str(yr) + 'q3'] = house[[str(yr) + '-07', str(yr) + '-08']].mean(axis = 1)
    
    final = final.set_index(['State', 'RegionName'])
            
        
    
    return final
    
    

convert_housing_data_to_quarters()



# In[211]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    
    data = convert_housing_data_to_quarters()
    
    start = get_recession_start()
    
    bot = get_recession_bottom()
    
    uni = get_list_of_university_towns()
    
    uni['unitown'] = True
    
    df = pd.merge(data, uni, how='outer', left_index=True, right_on=['State', 'RegionName'])
    
    df['unitown'] = df['unitown'].replace({np.NaN: False})
    
    df2 = df[['2008q2', bot, 'State', 'RegionName','unitown']]
    
    df2['ratio'] = df2['2008q2'] - df2[bot]
    
    non = df2[df2['unitown'] == False]
    unit = df2[df2['unitown'] == True]
    
    st, p = ttest_ind(non['ratio'], unit['ratio'], nan_policy='omit')
    
    uniM = unit['ratio'].mean()
    
    #print('univ ratio', uniM)
    
    nonM = non['ratio'].mean()
    
    #print('non ratio', nonM)
    
    diff = None
    
    if p < 0.01:
        diff = True
    else:
        diff = False
    
    
    return diff, p, "university town"
run_ttest()


# In[ ]:





# In[ ]:




