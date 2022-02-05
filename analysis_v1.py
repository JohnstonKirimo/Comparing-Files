#!/usr/bin/env python
# coding: utf-8

# ### Table of Contents 
# ##### 1. Importing libraries and reading data
# ##### 2. Exploratory Data Analysis 
# ##### 3. Data Cleaning and checking of coverage rates

# ### Importing Libraries and Reading data

# In[1]:


#importing modules and reading data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
test = pd.read_csv('/users/johnstonkirimo/Projects/Zesty/data/test.csv')
all_addrs = pd.read_csv('/users/johnstonkirimo/Projects/Zesty/data/all_addresses.csv')


# ### Exploratory Data Analysis

# In[2]:


#overview of df1 dataset

all_addrs.head()


# In[3]:


#overview of df2 dataset
test.head()


# In[4]:


#number of rows and columns
all_addrs.shape


# In[5]:


#number of rows and columns 
test.shape


# In[6]:


#info on dataset
all_addrs.info()


# In[7]:


test.info()


# In[8]:


#examinining specific columns : address 
all_addrs.groupby('address').size()


# In[9]:


#examinining specific columns : address (df2)
test.groupby('address').size()


# In[11]:


#examinining specific columns: top 5 cities
test.city.value_counts(dropna=False).head()


# In[12]:


#examinining percent distribution: top 5 states
test.state.value_counts(normalize = True, dropna=False)[:5]


# In[13]:


#checking for missing values
test.isnull().sum()


# In[14]:


#checking for missing values - all_addrs
all_addrs.isnull().sum()


# In[15]:


#examine city using groupby

all_addrs.groupby('city').size()


# In[16]:


#examine state using groupby

all_addrs.groupby('state').size()


# In[17]:


#examine state using groupby

test.groupby('city').size()


# In[18]:


#examine state using groupby

test.groupby('state').size()


# In[19]:


#check the unique values in the state column
test['state'].unique()


# #### Some Observations on the address column: 
# 
# - There are 504 records of incorrect inputs with the value '#NAME?' in the all_address dataframe
# - There are 167 records, with the value '- -' in the all_address dataframe
# - Several actual addresses with wrong inputs, starting with '-'
# - The test dataframe has similar issues of missing,wrong or incorrectly formatted inputs in the test dataframe

# #### Key Observations on the city and state columns:
# 
# - all_addrs dataframe has 524 records with missing values, with input '-'
# - Missing values/incorrect value, '-'
# - Incorrect inputs with names, e.g. GUATENG, instead of abbreviations
# - Wrong info/abbreviations used, e.g. ON 
# - Total of 59 unique values for state, instead of 50
# - Lowercase, uppercase and missing values 

# In[20]:


# Examining the zip column
all_addrs.zip.sample(10)


# In[21]:


# Examining the zip column
test.zip.sample(10)


# In[22]:


#top 5 most common zip codes
all_addrs.zip.value_counts().head()


# In[23]:


#top 5 most common zip codes
test.zip.value_counts().head()


# In[24]:


#examine using groupy
all_addrs.groupby('zip').size()


# In[25]:


#examine using groupy
test.groupby('zip').size()


# ### Data Cleaning 

# #### Coverage Rate - the percentage of properties in a file that has correct addresses and matches up with a standard address database

# #### To measure the impact of the data cleaning methods applied, let's compare the coverage rate before and after conducting the data cleaning process. We'll begin by checking the current coverage rate:

# #### There are several ways of checking the address match between the two dataframes.
# #### 1. Match on row level for each column

# In[26]:


#convert data type of zip column in test df to string
test.zip.astype(str).apply(lambda x: x.replace('.0',''))


# In[27]:


#For each row in test df, check if there is a match in all_addrs df
is_match =  test[(test.address.isin(all_addrs.address)) & (test.city.isin(all_addrs.city))
                                 & (test.state.isin(all_addrs.state)) & (test.zip.isin(all_addrs.zip))]


# In[28]:


match_rate = (len(is_match) * 100) /len(all_addrs)
print("The test dataset has a coverage rate of: {} percent ".format(match_rate)) 


# #### 2. Create a single 'full_address' column for each dataframe and compare the two columns 

# In[32]:


#create full_address column on each df

all_addrs['full_address'] = all_addrs.address  + ', ' + all_addrs.city + ', ' + all_addrs.state + ' ' + all_addrs.zip
test['full_address'] = test.address + ', '+ test.city + ', ' + test.state + ' ' + test.zip.astype(str)


# In[33]:


#let's view the change in test df
test.head(3)


# In[34]:


#let's view the change in all_addrs
all_addrs.head(3)


# In[35]:


#change data type for zip column in test df 

test['zip'] = test.zip.astype(str).apply(lambda x: x.replace('.0',''))


