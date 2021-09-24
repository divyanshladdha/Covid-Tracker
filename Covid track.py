import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from selenium import webdriver
import geopandas as gpd

url = 'https://www.covid19india.org/'

#Opening the provided url in a Web Browser
driver = webdriver.Chrome("F:/chromedriver.exe")
driver.get(url)
driver.maximize_window();

#Extracting the necessary data from the table 
states = driver.find_elements_by_xpath(".//div/div[2]/div[1]/div[4]/div[2]/div/div/div[1]/div[1]")[1:]
confirmed = driver.find_elements_by_xpath(".//div/div[2]/div[1]/div[4]/div[2]/div/div/div[2]/div[2]")[1:]
active = driver.find_elements_by_xpath(".//div/div[2]/div[1]/div[4]/div[2]/div/div/div[3]/div")[1:]
recovered = driver.find_elements_by_xpath(".//div/div[2]/div[1]/div[4]/div[2]/div/div/div[4]/div[2]")
deceased = driver.find_elements_by_xpath(".//div/div[2]/div[1]/div[4]/div[2]/div/div/div[5]/div[2]")
tested = driver.find_elements_by_xpath(".//div/div[2]/div[1]/div[4]/div[2]/div/div/div[7]/div[2]")
partially_vaccinated = driver.find_elements_by_xpath(".//div/div[2]/div[1]/div[4]/div[2]/div/div/div[8]/div[2]")
fully_vaccinated = driver.find_elements_by_xpath(".//div/div[2]/div[1]/div[4]/div[2]/div/div/div[9]/div[2]")

covid_stats = []
for i in range(len(states)):
    temp_data = {'States/UT' : states[i].text,
                 'Confirmed' : int(confirmed[i].text.replace(',','')),
                 'Active' : int(active[i].text.replace(',','')),
                 'Recovered' : int(recovered[i].text.replace(',','')),
                 'Deceased' : int(deceased[i].text.replace(',','')),
                 'Tested' : tested[i].text,
                 'Partially Vaccinated' : partially_vaccinated[i].text,
                 'Fully Vaccinated' : fully_vaccinated[i].text}
    covid_stats.append(temp_data)

#Converting the data into Pandas Dataframe for further processing and manipulating
df_covid_stats = pd.DataFrame(covid_stats)
df_covid_stats

# barplot to show total confirmed cases Statewise 
sns.set_style("ticks")
plt.figure(figsize = (15,10))
plt.barh(df_covid_stats["States/UT"], df_covid_stats["Confirmed"],align = 'center', color = 'lightblue', edgecolor = 'blue')
plt.xlabel('No. of Confirmed cases', fontsize = 18)
plt.ylabel('States/UT', fontsize = 18)
plt.gca().invert_yaxis() # this is to maintain the order in which the states appear
plt.xticks(fontsize = 14) 
plt.yticks(fontsize = 14)
plt.title('Total Confirmed Cases Statewise', fontsize = 20)

for index, value in enumerate(df_covid_stats["Confirmed"]):
    plt.text(value, index, str(value), fontsize = 12, verticalalignment = 'center')
plt.show()

# donut chart representing nationwide total confirmed, cured and deceased cases
group_size = [sum(df_covid_stats['Confirmed']), 
              sum(df_covid_stats['Recovered']), 
              sum(df_covid_stats['Deceased'])]

group_labels = ['Confirmed\n' + str(sum(df_covid_stats['Confirmed'])), 
                'Recovered\n' + str(sum(df_covid_stats['Recovered'])), 
                'Deceased\n'  + str(sum(df_covid_stats['Deceased']))]
custom_colors = ['skyblue','yellowgreen','tomato']

plt.figure(figsize = (5,5))
plt.pie(group_size, labels = group_labels, colors = custom_colors)
central_circle = plt.Circle((0,0), 0.5, color = 'white')
fig = plt.gcf()
fig.gca().add_artist(central_circle)
plt.rc('font', size = 12) 
plt.title('Nationwide total Confirmed, Recovered and Deceased Cases', fontsize = 16)
plt.show()

# read the state wise shapefile of India in a GeoDataFrame and preview it
map_data = gpd.read_file("F:\States\Admin2.shp")
map_data.rename(columns = {'ST_NM':'States/UT'}, inplace = True)

# correct the name of states in the map dataframe 
map_data['States/UT'] = map_data['States/UT'].str.replace('&','and')
map_data['States/UT'].replace('Andaman & Nicobar','Andaman and Nicobar Islands',inplace = True)

# merge both the dataframes - state_data and map_data
merged_data = pd.merge(map_data, df_covid_stats,how = 'left', on = 'States/UT')
merged_data.fillna(0, inplace = True)

# create figure and axes for Matplotlib and set the title
fig, ax = plt.subplots(1, figsize=(20, 12))
ax.axis('off')
ax.set_title('Covid-19 Statewise Data — Confirmed Cases',fontdict =  {'fontsize': '25', 'fontweight' : '3'})
merged_data.plot(column = 'Confirmed', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8',legend = True)
plt.show()

# create figure and axes for Matplotlib and set the title
fig2, ax2 = plt.subplots(1, figsize=(20, 12))
ax2.axis('off')
ax2.set_title('Covid-19 Statewise Data — Active Cases',fontdict =  {'fontsize': '25', 'fontweight' : '3'})
merged_data.plot(column = 'Active', cmap='Reds', linewidth=0.8, ax=ax2, edgecolor='0.8',legend = True)
plt.show()
