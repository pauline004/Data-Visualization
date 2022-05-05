import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from raceplotly.plots import barplot


path = 'https://raw.githubusercontent.com/Joaomcns/Group_47_DVProject/master/data/'

characters = pd.read_csv(path + 'Characters.csv')
episodes = pd.read_csv(path + 'Episodes.csv')
lines = pd.read_excel(path + 'Lines.xlsx')
ratings = pd.read_csv(path + 'episode_ratings_got.csv')
deaths = pd.read_excel(path + 'game-of-thones-deaths.xlsx')

episodes['seasonNumber'] = episodes['seasonNumber'].astype(str)

s = pd.Series(['Total', 73, 'Total', '2011-2019', 'No Desc', 470.7, 8.8, 3924153,'bla','bla',1234,'bla'], index=episodes.columns)
episodes = episodes.append(s, ignore_index=True)

s1 = episodes[episodes['seasonNumber'] == '1'].sort_values("millionViewers")
s2 = episodes[episodes['seasonNumber'] == '2'].sort_values("millionViewers")
s3 = episodes[episodes['seasonNumber'] == '3'].sort_values("millionViewers")
s4 = episodes[episodes['seasonNumber'] == '4'].sort_values("millionViewers")
s5 = episodes[episodes['seasonNumber'] == '5'].sort_values("millionViewers")
s6 = episodes[episodes['seasonNumber'] == '6'].sort_values("millionViewers")
s7 = episodes[episodes['seasonNumber'] == '7'].sort_values("millionViewers")
s8 = episodes[episodes['seasonNumber'] == '8'].sort_values("millionViewers")
s_total = episodes.sort_values("millionViewers")
s_total_1 = s_total[0:-1].tail(10)

scatter_colors = ['#DAA520', '#DAA520', '#DAA520', '#DAA520 ', '#DAA520', '#DAA520', '#DAA520', '#DAA520', '#DAA520']
scatter_options = [s1, s2, s3, s4, s5, s6, s7, s8, s_total_1]

tot_list = []
final = []
for season in episodes['seasonNumber'].unique():
    if season == 'Total':
        tot_list = [dict(label=' ' + season, value='9')]
    else:
        final.append(dict(label=' ' + season, value=season))

final += tot_list
season_options = final
radio_season_choice = dbc.RadioItems(
    id='season_choice',
    className='radio',
    options=season_options,
    value=2,
    inline=True,

)

options_s1 = [dict(label=key, value=key) for key in s1['episodeTitle'].tolist()[::-1]]
options_s2 = [dict(label=key, value=key) for key in s2['episodeTitle'].tolist()[::-1]]
options_s3 = [dict(label=key, value=key) for key in s3['episodeTitle'].tolist()[::-1]]
options_s4 = [dict(label=key, value=key) for key in s4['episodeTitle'].tolist()[::-1]]
options_s5 = [dict(label=key, value=key) for key in s5['episodeTitle'].tolist()[::-1]]
options_s6 = [dict(label=key, value=key) for key in s6['episodeTitle'].tolist()[::-1]]
options_s7 = [dict(label=key, value=key) for key in s7['episodeTitle'].tolist()[::-1]]
options_s8 = [dict(label=key, value=key) for key in s8['episodeTitle'].tolist()[::-1]]
options_s_total = [dict(label=key, value=key) for key in s_total_1['episodeTitle'].tolist()[::-1]]

drop_episodes = dcc.Dropdown(
    id='drop_episodes',
    clearable=False,
    searchable=False,
    style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': 'rgba(28, 53, 117, 0.56)'}
)


lines['Season']=lines['seasonEpisode'].str[:2]
lines['House'] = lines.speaker.str.extract(r'\b(\w+)$', expand=True)

house_to_keep = ['Stark', 'Lannister', 'Targaryen', 'Snow', 'Baratheon', 'Greyjoy', 'Tyrell', 'Mormont', 'Martell', 'Tully']
lines=lines[lines["House"].isin(house_to_keep)==True]
stack=lines.groupby(['House', 'Season'], as_index=False)['lineCount'].sum()

fig_lines = px.bar(stack, y="House", x="lineCount", color="Season", title="Total lines said for each House",
             color_discrete_sequence=px.colors.sequential.ice_r)
fig_lines.update_layout(yaxis={'categoryorder':'array', 'categoryarray':['Tully','Martell' ,'Tyrell','Mormont','Greyjoy',
                                                                   'Baratheon','Targaryen','Snow','Stark','Lannister']},)