# In[36]:


test.head(3)


# In[37]:


#apply change to the full_address column of test df
test['full_address'] = test.address + ', '+ test.city + ', ' + test.state + ' ' + test.zip.astype(str)


# In[34]:


test.head(3)


# In[38]:


#Now let's see how many full_addresses in test df are also in all_addrs df
is_match2 =  [i for i in test.full_address if i in all_addrs.full_address]


# In[39]:


match_rate2 = (len(is_match2) * 100) /len(all_addrs)
print("The test dataset has a new coverage rate of: {} percent ".format(match_rate2)) 


# In[37]:


#examine and try new method


# In[40]:


test.dtypes


# In[41]:


all_addrs.dtypes


# In[42]:


#function to get the common addresses 

def common_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result


# In[43]:


#get the full_address columns as lists 

test_lst = test['full_address'].to_list()
all_addrs_lst = all_addrs['full_address'].to_list()


# In[44]:


#check the number of addresses in test df which are also found in all_addrs df
is_match3 = common_elements(test_lst, all_addrs_lst )


# In[45]:


match_rate3 = (len(is_match3) * 100) /len(all_addrs)
match_rate3
#print("The test dataset has a new match rate of: {} percent ".format(match_rate3)) 


# ##### It appears using a function to get the common elements between the two lists produces a better match. However, the data still includes all the wrong and incorrectly formatted addreses. So let's start cleaning both datasets.

# ### Data Cleaning 

# In[46]:


#Examine addresses that start with # or -
test[test['address'].str.startswith(('#', '-'))].head()


# In[47]:


#Examine addresses that start with # or -
all_addrs[all_addrs['address'].astype(str).str.startswith(('#', '-'))].head()


# 
# #### We can see both datasets have the same issue of wrong or incorrectly formatted values
# #### Since the full_address column is made of the first three columns, the same errors are also found in the full_address column 

# In[48]:


#count addresses starting with '-' or '#'
is_dirty_all_addrs = all_addrs[all_addrs['address'].astype(str).str.startswith(('#', '-'))]
is_dirty_all_addrs.head()


# In[49]:


len(is_dirty_all_addrs)


# In[50]:


#Repeat the above for test df
is_dirty_test = test[test['address'].str.startswith(('#', '-'))]
is_dirty_test.head()


# In[51]:


len(is_dirty_test)


# ##### We can see that 792 rows in the all_addrs df has wrong/incorrectly formatted addresses while the test df has 278

# ##### However, there are more missing and incorrect/wrongly formatted values in the other columns as well. Some of the issues we previously found out about the city and state columns include:
# 
# - All_addrs dataframe has 524 records with missing values, with input '-'
# - Missing values/incorrect value, '-'
# - Incorrect inputs with names, e.g. GUATENG, instead of abbreviations
# - Wrong info/abbreviations used, e.g. ON
# - Total of 59 unique values for state, instead of 50
# - Lowercase, uppercase and missing values

# In[52]:


#examine where city is '-'
all_addrs[all_addrs['city'] == '-'] [['city','full_address']].head()


# In[53]:


#examine where city is '-'
test[test['city'] == '-'] [['city','full_address']].head()


# In[54]:


#any null valaues in city and state and zip columns?

test[['address','city','state','zip']].isna().sum()


# In[55]:


all_addrs[['address','city','state','zip']].isna().sum()


# #### Let's get the subset we don't want and remove it, i.e:
# - where the address starts with '#', '-' or is null
# - where the city or state is '-'
# - where the city, state or zip value is null

# In[56]:


#subset to be dropped from the all_addrs df
unwanted_all_addrs = all_addrs[all_addrs['address'].astype(str).str.startswith(('#', '-')) | (all_addrs['address'].isna())|
                              (all_addrs['city'].isna()) | (all_addrs['city'] == '-') | (all_addrs['state'].isna()) | (all_addrs['state'] == '-')|
                               (all_addrs['zip'].isna()) | (all_addrs['zip'] == '-')]
unwanted_all_addrs.head(3)


# In[57]:


#Now let's get the subset to be dropped from the test df

unwanted_test = test[test['address'].astype(str).str.startswith(('#', '-')) | (test['address'].isna())|
                              (test['city'].isna()) | (test['city'] == '-') | (test['state'].isna()) | (test['state'] == '-')|
                               (test['zip'].isna()) | (test['zip'] == '-')]
unwanted_test.head(3)


# In[58]:


#Let's check the length of the 'unwanted' for each dataset
print("There are {} unwanted dirty rows in the all_addrs dataset".format(len(unwanted_all_addrs)))
print("There are {} unwanted dirty rows in the test dataset".format(len(unwanted_test)))


# In[59]:


#create a new column 'clean' to identify distinguish 'dirty' vs 'clean'records in the all_addr dataset

all_addrs['clean'] = np.where(all_addrs['address'].astype(str).str.startswith(('#', '-')) | (all_addrs['address'].isna())|
                              (all_addrs['city'].isna()) | (all_addrs['city'] == '-') | (all_addrs['state'].isna()) | (all_addrs['state'] == '-')|
                               (all_addrs['zip'].isna()) | (all_addrs['zip'] == '-'),0,1) 


# In[60]:


all_addrs.groupby('clean').size()


# In[61]:


#distribution

all_addrs['clean'].value_counts(normalize=True)


# In[62]:


#create a new column 'clean' to identify & distinguish 'dirty' vs 'clean'records in the test dataset

test['clean'] = np.where(test['address'].astype(str).str.startswith(('#', '-')) | (test['address'].isna())|
                              (test['city'].isna()) | (test['city'] == '-') | (test['state'].isna()) | (test['state'] == '-')|
                               (test['zip'].isna()) | (test['zip'] == '-') | test['zip'].str.contains('nan'),0,1) 


# In[63]:


test.groupby('clean').size()


# In[64]:


#check distribution of 'clean' vs 'dirty' records 
test['clean'].value_counts(normalize=True)


# ##### Looking at the distribution, it's clear that 16.6% of the test dataset are rows in the 'unwanted/dirty' criteria

# In[65]:


#Now let's get the cleaned version of the test df 
is_clean_test = test.loc[test.clean == 1,:]
is_clean_test.head()


# In[66]:


#Now let's get the cleaned version of the all_addrs df 
is_clean_all_addrs = all_addrs.loc[all_addrs.clean == 1,:]
is_clean_all_addrs.head()


# In[67]:


#Get the full_address columns as lists for each of the 'cleaned' datasets

is_clean_test_lst = is_clean_test['full_address'].to_list()
is_clean_all_addrs_lst = is_clean_all_addrs['full_address'].to_list()


# In[68]:


#check the new number of addresses in is_clean_test df which are also found in is_clean_all_addrs df
is_match4 = common_elements(is_clean_test_lst, is_clean_all_addrs_lst)


# In[69]:


match_rate4 = len(is_match4) * 100 /len(is_clean_all_addrs_lst)
match_rate4


# In[70]:


#try another function using list comprehension

def same_elements(first_list, second_list):
    return [element for element in first_lst if element in second_lst]


# In[72]:


first_lst = is_clean_test['full_address'].to_list()
second_lst = is_clean_all_addrs['full_address'].to_list()


# In[73]:


is_same_clean  = same_elements(is_clean_test_lst,is_clean_all_addrs_lst)

coverage_rate = len(is_same_clean) * 100 /len(is_clean_all_addrs)


# In[74]:


coverage_rate


# #### After trying two different functions with the cleaned datasets, the coverage rate is now 43%. 
# #### let's examine the datasets a bit more to check for opportunities of improvement

# In[75]:


is_clean_test.head()


# In[76]:


is_clean_test.shape


# In[77]:


#xamine unique states in cleaned all_addrs df 
is_clean_all_addrs.state.unique()


# In[78]:


#examine unique states in cleaned test df
is_clean_test.state.unique()


# ##### Here we observe that the is_clean_test dataset has uppercase and lowercase values in the state column - 
# ##### this is an opportunity to make some changes and increase the coverage rate

# In[79]:


#remove records where given state name is not a correct US state

is_clean_all_addrs = is_clean_all_addrs[~is_clean_all_addrs.state.isin(['GAUTENG','CÓRDOBA','CHIH','CHIS','ON'])]
is_clean_all_addrs.shape


# In[80]:


#make the full address column uppercase

is_clean_test['full_address'] = is_clean_test['full_address'].str.upper()
is_clean_all_addrs['full_address'] = is_clean_all_addrs['full_address'].str.upper()


# In[81]:


lst_all = is_clean_all_addrs['full_address'].to_list()
lst_tst = is_clean_test['full_address'].to_list()
new_covrg = [x for x in lst_tst if x in lst_all]
cov_rate = len(new_covrg) * 100 /len(lst_all)
print("The coverage rate is now {} percent".format(cov_rate))


# #### New coverage rate is 48.8%

# In[82]:


#Now let's remove duplicates from both lists by using a set()

all_addrs_set = set(lst_all)
test_set = set(lst_tst)


# In[83]:


#find common elements in the two sets and print new coverage rate

set_covrg = [x for x in test_set if x in all_addrs_set]
set_covrg_rate = len(set_covrg) * 100 /len(all_addrs_set)


# In[84]:


set_covrg_rate


# #### Coverage rate now at 63.8%
