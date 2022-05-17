from tkinter.ttk import Style
import pandas as pd
import plotly.graph_objs as go
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

#Reading the CSV and creating a copy of it
Og = pd.read_csv('Insert File Directory')

df = Og.copy()

# print(df.tail())

# print(df.info()) #gives us the info about what type of data is present in the dataframe
# print(df.isnull().sum()) #gives the total missing values

# df = df.drop(columns=['Metacritic Score', 'Boxoffice', 'TMDb Trailer', 'IMDb Link', 'Image', 'Poster', 'Production House', 'Netflix Link', 'Trailer Site'], axis=1)
# print(df.head())
#Converting dates(object datatype) into datetime to use as real dates
df['Release Date'] = pd.to_datetime(df['Release Date'])
df['Netflix Release Date'] = pd.to_datetime(df['Netflix Release Date'])

df['Released_Year'] = pd.DatetimeIndex(df['Release Date']).year
df['Released_Year_Net'] = pd.DatetimeIndex(df['Netflix Release Date']).year

#print(df.head(1))

"""------------------------------- Series vs Movies -------------------------------"""
count = df['Series or Movie'].value_counts()
colors = ['black',] *2
colors[0] = 'Crimson'
#plotting the graph of series v movies
fig = go.Figure(data=[go.Bar(x = df["Series or Movie"],y = count,text = count,textposition='auto',marker_color=colors)])
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(title_text = 'Movie or Series??', uniformtext_minsize=8, uniformtext_mode='hide', barmode='group', xaxis_tickangle = -45,
                                                yaxis = dict(
                                                    title = 'Quantity',
                                                    titlefont_size = 14),
                                                xaxis = dict(
                                                    title = 'Category',
                                                    titlefont_size=14
                                                ))

# print(fig.show())                                     

##Segregating movies and Series
df_series  =  df[df['Series or Movie'] == 'Series']
#print(df_series.head(1))                                            

df_movie  =  df[df['Series or Movie'] == 'Movie']
#print(df_movie.head(1))                                            

"""------------------------------- Genres -------------------------------"""

#dropping null values from genre column

df_series_genres = df_series.dropna(subset=['Genre'])
#For Series
series_genre = df_series_genres.Genre.str.split(',') #split the list into two names
s_gen_list = {} #empty list

for genres in series_genre:
    for genre in genres:
        if genre in s_gen_list:
            s_gen_list[genre]+=1 
        else:
            s_gen_list[genre]= 1

s_gen_df = pd.DataFrame(s_gen_list.values() ,index = s_gen_list.keys(), columns= {'Different Genres in Series'})
s_gen_df.sort_values(by= 'Different Genres in Series', ascending=False, inplace=True) # Sort the dataframe in ascending order

top10_s_gen  = s_gen_df[0:10]
# print(top10_s_gen)

colors_10 = ['DarkRed', 'FireBrick','Red', 'Crimson', 'IndianRed', 'slategray', 'gray', 'dimgrey', 'DarkSlateGrey', 'black']
fig = go.Figure(data=[go.Bar(
    x = top10_s_gen.index,
    y = top10_s_gen['Different Genres in Series'],
    text = top10_s_gen['Different Genres in Series'],
    textposition='auto',
    marker_color=colors_10 # marker color can be a single color value or an iterable
)])
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(title_text= 'The most popular genres under series',
                  uniformtext_minsize=8, uniformtext_mode='hide',
                  yaxis=dict(
                  title='Frequency',
                  titlefont_size=15, ),
                  xaxis=dict(
                  title='Genres',
                  titlefont_size=15))

# print(fig.show())

#For Movies
df_movies_genres = df_movie.dropna(subset=['Genre'])
movies_genre = df_movies_genres.Genre.str.split(',') #split the list into two names
m_gen_list = {} #empty list

for genres in movies_genre:
    for genre in genres:
        if genre in m_gen_list:
            m_gen_list[genre]+=1 
        else:
            m_gen_list[genre]= 1

m_gen_df = pd.DataFrame(m_gen_list.values() ,index = m_gen_list.keys(), columns= {'Different Genres in Movies'})
m_gen_df.sort_values(by= 'Different Genres in Movies', ascending=False, inplace=True) # Sort the dataframe in ascending order

