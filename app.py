from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash

external_scripts = ['https://cdn.tailwindcss.com']
dash_app = Dash(__name__, external_scripts=external_scripts, use_pages=True)

app = dash_app.server

dash_app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body class="bg:white dark:bg-darkBG">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

navbar = html.Nav(children=[
    html.Div(children=[
        html.A(children=[html.H1(children='T20TI')], href='/',
               className='dark:text-white text-3xl font-extrabold')
    ], className='flex-1'),
    html.Div(children=[
        html.A(children='Home', href='/',
               className='dark:text-white text-2xl font-bold'),
        html.A(children='Team', href='/team',
               className='dark:text-white text-2xl font-bold')
    ], className='flex flex-initial gap-4')
], className='dark:bg-inherit py-5 px-5 flex')


dash_app.layout = html.Div(children=[
    navbar,

    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # ),


    dash.page_container
])


if __name__ == '__main__':
    dash_app.run(debug=True, port='8000', dev_tools_hot_reload=False)
