from dash import html, dcc, Output, Input, callback
import dash
from typing import List, Optional
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go


dash.register_page(__name__, path='/team')

ABB = {
    "csk": ['Chennai Super Kings', "#ffc107"],
    "mi": ['Mumbai Indians', "#004BA0"],
    "rcb": ['Royal Challengers Bangalore', "#e00c0b"],
    "kkr": ['Kolkata Knight Riders', "#8739fa"],
    "delhi": ['Delhi Capitals', "#17479e"],
    "pbks": ['Punjab Kings', "#ed1c24"],
    "rr": ['Rajasthan Royals', "#e50595"],
    "srh": ['Sunrisers Hyderabad', "#e75900"],
    "gt": ['Gujarat Titans', "#5bcbf5"],
    "lsg": ['Lucknow Super Giants', "#30D5C8"],
}

TEAMS = [val[0] for key, val in ABB.items()]

plotly_tempate = pio.templates['plotly_dark']
URL = 'https://sawlachintan.github.io/cricket_data/ipl_data/'
innings_df = pd.read_csv(f'{URL}innings_df.csv')
info_df = pd.read_csv(f'{URL}info_df.csv')
merge_df = innings_df.merge(info_df[['key', 'date']], on='key')
merge_df['date'] = pd.to_datetime(merge_df['date']).dt.year
merge_df = merge_df.loc[merge_df.batting_team.isin(
    TEAMS), :].reset_index(drop=True)


def test_fn(x: str) -> html.Button: return html.Button(x.upper(), id=f'{x}-btn', n_clicks=0,
                                                       className=f'transition ease-in-out border-{x} border-4 hover:bg-{x} text-black dark:text-white font-bold py-1.5 px-4 rounded w-fit')


layout = html.Div(children=[html.Div(children=[

    # html.H2(children="What is TwenVIZ?",
    #         className='text-2xl font-medium'),
    html.Div(children=[test_fn(x) for x in ABB],
             className='col-span-3 overflow-auto flex gap-2 justify-between'),
    dcc.RangeSlider(2008, 2023, 1, value=[2016, 2023],
                    id='my-range-slider',
                    marks={i: f'{i}' for i in range(2008, 2024)}, className='col-span-2', persistence='years')

], className='dark:text-white flex flex-col gap-5 md:grid md:grid-cols-5 md:gap-4'),
    html.Div(children=[


        dcc.Graph(id='runs-line', config={'displaylogo': False}),
        dcc.Graph(id='bndry-vs-dots', config={'displaylogo': False}),
        dcc.Graph(id='runs-per-wick', config={'displaylogo': False})
    ])], className='px-5 flex flex-col gap-3')


@callback(Output('my-range-slider', 'value'),
          Input('my-range-slider', 'value'))
def clear_persistence(values: List[int]):
    return dash.no_update


@callback(
    output={"all_class": {
        team: Output(f'{team}-btn', 'className') for team in ABB
    }},
    inputs={'all_btns': {
        team: Input(f'{team}-btn', 'n_clicks') for team in ABB
    }}, state={'all_states': {
        team: Input(f'{team}-btn', 'className') for team in ABB
    }})
def on_click(all_btns: dict, all_states: dict) -> dict:

    def find_key(all_btns: dict) -> str:
        for key in all_btns:
            if all_btns[key].triggered:
                return key
        return 'csk'

    c = dash.ctx.args_grouping.all_btns  # type: ignore

    all_class = {team: all_states[team].strip(
        f'bg-{team}').strip() for team in ABB}

    team_trig = find_key(c)

    all_class[team_trig] = f'{all_class[team_trig]} bg-{team_trig}'

    return {'all_class': all_class}


@callback(Output('runs-line', 'figure'), inputs={'all_btns': {
    team: Input(f'{team}-btn', 'n_clicks') for team in ABB
}, 'years': Input('my-range-slider', 'value')})
def runs_graph(all_btns, years):

    def find_key(all_btns: dict) -> str:
        for key in all_btns:
            if all_btns[key].triggered:
                return key
        return 'csk'

    c = dash.ctx.args_grouping.all_btns  # type: ignore

    team_trig = ABB[find_key(c)][0]
    color = ABB[find_key(c)][1]

    all_runs = merge_df[(merge_df.date >= years[0]) & (merge_df.date <= years[1])]\
        .groupby(['date'])\
        .agg({'runs_total': 'sum', 'key': pd.Series.nunique})\
        .reset_index()
    all_runs['avg_runs'] = round(
        all_runs['runs_total'] / (all_runs['key']*2), 2)
    runs = merge_df[(merge_df.batting_team == team_trig) & (merge_df.date >= years[0]) & (merge_df.date <= years[1])]\
        .groupby('date')\
        .agg({'runs_total': 'sum', 'key': pd.Series.nunique})\
        .reset_index()
    runs['avg_runs'] = round(runs['runs_total'] / runs['key'], 2)

    # fig = px.line(runs, 'date', 'runs_total',
    #               template=plotly_tempate, markers=True, range_x=years, color=color, color_discrete_map="identity")
    # fig.update_layout(transition_duration=500)

    fig = go.Figure(layout=dict(transition_duration=500))
    fig.add_trace(go.Scatter(
        x=all_runs['date'], y=all_runs['avg_runs'], mode='lines+markers', name='ALL', line=dict(color='#666')))
    fig.add_trace(go.Scatter(x=runs['date'], y=runs['avg_runs'],
                             mode='lines+markers', name=team_trig, connectgaps=False, line=dict(color=color)))
    fig.update_layout(template=plotly_tempate, xaxis_title='Year',
                      yaxis_title='Avg. Runs per Season')
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    return fig


