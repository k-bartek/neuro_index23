import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi


st.set_page_config(
    page_title="NEURO Index 2023",
    page_icon=":brain:"
    )

st.title('NEURO Index 2023')


st.sidebar.write("NEURO Index 2023")
st.sidebar.caption("This index shows how well are countries prepared for neuro-generative diseases.")
st.sidebar.caption("Created by Katarina Bartekova and MSquare. All rights reserved")



@st.cache_data
def load_data():
    data = pd.read_csv('data.csv')
    lowercase = lambda x: str(x).lower()
    #data.rename(lowercase, axis='columns', inplace=True)
    data['country'] = data['country'].replace('AVERAGE (NL,DE)', 'Benchmark (NL, DE)')  #benchmark average west
    data = data.iloc[2:].reset_index(drop=True)   #optional - apply only when we dont want to compare Germany and Netherlands

    #rename columns

    rename_dict = {
    "WAIT Indicator for orphan non-onco diseases": "WAIT indicator (orphan non-onco)",
    "Health care expenditure by function (Inpatient curative and rehabilitative care HC11_21)": "Inpatient curative and rehabilitative care Expenditure",
    "Health care expenditure by function (Long-term care (health) HC3)": "Long-term care Expenditure",
    "Health care expenditure by function (Preventive care HC6)": "Preventive Expenditure",
    "The Universal Health Coverage Index ": "Universal Health Coverage",
    "Beds in nursing and other residential long-term care facilities ": "Beds in long-term care facilities",
    "Household out-of-pocket payments OOP (Desc order)": "Household OOP",
    "Dependence Ratio (Desc order)": "Dependence Ratio",
    "Does a country have an HTA agency with clear and transparent decision rules?": "HTA agency",
    "Does a country have an investment strategy in the health sector?": "Investment strategy",
    "Does a country have early access scheme?  ": "Early access scheme",
    "Average life span of a minister of health": "Minister of health av. tenure"
    }

    # Rename the columns
    data.rename(columns=rename_dict, inplace=True)


    
    
    return data


data = load_data()




options_country = data['country'].to_list()

options_categories = data.columns.to_list()[1:] #without the first one tho as that one is country


selection_country = st.selectbox(
    "Pick a country",
    (options_country))




#graph should be based on selection 
st.subheader('Country comparison based on Categories')

selection_category = st.selectbox(
    "Pick a category",
    (options_categories))



#Bar chart

    
categories = data['country']
values = data[selection_category]

#find the index of the country
highlight_country = selection_country
categories_list = categories.to_list()
num_country = categories_list.index(selection_country)

highlight_value = values[num_country]
fig, ax = plt.subplots(figsize=(18, 12))

# Plot the bar chart
ax.bar(categories, values, width=0.4, alpha = 0.5)
ax.tick_params(axis='x', labelsize=9)
ax.set_xlabel('Countries')
ax.set_ylabel('Scores per ' + selection_category, size = 15)
ax.set_yticks(np.arange(0, 11, 1))
ax.set_ylim(0, 11)
ax.set_title('Comparison of countries based on ' + selection_category, size = 15)



# Highlight the bar corresponding 
highlight_index = num_country 
ax.bar(categories[highlight_index], highlight_value, width = 0.4, color='red', label=selection_country)


ax.legend()


st.pyplot(fig)
plt.close()




#info o kategorii
if selection_category == "Household OOP":
    st.caption("Household OOP is referring to the Household out-of-pocket payments in a descending order")
elif selection_category == "Dependence Ratio":
    st.caption("Dependence ratio is in a descending order")





#lollipop plot part



st.subheader('Country Comparison with the Benchmark (or other countries)')

selection_country_compare = st.selectbox(
    "Pick a country to compare with " + selection_country,
    (options_country), index = ((len(options_country)) - 1))  #last country is the west average

####lollipop plot
#add best and worst category for each country - same for spider plot

#data transform
df_trans = data.transpose()
# Set the first row as column names
df_trans.columns = df_trans.iloc[0]
df_trans = df_trans[1:]


df_trans.reset_index(inplace=True)
df_trans.rename(columns={'index': 'indicator'}, inplace=True)

#selection
selection_count = selection_country

value1 = df_trans[selection_country_compare]
value2 = df_trans[selection_count]

value1_name = selection_country_compare
value2_name = selection_count

#plotting
df = pd.DataFrame({'group': df_trans['indicator'], 'value1': value1 , 'value2':value2 })
# Reorder it following the values of the first value:
ordered_df = df.sort_values(by='value1')

my_range=range(1,len(df.index)+1)

plt.hlines(y=my_range, xmin=ordered_df['value1'], xmax=ordered_df['value2'], color='grey', alpha=0.4)
plt.scatter(ordered_df['value1'], my_range, color='blue', alpha=0.5, label=value1_name)
plt.scatter(ordered_df['value2'], my_range, color='red', alpha=1 , label=value2_name)
plt.legend()
plt.yticks(my_range, ordered_df['group'], size=8)

plt.xticks([0,2,4,6,8,10], ["0","2","4","6","8","10"], color="grey", size=8)
plt.title("Comparison of " + value2_name + " and " + value1_name , loc='left')
plt.xlabel('Scores per Category')

st.pyplot(plt.gcf())
plt.close()



######spider plot
categories_sp=list(data)[1:]  
N = len(categories_sp)
 

angles = [n / float(N) * 2 * pi for n in range(N)] 
angles += angles[:1]
 

ax = plt.subplot(111, polar=True)
 

ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)
 

plt.xticks(angles[:-1], categories_sp, size = 4, rotation = 45, ha = 'center') #size 4, rotation 90



 
# ylabels
ax.set_rlabel_position(0)
plt.yticks([0,2,4,6,8,10], ["0","2","4","6","8","10"], color="grey", size=7)
plt.ylim(0,12)
 
# Plot each individual = each line of the data

selection_country_1 = selection_country
selection_country_2 = selection_country_compare #default 'Average West'

#finding the index of each country row
selection_country_1_index = data[data['country'] == selection_country_1].index[0]
selection_country_2_index = data[data['country'] == selection_country_2].index[0]

# Ind1
#loc is based on index row of the country
values=data.loc[selection_country_1_index].drop('country').values.flatten().tolist() #what to drop
values += values[:1]
ax.plot(angles, values, color = 'red', linewidth=1, linestyle='solid',label=selection_country_1, alpha = 0.7)
ax.fill(angles, values, 'red', alpha=0.1)
 
# Ind2
values=data.loc[selection_country_2_index].drop('country').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, color = 'blue' , linewidth=1, linestyle='solid', label=selection_country_2, alpha = 0.5) 
ax.fill(angles, values, 'blue', alpha=0.07)
 
# legend
plt.legend(bbox_to_anchor=(0.01, 0.01))



st.pyplot(plt.gcf())
plt.close()