fig_test = px.bar(stack, x="House", y="lineCount", color="Season", title="Total lines said for each House",
             color_discrete_sequence=px.colors.sequential.ice_r)
fig_test.update_layout(xaxis={'categoryorder':'array', 'categoryarray':['Lannister','Stark','Snow','Targaryen','Baratheon',
                                                                   'Greyjoy', 'Mormont', 'Tyrell', 'Martell', 'Tully']})


deaths_count = deaths['Killer'].value_counts().to_frame().reset_index().rename(columns = {'index':'Name', 'Killer':'Kills'})
top5killers = deaths_count[(deaths_count['Name'] == 'Jon Snow') | (deaths_count['Name'] == 'Cersei Lannister')
            |(deaths_count['Name'] == 'Daenerys Targaryen') | (deaths_count['Name'] == 'Arya Stark')
            |(deaths_count['Name'] == 'Grey Worm') ]

fig_char = px.bar(top5killers, x="Kills", y="Name", orientation='h',color_discrete_sequence=px.colors.sequential.Teal_r)

fig_char.update_layout(yaxis={'categoryorder':'array', 'categoryarray':['Grey Worm','Jon Snow','Arya Stark','Cersei Lannister','Daenerys Targaryen' ]})



fig_char.add_layout_image(
    dict(
        source="https://hips.hearstapps.com/digitalspyuk.cdnds.net/17/35/1504282564-greyworm.jpg?crop=1xw:1.0xh;center,top&resize=980:*",
        x=0.925,
        y=0.2,
        sizex=0.2,
        sizey=0.2,
    ))
fig_char.add_layout_image(
    dict(
        source="https://images-na.ssl-images-amazon.com/images/M/MV5BMTk5MTYwNDc0OF5BMl5BanBnXkFtZTcwOTg2NDg1Nw@@._V1_SY1000_CR0,0,665,1000_AL_.jpg",
        x=0.925,
        y=0.4,
        sizex=0.2,
        sizey=0.2,
    ))

fig_char.add_layout_image(
    dict(
        source="https://images-na.ssl-images-amazon.com/images/M/MV5BMTkwMjUxMDk2OV5BMl5BanBnXkFtZTcwMzg3MTg4OQ@@._V1_.jpg",
        x=0.925,
        y=0.6,
        sizex=0.2,
        sizey=0.2,
    ))
fig_char.add_layout_image(
    dict(
        source="https://images-na.ssl-images-amazon.com/images/M/MV5BMTgzNTAxNjExMl5BMl5BanBnXkFtZTcwMDEwNzI4OQ@@._V1._CR954,56,605,670_.jpg",
        x=0.925,
        y=0.8,
        sizex=0.2,
        sizey=0.2,
    ))
fig_char.add_layout_image(
    dict(
        source="https://images-na.ssl-images-amazon.com/images/M/MV5BMjA4MzIxMTQwMF5BMl5BanBnXkFtZTcwMzY2NDg1Nw@@._V1_SY1000_CR0,0,810,1000_AL_.jpghttps://images-na.ssl-images-",
        x=0.925,
        y=1,
        sizex=0.2,
        sizey=0.2,
    ))
deaths_sunburst =  deaths.drop(['Allegiance','Death No.','Episode','Location','Season','Name'],axis =1 ).sort_values('Killer')
deaths_sunburst = deaths_sunburst.groupby(['Method','Killer']).value_counts().to_frame().reset_index()
deaths_sunburst = deaths_sunburst.rename(columns={0:'Kills','Killers House':'House'}).sort_values('Killer')

drop_houses = dcc.Dropdown(
    id='drop_houses',
    clearable=False,
    searchable=False,
    style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': 'rgba(28, 53, 117, 0.56)'},
    options = [{'label':x ,'value':x} for x in deaths_sunburst['House'].unique()],
    value = 'House Stark'
)
episodes['episodeAirYear'] = episodes['episodeAirDate'].apply(lambda x: x.split('-')[0])
my_raceplot = barplot(episodes,  item_column='episodeTitle', value_column='averageRating', time_column='episodeAirYear')
my_raceplot = my_raceplot.plot(item_label='Episodes', value_label='Ratings', frame_duration=600)