top10_m_gen  = m_gen_df[0:10]
# print(top10_m_gen)

fig = go.Figure(data=[go.Bar(
    x = top10_m_gen.index,
    y = top10_m_gen['Different Genres in Movies'],
    text = top10_m_gen['Different Genres in Movies'],
    textposition='auto',
    marker_color=colors_10 # marker color can be a single color value or an iterable
)])
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(title_text= 'The most popular genres under movies',
                  uniformtext_minsize=8, uniformtext_mode='hide',
                  yaxis=dict(
                  title='Frequency',
                  titlefont_size=15, ),
                  xaxis=dict(
                  title='Genres',
                  titlefont_size=15))

# print(fig.show())

"""------------------------------- Hidden Gems Top 10 -------------------------------"""
#For Series
def_hg_series = df_series.dropna(subset=['Hidden Gem Score'])
def_hg_series = def_hg_series.sort_values(by='Hidden Gem Score', ascending=False)
top10_s_list = def_hg_series[0:10]
top10_s_list.reset_index(drop=True, inplace=True)
# print('10 Best Hidden Gems - Series are: \n', top10_s_list['Title'])

#For Movies
def_hg_movies = df_movie.dropna(subset=['Hidden Gem Score'])
def_hg_movies = def_hg_movies.sort_values(by='Hidden Gem Score', ascending=False)
top10_m_list = def_hg_movies[0:10]
top10_m_list.reset_index(drop=True, inplace=True)
# print('10 Best Hidden Gems - Movies are: \n', top10_m_list['Title'])


"""------------------------------- Duration of the Content -------------------------------"""
df_series_dur = df_series.dropna(subset=['Runtime'])
# print(df_series_dur['Runtime'].value_counts())

df_movie_dur = df_movie.dropna(subset=['Runtime'])
count_d = df_movie_dur['Runtime'].value_counts()

fig = go.Figure(data=[go.Bar(
    x = count_d.index,
    y = count_d,
    text = count_d,
    textposition='auto',
    marker_color=colors_10
)])
fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig.update_layout(title_text= 'Average duration of a movie on Netflix',
                  uniformtext_minsize=8, uniformtext_mode='hide',
                  yaxis=dict(
                  title='Movies',
                  titlefont_size=14),
                  xaxis=dict(
                  title='Duration',
                  titlefont_size=14))
# print(fig.show())

"""------------------------------- Top 15 Movies and Series in terms of total awards received -------------------------------"""
df_series_awd = df_series.dropna(subset=['Awards Received'])
df_series_awd = df_series_awd.sort_values(by= 'Awards Received', ascending=False)
top15_s_awd = df_series_awd[0:15]

colors_15 = ['DarkRed', 'FireBrick', 'FireBrick' ,'Red', 'Crimson', 'Crimson', 'IndianRed' , 'slategray', 'slategray' , 'gray' , 'gray', 'dimgrey', 'dimgrey', 'DarkSlateGrey', 'black']
fig = go.Figure(data=[go.Bar(
    x = top15_s_awd['Title'],
    y = top15_s_awd['Awards Received'],
    text = top15_s_awd['Awards Received'],
    textposition='auto',
    marker_color=colors_15 # marker color can be a single color value or an iterable
)])
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(title_text= 'The 15 series with most awards',
                  uniformtext_minsize=8, uniformtext_mode='hide',
                  yaxis=dict(
                  title='Awards Received',
                  titlefont_size=14),
                  xaxis=dict(
                  title='Titles',
                  titlefont_size=14))
# print(fig.show())

#For Movies

df_movie_awd = df_movie.dropna(subset=['Awards Received'])
df_movie_awd = df_movie_awd.sort_values(by = 'Awards Received', ascending = False)
top15_m_awd = df_movie_awd[:15]
fig = go.Figure(data=[go.Bar(
    x = top15_m_awd['Title'],
    y = top15_m_awd['Awards Received'],
    text = top15_m_awd['Awards Received'],
    textposition='auto',
    marker_color=colors_15 # marker color can be a single color value or an iterable
)])
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(title_text= 'The 15 Movies with most awards?',
                  uniformtext_minsize=8, uniformtext_mode='hide',
                  yaxis=dict(
                  title='Awards Received',
                  titlefont_size=14),
                  xaxis=dict(
                  title='Titles',
                  titlefont_size=14))

