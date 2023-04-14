from dash import html, dcc
import dash

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H2(children="What is T20 Team Insights?",
            className='text-2xl font-bold'),
    dcc.Markdown(children='''
    This is an interactive website to visualize how the players and teams in the Indian Premier League. The objective is to ease the access of cricket statsitics for fans new to cricket and the cricket pundits.
    ''', className='dark:text-white'),
    dcc.Markdown(children='''
    The visuals and metrics can help in research and understanding of how teams have performed over the various phases in the match and over a given period of time.
    ''', className='dark:text-white'),
    html.H2(children='Visuals/Metrics',
            className='text-2xl font-bold'),
    html.H3(children='Phase wise Run Rate',
            className='text-xl font-bold'),
    dcc.Markdown(children='''
    The metrics show how a team's approach in the powerplay, middle and death overs. It also shows how they compare to the teams playing in that period of the time.
    ''', className='dark:text-white'),
    html.H3(children='Average Runs per season',
            className='text-xl font-bold'),
    dcc.Markdown(children='''
    This graph is a classical way to represent how the team has performed in general regardless of whom they play, and where they play. It computes the average runs scored in each match in a season and displays the trend.
    ''', className='dark:text-white'),
    dcc.Markdown(children='''
    Ideally, the rate of scoring runs should increase as awareness in the importance of power hitting increases amongst the teams and its players.
    ''', className='dark:text-white'),
    html.H3(children='Boundaries over dots',
            className='text-xl font-bold'),
    dcc.Markdown(children='''
    The graph shows the ratio of boundaries (4s and 6s) over the dot balls faced in the 20 overs played. This should explain the intent of hitting boundaries and reducing the dots to maximize the balls available in the innings.
    ''', className='dark:text-white'),
    dcc.Markdown(children='''
    The expectation is that dot balls faced from the middle overs to end of innings decrease while the boundaries hit steadily increases with an exponential increase in the death overs phase.
    ''', className='dark:text-white'),
    html.H3(children='Runs scored per wicket lost',
            className='text-xl font-bold'),
    dcc.Markdown(children='''
    The graph explains the average runs scored for every wicket lost. This can't be taken at face value because the contribution by bowlers shall almost never be as much as the contribution by top order. This graphs is more about how the batting team is drawing out runs from their players despite losing wickets.
    ''', className='dark:text-white'),
    dcc.Markdown(children='''
    If a team is able to keep the scoreboard running while losing wickets, it shows the depth in batting. However, there can also be the case where the team scores slowly and doesn't lose wickets as fast.
    ''', className='dark:text-white'),
    html.H2(children='Tools Used',
            className='text-2xl font-bold'),
    html.Ul(children=[
        html.Li('Pandas'),
        html.Li('Dash'),
        html.Li('Plotly'),
        html.Li('BeautifulSoup')], className='list-disc list-inside'),
], className='dark:text-white grid grid-flow-row auto-rows-max gap-4 px-5 justify-self-center')

# border-red-500 border-4 rounded
