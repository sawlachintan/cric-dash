from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash

external_scripts = ['https://cdn.tailwindcss.com']
app = Dash(__name__, external_scripts=external_scripts, use_pages=True)

app.index_string = """
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


df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City",
             barmode="group", template='plotly_dark')

navbar = html.Nav(children=[
    html.Div(children=[
        html.A(children=[html.H1(children='TwenVIZ')], href='/',
               className='dark:text-white text-3xl font-extrabold')
    ], className='flex-1'),
    html.Div(children=[
        html.A(children='Home', href='/',
               className='dark:text-white text-2xl font-bold'),
        html.A(children='Team', href='/team',
               className='dark:text-white text-2xl font-bold')
    ], className='flex flex-initial gap-4')
], className='dark:bg-inherit py-5 px-5 flex')


app.layout = html.Div(children=[
    navbar,

    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # ),


    dash.page_container
])


if __name__ == '__main__':
    app.run(debug=True, port='8000', dev_tools_hot_reload=False)