app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.Div([
        html.Label(children='Game of Thrones - A Visual Analysis'),
        html.Br(),
    ], id='title_box', className='top_bar'),

    html.Div([
        html.Div([
          html.Div([
                html.Label("Choose the Season or Total:"),
                html.Br(),
                html.Br(),
                radio_season_choice
            ], id='radio_test', className='ext_row'),

            html.Div([
                html.Div([
                    html.Div([
                        html.Label(id='title_scatter'),
                        dcc.Graph(id = 'scatter_fig'),
                    ], className='box', style={'padding-bottom': '15px'}),

                ], style={'width': '40%'}),
                html.Div([

                    html.Div([
                        html.Label(id='choose_season', style={'margin': '10px'}),
                        drop_episodes,
                    ], className='box'),

                    html.Div([
                        html.Div([
                            html.Label('Episode Description', style={'font-size': 'medium'}),
                            html.Br(),
                            html.Br(),
                            html.Div([
                                html.H3(id='description')
                            ]),

                        ], className='box', style={'heigth': '10%'}),
                    ]),

                    html.Div([
                        html.Div([
                            html.Label('Some Data on the Episode ',
                                       style={'font-size': 'medium'}),

                            html.Br(),
                            html.Br(),
                            html.Div([
                                html.Div([
                                    html.H4('Episode Number', style={'font-weight': 'normal'}),
                                    html.H3(id='episode_number')
                                ], className='box_curiosities'),

                                html.Div([
                                    html.H4('Air Date', style={'font-weight': 'normal'}),
                                    html.H3(id='air_date')
                                ], className='box_curiosities'),

                                html.Div([
                                    html.H4('Views( Million )', style={'font-weight': 'normal'}),
                                    html.H3(id='views')
                                ], className='box_curiosities'),

                                html.Div([
                                    html.H4('Number of Votes', style={'font-weight': 'normal'}),
                                    html.H3(id='votes')
                                ], className='box_curiosities'),

                                html.Div([
                                    html.H4('Writer', style={'font-weight': 'normal'}),
                                    html.H3(id='writer')
                                ], className='box_curiosities'),

                                html.Div([
                                    html.H4('Star', style={'font-weight': 'normal'}),
                                    html.H3(id='star1')
                                ], className='box_curiosities'),
                                html.Div([
                                    html.H4('Duration (Minutes)', style={'font-weight': 'normal'}),
                                    html.H3(id='duration')
                                ], className='box_curiosities'),
                                html.Div([
                                    html.H4('Director', style={'font-weight': 'normal'}),
                                    html.H3(id='director')
                                ], className='box_curiosities'),
                            ], style={'display': 'flex'}),



                        ], className='box', style={'heigth': '10%'}),

                    ]),
                ], style={'width': '60%'}),


            ], className='row'),

            html.Div([
                html.Div([
                    html.Label("3. Which Episode has the best ratings ? ",
                                   style={'font-size': 'medium'}),
                    dcc.Graph(figure=my_raceplot, style={'height': '500px'}),

                ], className='box',style = {'width':'60%'}),

                html.Div([
                    html.Label("4. Who is the line champion?",
                                   style={'font-size': 'medium'}),
                    dcc.Graph(figure=fig_test),
                ],className='box',style = {'width':'60%'})
            ],className = 'row'),

            html.Div([
                html.Div([
                    html.Label("5. Kill or Being Killed ?"),
                    html.Br(),
                    html.Label("5.1 Top Killers",
                               style={'font-size': 'medium'}),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(figure=fig_char)
                ], className='box', style={'width': '60%'}),
            html.Div([
                    html.Label("5.2 Type of Kills per House"),
                    html.Br(),
                    html.Label("Select the House:",
                               style={'font-size': 'medium'}),
                    drop_houses,
                    html.Br(),
                    html.Br(),
                    dcc.Graph(id = 'sunb_graph')
                ], className='box', style={'width': '60%'}),

            ], className= 'row'),
          html.Div([
                html.Div([
                    html.Div([
                        html.P(['Group 47', html.Br(),'João Silva (m20211014), Pauline Richard (m20211019), Sarra Jebali (20210765), Andreia Bastos(20210604)'], style={'font-size':'12px'}),
                    ], style={'width':'50%'}),
                    html.Div([
                        html.P(['Sources ', html.Br(), 'https://public.tableau.com/app/profile/isha.garg/viz/TheonewithdataFriendsTVShowViz/Dashboard1\n',
                                'https://www.washingtonpost.com/graphics/entertainment/game-of-thrones'], style={'font-size':'12px'}),
                    ], style={'width':'42%'}),
                ])
          ], className = 'footer', style={'display':'flex'}),
        ], className='main')
    ]),
])