def phase(over: int) -> str:
    if over < 6:
        return 'powerplay'
    elif over < 16:
        return 'middle'
    else:
        return 'death'


def boundary_over_dots(data: pd.DataFrame,
                       team: Optional[str] = None,
                       period: Optional[List[int]] = [2008, 2022]) -> pd.DataFrame:
    # filter by team if provided
    if team:
        data = data[data.batting_team == team]\
            .copy(deep=True)\
            .reset_index(drop=True)
    if period:
        period = sorted(period)
        data = data[(data['date'] >= period[0]) & (data['date'] <= period[1])]\
            .copy(deep=True)\
            .reset_index(drop=True)

    # group by over and runs. Get count of 0, 4 and 6 in each over
    agg_data = data.groupby(['over', 'runs_batter']).agg(
        {'key': 'count'}).reset_index()
    agg_data = agg_data[(agg_data.runs_batter == 0) | (
        agg_data.runs_batter == 4) | (agg_data.runs_batter == 6)]

    # sum 4 and 6 as one metric
    agg_data['d_b'] = agg_data.groupby(['over', agg_data['runs_batter'] == 0])[
        'key'].transform('sum')
    agg_data = agg_data.reset_index(drop=True)

    # remove the column with 6 in runs column
    dots_bndrs = agg_data.loc[agg_data['runs_batter']
                              != 6, :].reset_index(drop=True)

    # long to wide dataframe
    final_df = dots_bndrs.pivot(
        index='over', columns='runs_batter', values='d_b').reset_index()

    final_df['phase'] = final_df['over'].apply(phase)
    final_df['0'] = final_df.loc[:, 0]
    final_df['4'] = final_df.loc[:, 4]
    final_df['b_over_d'] = round((final_df['4'] / final_df['0']), 2)

    final_df = final_df[['over', '0', '4', 'b_over_d', 'phase']]
    return final_df


@callback(Output('bndry-vs-dots', 'figure'), inputs={'all_btns': {
    team: Input(f'{team}-btn', 'n_clicks') for team in ABB
}, 'years': Input('my-range-slider', 'value')})
def bndry_dots(all_btns, years):
    """create a plot of boundary vs dots to understand how teams have adapted over the years

    Args:
        all_btns (dict): find out teh button triggered
        years (list): range of seasons to include
    """
    def find_key(all_btns: dict) -> str:
        for key in all_btns:
            if all_btns[key].triggered:
                return key
        return 'csk'

    c = dash.ctx.args_grouping.all_btns  # type: ignore

    team_trig = ABB[find_key(c)][0]
    color = ABB[find_key(c)][1]

    all_bndrs = boundary_over_dots(merge_df, period=years)
    for_team = boundary_over_dots(merge_df, team_trig, years)

    everyone_col = ['#ffffff']*20
    colors = [color]*20

    layout = go.Layout(barmode='overlay', transition_duration=500)
    fig = go.Figure(layout=layout)
    fig.add_trace(
        go.Bar(x=for_team['over'], y=for_team['b_over_d'], name=team_trig, marker_color=colors))
    fig.add_trace(go.Bar(x=all_bndrs['over'], y=all_bndrs['b_over_d'],
                  name='All Teams', marker_color=everyone_col, opacity=0.15))
    fig.add_vline(x=5.5, col='#666666', line_dash="dash", line_color="grey")
    fig.add_vline(x=15.5, col='#666666', line_dash="dash", line_color="grey")
    fig.update_layout(title='Ratio of boundaries over dots across the innings',
                      xaxis_title='Over', yaxis_title='Ratio of boundaries over dots', template=plotly_tempate)
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    return fig


def rpw_df(data: pd.DataFrame,
           period: Optional[List[int]] = [2008, 2022]) -> pd.DataFrame:
    # if team:
    #     data = data[data.batting_team == team]\
    #         .copy(deep=True)\
    #         .reset_index(drop=True)
    if period:
        period = sorted(period)
        data = data[(data['date'] >= period[0]) & (data['date'] <= period[1])]\
            .copy(deep=True)\
            .reset_index(drop=True)

    agg_data = data.groupby('batting_team').agg(
        {'runs_total': 'sum', 'wicket_kind': 'count'}).reset_index()
    agg_data['runs_per_wicket'] = round(
        agg_data['runs_total'] / agg_data['wicket_kind'], 2)
    return agg_data


@callback(Output('runs-per-wick', 'figure'), inputs={'all_btns': {
    team: Input(f'{team}-btn', 'n_clicks') for team in ABB
}, 'years': Input('my-range-slider', 'value')})
def rpw_plot(all_btns, years):
    def find_key(all_btns: dict) -> str:
        for key in all_btns:
            if all_btns[key].triggered:
                return key
        return 'csk'

    c = dash.ctx.args_grouping.all_btns  # type: ignore

    team_trig = ABB[find_key(c)][0]
    color = ABB[find_key(c)][1]

    rpw = rpw_df(merge_df, years)
    all_time = round(sum(rpw['runs_total']) / sum(rpw['wicket_kind']), 2)
    layout = go.Layout(barmode='overlay')
    rpw['color'] = '#666666'
    rpw.loc[rpw.batting_team == team_trig, 'color'] = color
    fig = go.Figure(layout=layout)

    fig.add_trace(
        go.Bar(x=rpw['batting_team'], y=rpw['runs_per_wicket'], marker_color=rpw['color']))

    fig.add_hline(y=all_time, line_dash="dot")

    fig.update_layout(title='Runs per wicket',
                      xaxis_title='Teams', yaxis_title='Runs per Wicket', template=plotly_tempate)
    return fig
