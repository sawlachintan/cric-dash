from dash import html, dcc
import dash

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H2(children="What is TwenVIZ?",
            className='text-2xl font-medium'),
    dcc.Markdown(children='''
    This is an interactive website to visualize how the players and teams in the Indian Premier League
    ''', className='dark:text-white'),
    html.H2(children='Tools Used',
            className='text-2xl font-medium'),
    html.Ul(children=[
        html.Li('Pandas'),
        html.Li('Dash'),
        html.Li('Plotly'),
        html.Li('BeautifulSoup')], className='list-disc list-inside'),
], className='dark:text-white grid grid-flow-row auto-rows-max gap-4 px-5 justify-self-center')

# border-red-500 border-4 rounded