# print(fig.show())

"""------------------------------- Quantity of Content Released by Netflix -------------------------------"""

df_series_release = df_series.dropna(subset=['Released_Year_Net'])
series_release = df_series_release['Released_Year_Net']
s_release = {}

for year in series_release:
    if year in s_release :
        s_release[year]+=1
    else:
        s_release[year] = 1
s_rel_df = pd.DataFrame(s_release.values(),index = s_release.keys(),
                        columns = {'Year Counts'})
s_rel_df.sort_values(by='Year Counts',ascending=False, inplace=True)

top10_s_release = s_rel_df[0:10]
# print(top10_s_release)

fig = go.Figure(data=[go.Bar(
    x = top10_s_release.index,
    y = top10_s_release['Year Counts'],
    text = top10_s_release['Year Counts'],
    textposition='auto',
    marker_color=colors_10 # marker color can be a single color value or an iterable
)])
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(title_text= 'Comparison of Series released by Netlfix over the last 7 years',
                  uniformtext_minsize=8, uniformtext_mode='hide',
                  yaxis=dict(
                  title='N° of release',
                  titlefont_size=14),
                  xaxis=dict(
                  title='Titles',
                  titlefont_size=14))
# print(fig.show())

#For Movies
df_movie_release = df_movie.dropna(subset=['Released_Year_Net'])
movie_rel_list = df_movie_release['Released_Year_Net']
m_rel_list = {} #create an empty list
for year in movie_rel_list: # for any year in movie_rel_list
    if (year in m_rel_list): #if this year is already present in the m_rel_list
        m_rel_list[year]+=1 # increase his value
    else:  # else
        m_rel_list[year]=1 # Create his index in the list
m_rel_df = pd.DataFrame(m_rel_list.values(),index = m_rel_list.keys(),
                        columns = {'Year Counts'}) #Create a s_ctr_df
m_rel_df.sort_values(by = 'Year Counts',ascending = False,inplace = True) #Sort the dataframe in ascending order
top_10_m_rel = m_rel_df[0:10] 
fig = go.Figure(data=[go.Bar(
    x = top_10_m_rel.index,
    y = top_10_m_rel['Year Counts'],
    text = top_10_m_rel['Year Counts'],
    textposition='auto',
    marker_color=colors_10 # marker color can be a single color value or an iterable
)])
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(title_text= 'Comparison of Movies released by Netlfix over the last 7 years',
                  uniformtext_minsize=8, uniformtext_mode='hide',
                  yaxis=dict(
                  title='N° of release',
                  titlefont_size=14),
                  xaxis=dict(
                  title='Titles',
                  titlefont_size=14))
# print(fig.show())

"""------------------------------- Top 15 Movies and Series in terms of total awards received -------------------------------"""

score_columns = [col for col in df.columns if 'Score' in col]
score_columns.append('Boxoffice')

df_score = df[score_columns]
df_score = df_score.dropna(subset=['Boxoffice'])
df_score['Boxoffice'] = df_score['Boxoffice'].replace('[\$,]','',regex=True)
df_score['Boxoffice'] = pd.to_numeric(df_score['Boxoffice'])
df_score['Rotten Tomatoes Score'] = df_score['Rotten Tomatoes Score']/10
df_score['Metacritic Score'] = df_score['Metacritic Score']/10
# print(df_score.head())

df_score_long = pd.melt(df_score, id_vars= ['Boxoffice'], value_vars= ['Hidden Gem Score', 'IMDb Score', 'Rotten Tomatoes Score', 'Metacritic Score'],
                                                            var_name= 'Platform', value_name= 'Score')
# print(df_score_long.head())

sns.lmplot(x = 'Score',y = 'Boxoffice',hue = 'Platform',data = df_score_long )
print(plt.show())