@app.callback(
    [
        Output('title_scatter', 'children'),
        Output('scatter_fig', 'figure'),
        Output('drop_episodes', 'options'),
        Output('drop_episodes', 'value'),
        Output('choose_season', 'children')
    ],
    [
        Input('season_choice', 'value')
    ],
)
def scatter_chart_drop(episodes_select):
    a = int(episodes_select) - 1
    ################## Episode Scatter Plot ##################
    title = '1. Season viewers per episode (episode name per mil views)'
    df = scatter_options[a]

    if a ==8:
        scatter_fig = dict(type='scatter',
             x=df.millionViewers,
             y=df["episodeTitle"],
             #orientation='h',
             marker_color=[scatter_colors[6] if x=='7' else scatter_colors[7] for x in df.seasonNumber])
    else:
        scatter_fig = dict(type='scatter',
                   x=df.millionViewers,
                   y=df["episodeTitle"],
                   #orientation='h',
                   marker_color=scatter_colors[a])

    ################## Dropdown Scatter ##################
    if a == 0:
        options_return = options_s1
        season_chosen = "2. Choose an episode from season 1:"
        comment = ["Look at the beef production emissions! Each kilogram of beef produces almost 60 kg of CO2.",
                   html.Br(), html.Br()]

    elif a==1:
        options_return = options_s2
        season_chosen = "2. Choose an episode from season 2:"
    elif a==2:
        options_return = options_s3
        season_chosen = "2. Choose an episode from season 3:"
    elif a==3:
        options_return = options_s4
        season_chosen = "2. Choose an episode from season 4:"
    elif a==4:
        options_return = options_s5
        season_chosen = "2. Choose an episode from season 5:"
    elif a == 5:
        options_return = options_s6
        season_chosen = "2. Choose an episode from season 6:"
    elif a == 6:
        options_return = options_s7
        season_chosen = "2. Choose an episode from season 7:"
    elif a == 7:
        options_return = options_s8
        season_chosen = "2. Choose an episode from season 8:"

    else :
       options_return = options_s_total
       season_chosen = "2. Choose a total top 10 viewed episode:"

    return title, \
           go.Figure(data=scatter_fig, layout=dict(height=300, font_color='#000000', paper_bgcolor='rgba(0,0,0,0)',
                                               plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20),
                                               margin_pad=10,xaxis=dict(title='Views'), yaxis=dict(title='Episode'))), \
           options_return, \
           options_return[0]['value'], \
           season_chosen


@app.callback(
    [
        Output('episode_number', 'children'),
        Output('air_date', 'children'),
        Output('description', 'children'),
        Output('views', 'children'),
        Output('votes', 'children'),
        Output('writer', 'children'),
        Output('star1', 'children'),
        Output('duration', 'children'),
        Output('director', 'children'),

    ],
    [
        Input('drop_episodes', 'value'),
        #Input('season_choice','value')
    ],
    [State("drop_episodes", "options")]
)
def update_info(drop_value, opt):
    ################## Emissions datset ##################
    the_label = [x['label'] for x in opt if x['value'] == drop_value]



    data_episodes = episodes[episodes["episodeTitle"] == the_label[0]]
    season_str = str(data_episodes["seasonNumber"].values[0])
    epnumber_str = str(data_episodes["episodeNumber"].values[0])
    airdate_str = str(data_episodes["episodeAirDate"].values[0])
    description_str = str(data_episodes["episodeDescription"].values[0])
    millionView_str = str(data_episodes["millionViewers"].values[0])
    numVotes_str = str(data_episodes["numVotes"].values[0])
    writer_str = str(data_episodes["Writer_1"].values[0])
    star_str = str(data_episodes["Star_1"].values[0])
    duration_str = str(data_episodes["Duration"].values[0])
    director_str = str(data_episodes["Director"].values[0])



    return epnumber_str, \
           airdate_str,\
           description_str, \
           millionView_str, \
           numVotes_str, \
           writer_str, \
           star_str, \
           duration_str, \
           director_str

@app.callback(
        Output('sunb_graph', 'figure'),
        Input('drop_houses', 'value'))


def sunburst_graph(house_name_value):
    df = deaths_sunburst[deaths_sunburst.House == house_name_value]
    fig = px.sunburst(df, path = ['Method','Killer'], values = 'Kills',
                    color = 'Method', color_discrete_sequence = px.colors.sequential.ice_r).update_traces(hovertemplate = '%{label}<br>' + 'Number of Kills: %{value}', textinfo = "label + percent entry")

    fig = fig.update_layout({'margin' : dict(t=0, l=0, r=0, b=10),
                        'paper_bgcolor': '#F9F9F8',
                        'font_color':'#363535'})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
