
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import copy
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import json
import psycopg2
# import figures_save
import math

ctx = dash.callback_context
ton_k = "k ton"
ton_M = "M ton"
tep_k = "k toe"
tep_M = "M toe"
mw = "MWh"
mw_k = "k MWh"
mw_M = "Millions MWh"


# color_6_live = ["#8DDç3C7", "#fff069", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69"]
# color_6_dead = ["#d3ede9", "#FFF9C4", "#e3e1ed", "#f5d4d0", "#cee1ed", "#fae0c3", "#e7f2d3"]

color_6_live = ["#8DD3C7", "#fff069", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462"]
color_6_dead = ["#96ebde", "#f7efa6", "#c1bae8", "#f0ada5", "#a7d0eb", "#f0c595"]


color_5_live = color_6_live[:5]
color_5_dead = color_6_dead[:5]

color_6_live_d = {"Diesel": color_6_live[0],
                    "Electricity": color_6_live[1],
                    "Natural Gas": color_6_live[2],
                    "Gasoline": color_6_live[3],
                    "LPG": color_6_live[4],
                    "Other": color_6_live[5]}

color_6_dead_d = {"Diesel": color_6_dead[0],
                    "Electricity":color_6_dead[1],
                    "Natural Gas": color_6_dead[2],
                    "Gasoline": color_6_dead[3],
                    "LPG": color_6_dead[4],
                    "Other": color_6_dead[5]}

color_5_live_d = {"Agriculture": color_5_live[0],
                  "Domestic": color_5_live[1],
                    "Industry": color_5_live[2],
                    "Services": color_5_live[3],
                    "Transportation": color_5_live[4]}

color_5_dead_d = {"Agriculture": color_5_dead[0],
                    "Domestic": color_5_dead[1],
                    "Industry": color_5_dead[2],
                    "Services": color_5_dead[3],
                    "Transportation": color_5_dead[4]}

unidades_emissoes = 'ton'
unidades_energia = 'toe'


# JA NAO E PRECISO ESTA FUNCAO, VISTO QUE CRIEI EXCEIS INDEPENDENTES
# def cria_df(file_path):
#     forma_df = pd.read_excel(file_path)
#
#     # errados = ['Indústria', 'Serviços', 'Doméstico']
#     # correctos = ['Industria', 'Servicos', 'Domestico']
#     # forma_df = forma_df.replace(errados, correctos)
#     forma_df.rename(columns={'Outros ': 'Outros'}, inplace=True)
#
#     # aa = forma_df.loc[forma_df['Ano'] == 2016, :]
#     # aa = aa.iloc[:, 1:-1]
#     # aa_sum = aa.to_numpy().sum()
#
#     forma_df.fillna(0, inplace=True)
#     anos = list(forma_df.Ano.unique())
#     # numero_anos = len(anos)
#     forma_df_sem_ano = forma_df.iloc[:, :-1]
#     # forma_sector_df = forma_df_sem_ano.groupby(['Sector']).sum()
#     forma_anual = forma_df.groupby(['Ano']).sum()
#     forma_anual['Total'] = forma_anual.sum(axis=1)
#
#     sector_df = forma_df.transpose().copy()
#     sector_df.rename(columns=sector_df.iloc[0], inplace=True)
#     sector_df.drop('Sector', inplace=True)
#     sector_df_temp = sector_df.iloc[:7, 0:5].copy()
#     sector_df_temp['Ano'] = anos[0]
#     sector_df_temp.reset_index(inplace=True)
#     sector_df_temp.rename(columns={'index': 'Forma'}, inplace=True)
#
#     for ano in anos[1:]:
#         df = sector_df.loc[:, sector_df.loc['Ano', ] == ano].copy()
#         df.loc[:, 'Ano'] = ano
#         df.drop('Ano', axis=0, inplace=True)
#         df.reset_index(inplace=True)
#         df = df.rename(columns={'index': 'Forma'})
#
#         sector_df_temp = pd.concat([sector_df_temp, df], ignore_index=True)
#
#     sector_df = sector_df_temp
#     sector_anual = sector_df.groupby(['Ano']).sum()
#     sector_anual.drop('Forma', axis=1, inplace=True)
#
#     forma_list = sorted(forma_df.columns[1:-1].tolist())
#     sector_list = sorted(sector_df.columns[1:-1].tolist())
#     forma_df = forma_df.round(0)
#     sector_df = sector_df.round(0)
#     forma_anual = forma_anual.round(0)
#     sector_anual = sector_anual.round(0)
#     # forma_sector_df = forma_sector_df.round(0)
#
#     forma_df['color_fill'] = forma_df['Sector'].apply(lambda x: color_5_dead_d[x])
#     forma_df['color_line'] = forma_df['Sector'].apply(lambda x: color_5_live_d[x])
#
#     sector_df['color_fill'] = sector_df['Forma'].apply(lambda x: color_6_dead_d[x])
#     sector_df['color_line'] = sector_df['Forma'].apply(lambda x: color_6_live_d[x])
#
#
#     # forma_df['color_dead'] = color_5_dead * len(anos)
#     # forma_df['color_live'] = color_5_live * len(anos)
#     #
#     # sector_df['color_dead'] = color_6_dead * len(anos)
#     # sector_df['color_live'] = color_6_live * len(anos)
#
#     return forma_df, sector_df, forma_anual, sector_anual, forma_list, sector_list, anos


# def change_df(which_df, primaria_final):
#     if primaria_final == 'primaria':
#         forma_df, sector_df, forma_anual, sector_anual = forma_df_pr, sector_df_pr, forma_anual_pr, \
#                                                                           sector_anual_pr
#     else:
#         forma_df, sector_df, forma_anual, sector_anual  = forma_df_fi, sector_df_fi, forma_anual_fi, \
#                                                                           sector_anual_fi
#
#     return {
#         "forma_df": forma_df,
#         "sector_df": sector_df,
#         "forma_anual": forma_anual,
#         "sector_anual": sector_anual,
#     }[which_df]
#


def cria_cores(cores_5_7, select):
    if cores_5_7 == 5:
        color_dead = color_5_dead
        color_live = color_5_live
        selec_list = sector_list

    else:
        color_dead = color_6_dead
        color_live = color_6_live
        selec_list = forma_list

    colors = color_dead.copy()
    selecao_posi = selec_list.index(select)
    cor_viva = color_live[selecao_posi]
    colors[selecao_posi] = cor_viva

    return colors


# energia_final_path = "data/energia_final.xlsx"
# energia_primaria_path = "data/energia_primaria.xlsx"
# emissoes_path = "data/emissoes_CO2.xlsx"


def set_colors(df, pallete):
    return pallete * int(len(df) / len(pallete))


def create_anual(df):
    df_anual = df.groupby(['Year']).sum()
    df_anual['Total'] = df_anual.sum(axis=1)
    df_anual = df_anual.round(0)
    return df_anual

forma_df_fi = pd.read_excel('data/en/forma_fi_en.xlsx')
sector_df_fi = pd.read_excel('data/en/sector_fi_en.xlsx')
forma_df_pr = pd.read_excel('data/en/forma_pr_en.xlsx')
sector_df_pr = pd.read_excel('data/en/sector_pr_en.xlsx')
forma_df_em = pd.read_excel('data/en/forma_em_en.xlsx')
sector_df_em = pd.read_excel('data/en/sector_em_en.xlsx')
populacao = pd.Series(
    [563312, 550466, 549210, 542917, 530847, 520549, 513064, 506892, 504718, 505526, 506654],
    index=[2001, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
)


forma_df_fi['color_fill'] = set_colors(forma_df_fi, color_5_dead)
forma_df_fi['color_line'] = set_colors(forma_df_fi, color_5_live)
sector_df_fi['color_fill'] = set_colors(sector_df_fi, color_6_dead)
sector_df_fi['color_line'] = set_colors(sector_df_fi, color_6_live)
forma_df_pr['color_fill'] = set_colors(forma_df_pr, color_5_dead)
forma_df_pr['color_line'] = set_colors(forma_df_pr, color_5_live)
sector_df_pr['color_fill'] = set_colors(sector_df_pr, color_6_dead)
sector_df_pr['color_line'] = set_colors(sector_df_pr, color_6_live)
forma_df_em['color_fill'] = set_colors(forma_df_em, color_5_dead)
forma_df_em['color_line'] = set_colors(forma_df_em, color_5_live)
sector_df_em['color_fill'] = set_colors(sector_df_em, color_6_dead)
sector_df_em['color_line'] = set_colors(sector_df_em, color_6_live)

forma_anual_fi = create_anual(forma_df_fi)
sector_anual_fi = create_anual(sector_df_fi).iloc[:, :-1]
forma_anual_pr = create_anual(forma_df_pr)
sector_anual_pr = create_anual(sector_df_pr).iloc[:, :-1]
forma_anual_em = create_anual(forma_df_em)
sector_anual_em = create_anual(sector_df_em).iloc[:, :-1]

forma_list = sorted(forma_df_fi.columns[1:-3].tolist())
sector_list = sorted(sector_df_fi.columns[1:-3].tolist())
anos = forma_anual_fi.index.unique().tolist()
anos.sort()


# Total de energia em texto e milhões ou gigas
total_m_fi = list(forma_anual_fi['Total']/1000)
total_m_fi = ['{:,}'.format(int(tr)).replace(',', ' ') for tr in total_m_fi]
total_m_fi = list(map(str, total_m_fi))
# total_m_fi = [a + ' GWh' for a in total_m_fi]

total_m_pr = list(round(forma_anual_pr['Total'] / 1000, 1))
total_m_pr = ['{:,}'.format(int(tr)).replace(',', ' ') for tr in total_m_pr]
total_m_pr = list(map(str, total_m_pr))
# total_m_pr = [a + 'M' for a in total_m_pr]

total_m_em = list(round(forma_anual_em['Total'] / 1000, 1))
total_m_em = ['{:,}'.format(int(tr)).replace(',', ' ') for tr in total_m_em]
total_m_em = list(map(str, total_m_em))
# total_m_em = [a + ' M' for a in total_m_em]

def get_ano_bar_plot():
    forma_anual = forma_anual_fi
    color_fill = ['#85ceed', ] * len(forma_anual.index)
    color_fill[-1] = '#029CDE'
    color_line = ['#029CDE', ] * len(forma_anual.index)
    total_m = total_m_fi
    my_text = 'aaaa'
    layout_ano_bar = copy.deepcopy(layout)

    fig = go.Figure(data=[go.Bar(
        x=forma_anual.index,
        y=forma_anual['Total'],
        marker_color=color_fill,
        marker_line_color=color_line,
        text=total_m,
        hovertext=my_text,
        hoverinfo='text',
        textposition='outside',
        hoverlabel=dict(font=dict(family=layout['font']['family'])),
    )])

    layout_ano_bar['margin'] = dict(l=0, r=0, b=0, t=0)
    layout_ano_bar['height'] = 200
    layout_ano_bar['dragmode'] = 'select'
    fig.update_layout(layout_ano_bar)
    # fig.update_layout(height=350)
    fig.update_yaxes(automargin=True, range=[0, max(forma_anual['Total']) * 1.15],
                     autorange=False, fixedrange=True, showticklabels=False)
    fig.update_xaxes(fixedrange=True)

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
external_stylesheets = [dbc.themes.BOOTSTRAP, FONT_AWESOME]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# app.server.config['SECRET_KEY'] = '60b69ea75d65bfc586c4e778a9357219'
# app.server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# HEROKU
app.server.config['SECRET_KEY'] = '60b69ea75d65bfc586c4e778a9357219'
app.server.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ifjlbyuxowaqjf:5effd60ed1a219e7ed6a8e0e552f35629cf5cdce9fc23962ecc5e3f67576aeb4@ec2-54-246-89-234.eu-west-1.compute.amazonaws.com:5432/d1ddrskt434lql'
app.server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app.server)

class Pessoas(db.Model):
    __tablename__ = "registo"
    id = db.Column(db.Integer, primary_key=True)
    primaria = db.Column(db.String(20))
    final = db.Column(db.String(20))
    emissoes = db.Column(db.String(20))

    def __repr__(self):
        return f"pessoas('{self.primaria}', '{self.final}', '{self.emissoes}')"

size_generico = 15
# family_generico = "'Abel', sans-serif"
family_generico = "'Questrial', sans-serif"


layout = dict(
    font=dict(
        size=size_generico,
        family=family_generico,
    ),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    hoverlabel=dict(font=dict(size=size_generico, family=family_generico))
)


layout_ano_bar = copy.deepcopy(layout)
layout_ano_bar['margin'] = dict(l=0, r=4, b=0, t=0)
layout_ano_bar['height'] = 200
layout_ano_bar['dragmode'] = 'select'
layout_ano_bar['xaxis'] = dict(fixedrange=True)
layout_ano_bar['yaxis'] = dict(automargin=True, autorange=False, fixedrange=True, showticklabels=False)

layout_donut = copy.deepcopy(layout)
layout_donut['legend'] = go.layout.Legend(
    # x=1.1,
    # y=-0.2,
    traceorder="normal",
    font=dict(
        # size=13,
        color="black"
    ),
    bgcolor='rgba(0,0,0,0)',
    orientation='h'
)
layout_donut['autosize'] = True
layout_donut['margin'] = dict(l=25, r=35, b=20, t=20)


layout_bar_single = copy.deepcopy(layout)
layout_bar_single['margin'] = dict(l=0, r=30, b=0, t=0)
layout_bar_single['height'] = 300
layout_bar_single['hovermode'] = "y"

layout_ano_line = copy.deepcopy(layout)
layout_ano_line['legend'] = go.layout.Legend(
    y=1,
    x=0.5,
    yanchor='bottom',
    xanchor='right',
    font=dict(
        # size=13,
        color="black"
    ),
    orientation='h',
    bgcolor='rgba(0,0,0,0)',

)
layout_ano_line['hovermode'] = "x"
layout_ano_line['margin'] = dict(l=10, r=10, b=10, t=10)
layout_ano_line['height'] = 300
layout_ano_line['hoverlabel'] = dict(font=dict(family=layout['font']['family']))

# SIDEBAR_STYLE = {
#     # "position": "fixed",
#     "top": 0,
#     # "margin-top": 100,
#     "left": 0,
#     # "bottom": 0,
#     'height': '100%',
#     "width": "40rem",
#     "padding": "2rem 1rem",
#     "background-color": "#f8f9fa",
#     "float": "left",
#     "position": "absolute",
#     "z - index": 99999,
#     "box-shadow": "2px 2px 2px lightgrey"
# }

SIDEBAR_STYLE = {
    "background-color": "#f8f9fa",
    "padding": "0% 2% 0% 2%",

    'height': '100%',
    'font-family': layout['font']['family'],
    'margin-bottom': '0'
}



    # 'padding-bottom': '99999px', 'margin-bottom': '-99999px'
#
#
# INSIDE_STYLE = {
#     "margin-left": "2rem",
#     "margin-right": "2rem",
#     "padding": "2rem 2rem",
# }
#
CONTENT_STYLE_1 = {
    "padding": "2%",
    'height': '98%',
    'font-family': layout['font']['family']

}

CONTENT_STYLE_2 = {
    "padding": "2%",
    'height': '100%',
    'font-family': layout['font']['family']

}


#
# nomes = ['primaria', 'final', 'emissoes']
# headers = ['Energia Primária', 'Energia Final', 'Emissões de CO2']
# id_m = ['modal-p', 'modal-f', 'modal-em']
# id_l = ['link-file-p', 'link-file-f', 'link-file-em']
# id_c = ['close-p', 'close-f', 'close-em']
# id_d = ['download-p', 'download-f', 'download-em']
# id_r = ['radio-p', 'radio-f', 'radio-em']
# id_t = ['target-p', 'target-f', 'target-em']
# links = ['/download/Primary_Energy_Lisbon.xlsx', '/download/Final_Energy_Lisbon.xlsx', '/download/CO2_Emissions_Lisbon.xlsx']
# divs = ['hidden-p', 'hidden-f', 'hidden-em']
#
# ids_modal = {nom : {
#     'header': h,
#     'id_m': m,
#     'id_l': l,
#     'id_c': c,
#     'id_d': d,
#     'id_r': r,
#     'id_t': t,
#     'link': l2,
#     'div':div
#
# } for nom, h, m, l, c, d, r, t, l2, div in zip(nomes, headers, id_m, id_l, id_c, id_d, id_r, id_t, links, divs)}
#
#
#
# def create_modal(tab):
#     header = ids_modal[tab]['header']
#     id_m = ids_modal[tab]['id_m']
#     id_l = ids_modal[tab]['id_l']
#     id_c = ids_modal[tab]['id_c']
#     id_d = ids_modal[tab]['id_d']
#     id_r = ids_modal[tab]['id_r']
#     link = ids_modal[tab]['link']
#     div = ids_modal[tab]['div']
#     return html.Div(
#         [
#             dbc.Modal(
#                 [
#                     dbc.ModalHeader("DOWNLOAD - {}".format(header)),
#                     dbc.ModalBody(["What's the purpose of this download??",
#                                    dcc.RadioItems(
#                                        options=[
#                                            {"label": "Personal", "value": 1},
#                                            {"label": "Professional", "value": 2},
#                                            {"label": "Academic", "value": 3},
#                                        ],
#                                        # value=1,
#                                        id=id_r,
#                                    ),
#                                    html.Div(id=div, style={'display': 'none'})
#
#                                    ]),
#
#                     dbc.ModalFooter(
#
#                         [
#                             html.A(
#                                 children=dbc.Button("Download", id=id_d, className="ml-auto", color="primary",size="lg",
#                                                     disabled=True),
#                                 href = link,
#                                 id=id_l
#                             ),
#                             dbc.Button(
#                                 "Close", id=id_c, className="m1-auto",size="lg", color="danger"
#                             )]
#                     ),
#                 ],
#                 id=id_m,
#                 centered=True,
#                 style={'font-family': layout['font']['family']}
#             ),
#         ], style={'font-family': layout['font']['family']},
#     )
#
#
# modal_p = create_modal('primaria')
# modal_f = create_modal('final')
# modal_em = create_modal('emissoes')

# modal = dbc.Modal(
#     [
#         dbc.ModalHeader("DOWNLOAD DE FICHEIROS - {}".format("aaa")),
#         dbc.ModalBody(["Qual o propósito deste download?",
#                        dcc.RadioItems(
#                            options=[
#                                {"label": "Pessoal", "value": 1},
#                                {"label": "Profissional", "value": 2},
#                                {"label": "Académico", "value": 3},
#                            ],
#                            # value=1,
#                            id="radio-modal",
#                        ),
#                        html.Div(id="hidden", style={'display': 'none'})
#
#                        ]),
#
#         dbc.ModalFooter(
#
#             [
#                 html.A(
#                     children=dbc.Button("Download", id='download-file', className="ml-auto", color="primary", size="lg",
#                                         disabled=True),
#                     # href=link,
#                     id='file-link'
#                 ),
#                 dbc.Button(
#                     "Close", id='cancel', className="m1-auto", size="lg", color="danger"
#                 )]
#         ),
#     ],
#     id='modal',
#     centered=True,
#     style={'font-family': layout['font']['family']}
# ),

# cartao com butoes final/primaria
card_final_primaria = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H6("Select energy type:", style={'font-style': 'italic'}
                               ), width={"size": 6}),

                dbc.Col(

                        dcc.Dropdown(
                            id='dd-primaria-final',
                            options=[{'label': 'Primary', 'value': 'Primary'},
                                       {'label': 'Final', 'value': 'Final'}],
                            clearable=False,
                            value='Final',
                            style= dict(font=layout['font'])

                        ),
                    width=6, align='center'
                ),
            ],
            align="center", justify='center'
        ),
    ]
)


# cartao com butoes forma/sector
card_forma_sector = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H6(id='header-forma-sector', style={'font-style': 'italic'}
                               ), width={"size": 6}),

                dbc.Col(
                    dcc.Dropdown(
                        id='dd-forma-sector',
                        options=[{'label': 'Form of Energy', 'value': 'Form'},
                                 {'label': 'Sector', 'value': 'Sector'}],
                        clearable=False,
                        value='Form'
                    ), width=6
                ),
            ],
            align="center", justify='center'
        ),
    ]
)

##029CDE , "background-color": "#029CDE"
def create_year_button(ano):
    butao = dbc.Button(ano, color='primary', outline=True, id='sel_{}'.format(ano), className='bt-anos')

    return butao


info_button_year = html.Div(
    [
        html.I(className="fas fa-question-circle fa-sm", id="target_year"),
        dbc.Tooltip(target="target_year",
                    style={'font-size': '1.4rem'}, id='tt-year-bar'),
    ],
    className="p-1 text-muted"
)


# slider + grafico de barras
year_selector = html.Div([
# "<br>(Seleccione o ano pretendido)"
    dbc.Row([html.H5(id='header-ano-bar', style={'textAlign': 'center'}), info_button_year], align='center', justify='center',style={'textAlign': 'center', "margin": "0% 2% 0% 2%"}),
    html.P(dcc.Markdown('''**Select year:**'''), style={'textAlign': 'center', "padding": "0% 0% 1% 0%", 'font-style': 'italic'}),

    html.Div(
        [html.Div(create_year_button(2008), style={'display': 'inline'}), create_year_button(2009), create_year_button(2010),
         create_year_button(2011), create_year_button(2012), create_year_button(2013),
         create_year_button(2014), create_year_button(2015), create_year_button(2016),
         dbc.Button(2017, color='primary', outline=False, id='sel_2017', className='bt-anos')
],
        style={"margin-right": "0.5rem"}
    ),
    html.Div(children=json.dumps(str(2017)), id='mem-year', style={'display':'none'}),
    dcc.Loading(id="loading-ano-bar", type="circle",
                children=[
                    dcc.Graph(id="ano-bar-graph", config={'displayModeBar': False})]),


    # html.Div([dcc.Slider(id='year-selected', min=min(anos), max=max(anos), value=min(anos),
    #                      marks={str(ano): str(ano) for ano in anos})],
    #          style={'textAlign': "center", "margin-left": "1rem", "margin-right": "1rem", "padding": "1rem 1rem"}
    #          ),
    html.Div(id='hidd_year_bt', style={'display': 'none'})
        ])

download_button_em = html.Div(
    [
    html.A(
        children=html.I(
            className="fas fa-file-download fa-lg",
            id="target-em",
        ),
        href='javascript:void(0);',
        id='link-file-em'
    ),
    dbc.Tooltip(
        ' Download: CO2 emissions in the city of Lisbon, by sector and energy form (.xlsx).',
        target="target-em", style={'font-size': '1.4rem'}, id='tooltip-em'),
        ],
    className="p-3 text-muted", style={'textAlign': 'center'})



download_button_p = html.Div(
    [
    html.A(
        children=html.I(
            className="fas fa-file-download fa-lg",
            id="target-p",
        ),
        href='javascript:void(0);',
        id='link-file-p'
    ),
    dbc.Tooltip(
        ' Download: Primary energy consumption in the city of Lisbon, by sector and energy form (.xlsx).',
        target="target-p", style={'font-size': '1.4rem'}, id='tooltip-p'),
        ],
    className="p-3 text-muted")

download_button_f = html.Div(
    [
    html.A(
        children=html.I(
            className="fas fa-file-download fa-lg",
            id="target-f",
        ),
        href='javascript:void(0);',
        id='link-file-f'
    ),
    dbc.Tooltip(
        ' Download: Final energy consumption in the city of Lisbon, by sector and energy form (.xlsx).',
        target="target-f", style={'font-size': '1.4rem'}, id='tooltip-f'),
        ],
    className="p-3 text-muted")



sidebar = html.Div(
    [
        # html.H3("Matriz de Energia", className="display-6"),
        # html.Hr(),

        dbc.Tabs(
                [
                    dbc.Tab([
                             html.Br(),
                             html.Div([card_final_primaria], style={"padding": "0% 10% 0% 10%"}),
                             html.Hr(),

                             ], label="Energy", tab_id="tab-energia",
                            tab_style={'width': '50%', 'textAlign': 'center', 'font-size': '1.7rem'}),

                    dbc.Tab([html.Br()],
                            label="Emissions", tab_id="tab-emissoes",
                            tab_style={'width': '50%', 'textAlign': 'center', 'font-size': '1.7rem'}),
                ],
                id="tabs",
                # card=True,
                active_tab="tab-energia",
        ),

        html.Div([card_forma_sector], style={"padding": "0% 10% 0% 10%"}),
        html.Hr(),
        html.Div([year_selector], style={"padding": "0% 0% 0% 0%"}),
        html.Hr(),
        dbc.Row(html.H5('DOWNLOADS:', style={'font-weight': 'bold', "textAlign": "center"}), align='center', justify='center'),
        # html.Hr(),
        html.Div(dbc.Row([html.P('CO2 Emissions:', style={'textAlign': 'center'}), download_button_em], align='center', justify='center'), id="down-em-container", style={'display': 'none'}),
        html.Div(
            [
            dbc.Row(
                [
                dbc.Col(dbc.Row([html.P('Final Energy:'), download_button_f],align='center', justify='center'), md=6),
                dbc.Col(dbc.Row([html.P('Primary Energy:'), download_button_p],align='center', justify='center'), md=6)
                 ],

                align='center',  justify='center'),
            ],
            id="down-pf-container")

    ],
    style=SIDEBAR_STYLE,
    className="pretty_container",
)
down_but = dbc.Button(
    "DOWNLOAD",
    id="dwn",
    size="lg",
    # className="mb-3",
    # outline=True,
    color="link",
)

# Donut Container
donut_container = html.Div([

                    dbc.Row(
                        [
                            html.Div([html.H5(id='header-donut',
                                             style={"textAlign": "center", 'margin': 'auto', 'padding': '8px'}
                                             )
                                      ],
                                     className="twelve columns")
                        ],
                        style={"textAlign": "center"}, className="pretty_container_2 row"
                    ),

                    dbc.Row(
                        [
                            html.Div([dcc.Loading(id="loading-donut", type="circle",
                                                  style={'margin-left': '0%', 'margin-top': '10%'},
                                                  children=[dcc.Graph(id="donut-graph", config={'displayModeBar': False}, style={'margin-bottom': '4%'})])],

                                    # align="center"
                                     className="ten columns",
                                     # style={
                                     #     "margin-left": "10%",
                                     # #     "margin-bottom": "0%",
                                     # #     "bottom": 0,
                                     #     "padding": "1% 1% 15% 0%",
                                     # },
                                     )
                        ],
                        justify='center'
                        # className="row"
                    )

                ],
                    style=CONTENT_STYLE_1,
                    className="pretty_container")


# single bar Container
single_bar_container = html.Div([
                    html.Div(
                        [
                            # html.Abbr("\u003f\u20dd", title="Hello, I am hover-enabled helpful information."),

                            html.Div(
                                [
                                    dbc.Col([

                                        html.H5(id='text-bar',
                                               style={"textAlign": "center", 'margin': 'auto', 'padding': '8px'}),
                                        ]),

                                ],

                                id='text-bar-div',
                                className="bare_container twelve columns",
                                style={"textAlign": "center"}),
                        ],
                        className="pretty_container_2 row"
                    ),
                    html.Div(
                        [
                            dbc.Row([
                                dbc.Col(html.Div(id='select-dd-text'), lg=4, style={'font-style': 'italic', 'padding': '0% 2%', 'textAlign':'center'}),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='dropdown-single',
                                        clearable=False,

                                            ), lg=4
                                ),
                                dbc.Col(html.Div(id='value-dd-text'), lg=3,
                                        style={'font-weight': 'bold', "textAlign": "center", 'font-size': '1.7rem'})
                            ],  no_gutters=True,  align="center", justify='center'),

                            html.Hr(),



                            html.Div([dcc.Loading(id="loading-single-bar", type="circle",
                                                  style={'margin-left': '0%', 'margin-top': '10%'},
                                                  children=[html.Div([dcc.Graph(id="bar-single-graph", config={'displayModeBar': False})],
                                                                     id='single_bar_div')]
                                                  )
                                      ],
                                     )
                        ],
                    )

                ],

    # id='single_bar_container',

    style=CONTENT_STYLE_1,
    className="pretty_container",
)

year_line_container = html.Div([
    html.Div(
        [
            html.Div([html.H5(id='header-ano-line',
                              style={"textAlign": "center", 'margin': 'auto', 'padding': '8px'}
                              )
                      ],
                     className="twelve columns")
        ],
        style={"textAlign": "center"}, className="pretty_container_2 row"
    ),

    html.Div(
        [
            dcc.Loading(
                id="loading-ano-line",
                type="circle",
                children=[dcc.Graph(id="ano-line-graph", config={'displayModeBar': False})]
            )
        ],
        className="twelve columns"
    ),

],
    className="pretty_container",
    style=CONTENT_STYLE_2
)
#
# dom_line_container = html.Div([
#     html.Div(
#         [
#             html.Div([html.H5(id='header-ano-dom',
#                               style={"textAlign": "center", 'margin': 'auto', 'padding': '8px'}
#                               )
#                       ],
#                      className="twelve columns")
#         ],
#         style={"textAlign": "center"}, className="pretty_container_2 row"
#     ),
#
#     html.Div(
#         [
#             dcc.Loading(
#                 id="loading-ano-dom",
#                 type="circle",
#                 children=[dcc.Graph(id="ano-line-dom", config={'displayModeBar': False})]
#             )
#         ],
#         className="twelve columns"
#     ),
#
# ],
#     className="pretty_container",
#     style=CONTENT_STYLE_2
# )
# ], id='single_bar_container', style={'display': 'none'})

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Energy Matrix</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''



app.layout = html.Div([
    # dcc.Store(id='memory_p_f'),
    dcc.Store(id='memory_s_f'),
    dbc.Row(
        [
            dbc.Col(sidebar, lg=4, style=dict(font=layout['font'])),

            dbc.Col([

                dbc.Row([
                    dbc.Col(donut_container, lg=6),
                    dbc.Col(single_bar_container, lg=6),
                    ], justify="start"),

                dbc.Row([
                    dbc.Col(year_line_container, lg=12)

                ], justify="start"),
                # dbc.Row([
                #     dbc.Col(dom_line_container, md=12)
                #
                # ], justify="start")

            ],
                lg=8)

        ],
        justify="start"

    ),
    dbc.Modal(
        [
            dbc.ModalHeader(id='header-modal'),
            dbc.ModalBody(["What is the purpose of this download?",
                           dcc.RadioItems(
                               options=[
                                   {"label": "Personal", "value": 1},
                                   {"label": "Professional", "value": 2},
                                   {"label": "Academic", "value": 3},
                               ],
                               # value=1,
                               id="radio-modal",
                           ),
                           html.Div([None],id="hidden", style={'display': 'none'}),
                           html.Div(id="hidden2", style={'display': 'none'}),
                           html.Div(id="hidden3", style={'display': 'none'})

                           ]),

            dbc.ModalFooter(

                [
                    html.A(
                        children=dbc.Button("Download", id='download-file', className="ml-auto", color="primary",
                                            size="lg",
                                            disabled=True),
                        # href=link,
                        id='file-link'
                    ),
                    dbc.Button(
                        "Close", id='cancel', className="m1-auto", size="lg", color="danger"
                    )]
            ),
        ],
        id='modal',
        centered=True,
        style={'font-family': layout['font']['family']}
    ),
    # html.Div(id='mem-df', style={'display': 'none'}),
],
)
#
# @app.callback(
#     Output('mem-df', 'children'),
#     [
#     Input('tabs', 'active_tab'),
#     Input('dd-primaria-final', 'value'),
#     Input('dd-forma-sector', 'value')
#     ]
# )
#
# def update_memory_df(at,prim_fin, form_sect):
#
#     if at == 'tab-energia':
#
#         if prim_fin == 'Final':
#
#             if form_sect == 'Sector':
#                 df_1 = sector_df_fi
#                 df_2 = forma_df_fi
#                 anual = sector_anual_fi
#
#             else:
#                 df_1 = forma_df_fi
#                 df_2 = sector_df_fi
#                 anual = forma_anual_fi
#
#
#         else:
#
#             if form_sect == 'Sector':
#                 df_1 = sector_df_pr
#                 df_2 = forma_df_pr
#                 anual = sector_anual_pr
#
#             else:
#                 df_1 = forma_df_pr
#                 df_2 = sector_df_pr
#                 anual = forma_anual_pr
#
#     else:
#
#         if form_sect == 'Sector':
#             df_1 = sector_df_em
#             df_2 = forma_df_em
#             anual = sector_anual_em
#         else:
#             df_1 = forma_df_em
#             df_2 = sector_df_em
#             anual = forma_anual_em
#
#
#     datasets = {
#         'df_1': df_1.to_json(orient='split', date_format='iso'),
#         'df_2': df_2.to_json(orient='split', date_format='iso'),
#         'anual': anual.to_json(orient='split', date_format='iso'),
#     }
#     return json.dumps(datasets)

@app.callback(
    Output('modal', "is_open"),
    [
        Input('target-p', "n_clicks"),
        Input('target-f', "n_clicks"),
        Input('target-em', "n_clicks"),
        Input('download-file', "n_clicks"),
        Input('cancel', "n_clicks")],
    [State('modal', "is_open")],
)
def toggle_modal_consumo(np, nf, ne, nd, close, is_open):
    if np or nf or ne or nd or close or is_open:
        return not is_open
    else:
        return is_open


@app.callback(
Output('download-file', 'disabled'),
[Input('radio-modal', "value"), Input('cancel', "n_clicks")]
)
def enable_dwnld_button(value, n):
    if value:

        return False
    if n:
        return True
    else:
        return True


@app.callback(
Output('radio-modal', "value"),
[Input('modal', "is_open")]
)
def enable_radio(n):
    if n:
        return None


@app.callback(
    Output('hidden', 'children'),
    [
        Input('target-p', "n_clicks"),
        Input('target-f', "n_clicks"),
        Input('target-em', "n_clicks"),
]
)
def regista_target(np, nf, ne):
    if not ctx.triggered:
        raise PreventUpdate
    # print(ctx.triggered[0]['prop_id'])

    if ctx.triggered[0]['prop_id'] == 'target-p.n_clicks':
        return json.dumps(str(0))

    elif ctx.triggered[0]['prop_id'] == 'target-f.n_clicks':
        return json.dumps(str(1))

    elif ctx.triggered[0]['prop_id'] == 'target-em.n_clicks':
        return json.dumps(str(2))
    else:
        return None

# links = ['/download/Energia_Primaria_Lisboa.xlsx', '/download/Energia_Final_Lisboa.xlsx', '/download/Emissoes_CO2_Lisboa.xlsx']


@app.callback(
    [
    Output('header-modal', 'children'),
    Output('file-link', 'href'),
    ],
    [
        Input('target-p', "n_clicks"),
        Input('target-f', "n_clicks"),
        Input('target-em', "n_clicks"),
]
)
def update_link(np, nf, ne):
    if not ctx.triggered:
        raise PreventUpdate

    if ctx.triggered[0]['prop_id'] == 'target-p.n_clicks':
        return "DOWNLOAD - Primary Energy",'/download/Primary_Energy_Lisbon.xlsx'

    elif ctx.triggered[0]['prop_id'] == 'target-f.n_clicks':
        return "DOWNLOAD - Final Energy", '/download/Final_Energy_Lisbon.xlsx'

    elif ctx.triggered[0]['prop_id'] == 'target-em.n_clicks':
        return "DOWNLOAD - CO2 Emissions", '/download/CO2_Emissions_Lisbon.xlsx'
    else:
        return 'javascript:void(0);'

@app.callback(
    Output('hidden2', 'children'),
    [Input('radio-modal', "value")]
)
def regista_tipo(tipo):
    if not ctx.triggered:
        raise PreventUpdate
    if tipo == 1:
        letra = 'pessoal'

    elif tipo == 2:
        letra = 'profissional'

    else:
        letra = 'academico'
    return json.dumps(letra)

@app.callback(
    Output('hidden3', 'children'),
    [

        Input('download-file', "n_clicks"),
    ],
    [
        State('hidden2', "children"),
        State('hidden', "children"),
    ]
)
def regista_pessoas(nd, letra, num):
    if not ctx.triggered:
        raise PreventUpdate

    # print(ctx.triggered)
    try:
        letra = json.loads(letra)
    except (TypeError, ValueError) as e:
        raise PreventUpdate
    try:
        num = int(json.loads(num))
    except (TypeError, ValueError) as e:
        raise PreventUpdate

    if ctx.triggered[0]['prop_id'] == 'download-file.n_clicks':

        pessoa_lista = ["", "", ""]
        pessoa_lista[num] = letra
        registo = Pessoas(primaria=pessoa_lista[0], final=pessoa_lista[1], emissoes=pessoa_lista[2])
        db.session.add(registo)
        db.session.commit()
        return None


#
# registo = openpyxl.load_workbook('data/registo_pessoas.xlsx')
# registo_sheet = registo['Sheet1']
# registo_sheet[position] = registo_sheet[position].value + 1
# registo.save('data/registo_pessoas.xlsx')

# @app.callback(
#     [Output("primaria", "active"),
#      Output("final", "active"),
#      # Output("memory-output", "data")
#      ],
#     [Input('primaria', 'n_clicks'),
#      Input('final', 'n_clicks'),
#      ],
#     [State('memory_p_f', 'data')]
# )
# def update_color_data_pf(primaria, final, memory_p_f):
#     if not ctx.triggered:
#         raise PreventUpdate
#
#     trigger = ctx.triggered[0]['prop_id'].split('.')[0]
#
#     memory_p_f = memory_p_f or {'final': 1, 'primaria': 0}
#
#     if trigger == 'primaria':
#         if memory_p_f['primaria'] == 1:
#             return dash.no_update, dash.no_update
#         else:
#             # datasets = {
#             #     'forma_df': forma_df_pr.to_json(orient='split'),
#             #     'sector_df': sector_df_pr.to_json(orient='split'),
#             #     'forma_anual': forma_anual_pr.to_json(orient='split'),
#             #     'sector_anual': sector_anual_pr.to_json(orient='split'),
#             #     'forma_sector_df': forma_sector_df_pr.to_json(orient='split')
#             # }
#             return True, False
#     else:
#         if memory_p_f['final'] == 1:
#             return dash.no_update, dash.no_update
#         # datasets = {
#         #     'forma_df': forma_df_fi.to_json(orient='split'),
#         #     'sector_df': sector_df_fi.to_json(orient='split'),
#         #     'forma_anual': forma_anual_fi.to_json(orient='split'),
#         #     'sector_anual': sector_anual_fi.to_json(orient='split'),
#         #     'forma_sector_df': forma_sector_df_fi.to_json(orient='split')
#         # }
#         else:
#             return False, True
#         # json.dumps(datasets)
#
#
# @app.callback(
#     [Output("sector", "active"),
#      Output("forma", "active")],
#     [Input('dd-forma-sector', 'value')]
# )
# def update_color_sf(form_sect):
#     if not ctx.triggered:
#         raise PreventUpdate
#
#     trigger = ctx.triggered[0]['prop_id'].split('.')[0]
#
#     if form_sect == 'Sector':
#         return True, False
#
#     else:
#         return False, True

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory("data/en", path, as_attachment=True)

#
# @app.callback(
#     [Output(f"sel_{a}", "style") for a in anos] + [Output("2008-hide", "style")],
#     [Input("radio-pop", "value")]
# )
# def update_hide_2008(per_capita):
#     if not ctx:
#         raise PreventUpdate
#     if per_capita == 2:
#         return [{'width': '11.1111111111111111111%'}]*len(anos) + [{'display': 'none'}]
#     else:
#         return [{}]*len(anos) + [{'display': 'inline'}]


@app.callback(
    [Output(f"sel_{a}", "outline") for a in anos]
    + [Output("mem-year", "children")]
    ,
    [Input("ano-bar-graph", "clickData")] + [Input(f"sel_{a}", "n_clicks") for a in anos]
)
def update_button_outline(ano_bar_graph_selected, sel_2008, sel_2009, sel_2010, sel_2011, sel_2012, sel_2013, sel_2014, sel_2015, sel_2016, sel_2017):
    if not dash.callback_context.triggered:
        raise PreventUpdate
    # print(ctx.triggered[0]['prop_id'])

    if ctx.triggered[0]['prop_id'] != 'ano-bar-graph.clickData':
        anos_bool = [ctx.triggered[0]['prop_id'] != f'sel_{a}.n_clicks' for a in anos]
        if sum(anos_bool) == len(anos):
            #anos_bool = [True]*(len(anos)-1) + [False]
            raise PreventUpdate

        a_pos = anos_bool.index(False)
        ano = anos[a_pos]

        # print(anos_bool, ano)
        return anos_bool + [json.dumps(str(ano))]
    else:
        print(type(ano_bar_graph_selected['points'][0]['x']))
        anos_bool = [str(ano) != ano_bar_graph_selected['points'][0]['x'] for ano in anos]
        print(anos_bool)
        a_pos = anos_bool.index(False)
        ano = anos[a_pos]
        return anos_bool + [json.dumps(str(ano))]


@app.callback([
Output('tt-year-bar', 'children'),
    Output('header-ano-bar', 'children'),
               Output('header-forma-sector', 'children')],
              [Input('tabs', 'active_tab'),
               Input('dd-primaria-final', 'value'),

               ]
              )
def headers_emissoes(at, prim_fin):
    if not dash.callback_context.triggered:
        raise PreventUpdate
    if at == "tab-emissoes":
        return dcc.Markdown('''**k ton** stands for 1 000 tonnes of CO2 emissions.'''), 'CO2 Emissions per year (k ton)', 'CO2 Emissions per:'

    else:
        if prim_fin == 'Primary':
            head_a_b = 'Primary Energy consumption per year (k toe)'
            return dcc.Markdown('''**k toe** stands for 1 000 tonnes of oil equivalent.'''), head_a_b, 'Select disaggregation:'
        else:

            head_a_b = 'Final Energy consumption per year (GWh)'
            text_tool = dcc.Markdown('''**GWh** (Gigawatt hour) stands for 1 000 MWh or 1 000 000 kWh.''')

            return text_tool, head_a_b, 'Select disaggregation:'

#
# @app.callback(
#     [Output(f"sel_{a}", "outline") for a in anos],
#     [Input(f"sel_{a}", "n_clicks") for a in anos]
# )
# def update_butoes(sel_2008, sel_2009, sel_2010, sel_2011, sel_2012, sel_2013, sel_2014, sel_2015, sel_2016, sel_2017):
#
#     anos_bool = [ctx.triggered[0]['prop_id'] == f'sel_{a}.n_clicks' for a in anos]
#     if sum(anos_bool) == 0:
#         anos_bool = [False]*(len(anos)-1) + [True]
#     # a_pos = anos_bool.index(True)
#     # ano = anos[a_pos]
#
#     return anos_bool


@app.callback(
    Output("hidd_year_bt", "children"),
    [

]
)

@app.callback(
    [
    Output('down-pf-container', 'style'),
    Output('down-em-container', 'style'),
    Output("ano-bar-graph", "figure"),

    ],
    [
        # Input("year-selected", "value"),
     Input('dd-primaria-final', 'value'),
     Input('tabs', 'active_tab'),
     Input("mem-year", "children"),



    ]
)
def update_ano_bar(prim_fin, at, ano_mem):
    if not ctx.triggered:
        raise PreventUpdate

    try:
        ano = int(json.loads(ano_mem))
    except (ValueError, TypeError) as e:
        raise PreventUpdate

    if at == "tab-emissoes":
        visi_em = {'display': 'inline'}
        visi_pf = {'display': 'none'}

        forma_anual = forma_anual_em
        total_m = total_m_em
        # unidade = unidades_emissoes
        unidade = ' ton'



    else:
        visi_em = {'display': 'none'}
        visi_pf = {'display': 'inline'}

        if prim_fin == 'Primary':


            unidade = ' toe'
            forma_anual =forma_anual_pr
            total_m = total_m_pr


        else:

            unidade = ' MWh'

            forma_anual = forma_anual_fi
            total_m = total_m_fi

    try:
        ano_posi = list(forma_anual.index).index(ano)
    except ValueError:
        ano_posi = list(forma_anual.index).index(2009)
    color_fill = ['#85ceed', ] * len(forma_anual.index)
    color_fill[ano_posi] = '#029CDE'
    color_line = ['#029CDE', ]*len(forma_anual.index)


    my_text = ['Total: ' + '{:,}'.format(int(tr)).replace(',', ' ') + unidade + '<br>Year: ' + '{}'.format(an)
               for tr, an in zip(list(forma_anual['Total']), anos)]

    fig = go.Figure(data=[go.Bar(
        x=forma_anual.index,
        y=forma_anual['Total'],
        marker_color=color_fill,
        marker_line_color=color_line,
        text=total_m,
        hovertext=my_text,
        hoverinfo='text',
        textposition='outside',
        hoverlabel=dict(font=dict(family=layout['font']['family'])),
    )])

    fig.update_layout(layout_ano_bar)
    fig.update_yaxes(range=[0, max(forma_anual['Total'])*1.15])
    fig.update_xaxes(fixedrange=True, type='category')



    return visi_pf, visi_em, fig


@app.callback([
                Output('header-ano-line', 'children'),
              Output('header-donut', 'children')],
              [Input("mem-year", "children"),
               Input('tabs', 'active_tab'),
               Input('dd-primaria-final', 'value'),
               Input('dd-forma-sector', 'value')
               ],

              )
def header_donut_ano_line(ano_mem, at, prim_fin, form_sect):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    try:
        ano = int(json.loads(ano_mem))
    except (ValueError, TypeError) as e:
        # ano = 2017
        raise PreventUpdate

    if at == "tab-emissoes":
        unidade = unidades_emissoes

        text_1 = "CO2 Emissions"
        text_1_1 = ' per year'
    else:


        text_1 = "Energy Consumption"
        text_1_1 = ' per year'


        if prim_fin == 'Primary':
            unidade = unidades_energia
            text_1 = "Primary " + text_1
        else:
            unidade = 'GWh'

            text_1 = "Final " + text_1

    if form_sect == "Sector":
        text_2 = ', per Sector'
    else:
        text_2 = ', per Energy Form'

    ano_format = ', in ' + str(ano)
    texto_donut = text_1 + text_2 + ano_format
    texto_line = text_1 + text_1_1 + text_2 + " ({})".format(unidade)

    return  texto_line, texto_donut


# Donut Total
@app.callback(
    Output("donut-graph", "figure"),
    [Input("mem-year", "children"),
     Input('dd-forma-sector', 'value'),
     Input('donut-graph', 'clickData'),
     Input('tabs', 'active_tab'),
     Input('dropdown-single', 'value'),
     Input('dd-primaria-final', 'value'),
     ]
)
def update_donut(ano_mem, form_sect, selecao, at, dd_select, prim_fin):

    if not ctx.triggered:
        raise PreventUpdate

    try:
        ano = int(json.loads(ano_mem))

    except (ValueError, TypeError) as e:
        # ano = 2017
        raise PreventUpdate

    if at == "tab-emissoes":
        forma_anual = forma_anual_em
        sector_anual = sector_anual_em
        unidade_1 = ton_k
        unidade_2 = ' ton'

    else:
        unidade_2 = unidades_energia

        if prim_fin == 'Primary':
            unidade_1 = tep_k

            sector_anual =sector_anual_pr
            forma_anual = forma_anual_pr
        else:
            unidade_1 = " GWh"

            sector_anual = sector_anual_fi
            forma_anual = forma_anual_fi



    # seleciona Sector
    if form_sect == 'Sector':

        s_f_lista = sector_list
        color_live = color_5_live_d
        color_dead = color_5_dead_d
        df = sector_anual

        if dd_select:

            if dd_select in sector_list:
                select = dd_select

            else:
                select = 'Transportation'

        elif selecao:
            select_1 = selecao['points'][0]['label']
            if select_1 in sector_list:

                select = select_1

            else:
                select = 'Transportation'

        else:
            select = 'Transportation'

    # seleciona Forma
    else:
        s_f_lista = forma_list

        df = forma_anual.iloc[:, :-1]
        color_live = color_6_live_d
        color_dead = color_6_dead_d

        if dd_select:

            if dd_select in forma_list:
                select = dd_select
            else:
                select = 'Electricity'

        elif selecao:

            select_1 = selecao['points'][0]['label']

            if select_1 in forma_list:
                select = select_1
            else:
                select = 'Electricity'

        else:
            select = 'Electricity'


    # filtra por ano, atribui cores e remove os valores nulos

    df = df.loc[ano, :].to_frame()

    df.sort_index(inplace=True)
    df['labels'] = df.index

    s_f_lista_cut = s_f_lista.copy()
    s_f_lista_cut.remove(select)

    df['color_fill'] = df['labels'].apply(lambda x: color_dead[x])
    df['color_line'] = df['labels'].apply(lambda x: color_live[x])

    for c in s_f_lista_cut:
        df.loc[(df.index == c), 'color_fill'] = color_dead[c]
        df.loc[(df.index == c), 'color_line'] = color_live[c]

    df.loc[(df.index == select), 'color_fill'] = color_live[select]
    # df.loc[(df.index == select), 'color_line'] = "#FFFFFF"

    df = df[(df != 0).all(1)]
    df = df.drop(['labels'], axis=1)
    values = list(df[ano]/1000)
    unidades = [unidade_1]*len(values)
    for a in list(df[ano]/1000):
        if round(a,0) == 0:
            index_pos = values.index(a)
            values[index_pos] = values[index_pos]*1000
            unidades[index_pos] = " " + unidade_2


    percentagens = ((df[ano]/sum(df[ano].tolist()))*100).tolist()

    percentagens = [round(p) if p > 1 else round(p, 2) for p in percentagens]

    if prim_fin == 'Primary':
        my_text_hover = [fs + ': ' + '{:.0f}'.format(sel) + un + '<br>Year: ' + '{}'.format(ano)
                         for fs, sel,un in zip(df.index.tolist(), values, unidades)]
    else:
        my_text_hover = [fs + ': ' + '{:,}'.format(int(round(sel, 0))).replace(',', ' ') + un + '<br>Year: ' + '{}'.format(ano)
                         for fs, sel, un in zip(df.index.tolist(), values, unidades)]

    my_text_write = ['{}'.format(p) + '%'
                     for p in percentagens]

    fig = go.Figure(data=[go.Pie(labels=df.index.tolist(),
                    values=df[ano].tolist(),
                    hole=0.4,
                    marker=dict(colors=df['color_fill'], line=dict(color=df['color_line'], width=2)),
                    text=my_text_write,
                    textinfo='text',
                    hovertext=my_text_hover,
                    hoverinfo='text',
                    hoverlabel=dict(font=dict(family=layout['font']['family'])),
                    opacity=0.8,
                    sort=False)])


    fig.update_layout(layout_donut)
    return fig


@app.callback(
    [Output('dropdown-single', 'options'),
     Output('dropdown-single', 'value')],
    [Input('dd-forma-sector', 'value'),
     Input('donut-graph', 'clickData')],

)
def update_dropdown_items(form_sect, selecao):
    if not ctx.triggered:
        raise PreventUpdate

    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    trigger_value = ctx.triggered[0]['value']

    if form_sect == 'Sector':
        items = [
            {'label': 'Services', 'value': 'Services'},
            {'label': 'Transportation', 'value': 'Transportation'},
            {'label': 'Domestic', 'value': 'Domestic'},
            {'label': 'Industry', 'value': 'Industry'},
            {'label': 'Agriculture', 'value': 'Agriculture'}
        ]

        if selecao is None:
            value = 'Transportation'
        else:
            value = selecao['points'][0]['label']

    else:
        items = [
            {'label': 'Electricity', 'value': 'Electricity'},
            {'label': 'Diesel', 'value': 'Diesel'},
            {'label': 'Natural Gas', 'value': 'Natural Gas'},
            {'label': 'Gasoline', 'value': 'GasolineLPG'},
            {'label': 'LPG', 'value': 'LPG'},
            {'label': 'Other', 'value': 'Other'}
        ]
        if selecao is None:
            value = 'Electricity'
        else:
            value = selecao['points'][0]['label']

    return items, value

@app.callback(
    [Output("value-dd-text", "children"),
     Output("select-dd-text", "children"),
     Output("text-bar", "children"),
     Output("text-bar-div", "style"),
     Output("bar-single-graph", "figure")],
    [Input("mem-year", "children"),
     Input('dd-forma-sector', 'value'),
     Input('donut-graph', 'clickData'),
     Input('dd-primaria-final', 'value'),
     Input('tabs', 'active_tab'),
     Input('dropdown-single', 'value'),

     ]
)
def update_bar_single(ano_mem, form_sect, selecao, prim_fin, at, dd_select):
    if not dash.callback_context.triggered:
        raise PreventUpdate

    try:
        ano = int(json.loads(ano_mem))
    except (ValueError, TypeError) as e:
        # ano = 2017
        raise PreventUpdate


    if at == "tab-emissoes":
        sector_df = sector_df_em
        forma_df = forma_df_em
        unidade_1 = ton_k
        unidade_2 = " ton"

    else:

        # unidade_1 = tep_k
        # unidade_2 = " " + unidades_energia

        if prim_fin == 'Primary':
            unidade_1 = tep_k
            unidade_2 = " " + unidades_energia
            sector_df = sector_df_pr
            forma_df = forma_df_pr

        else:
            unidade_1 = ' GWh'
            unidade_2 = " " + 'MWh'

            sector_df = sector_df_fi
            forma_df = forma_df_fi

    if form_sect == 'Sector':

        select_dd_text = "Select Energy Sector:"

        df = sector_df
        forma_sector = 'Form'

        if dd_select:
            if dd_select in sector_list:
                select = dd_select
            else:
                select = 'Transportation'

        elif selecao:
            pre_select = selecao['points'][0]['label']
            if pre_select in sector_list:
                select = pre_select
            else:
                select = 'Transportation'
        else:

            select = 'Transportation'

        prep_select = {
            'Agriculture': 'in',
            'Services': 'in',
            'Industry': 'in the',
            'Transportation': 'in',
                       }
        if at == "tab-emissoes":
            title_1 = 'CO2 Emissions in the ' + select + ' sector'

            # if select == 'Doméstico':
            #     title_1 = 'Emissões de CO2 no sector ' + select
            # else:
            #     title_1 = 'Emissões de CO2 ' + prep_select[select] + ' ' + select

        else:
            if select == 'Domestic':
                title_1 = select + " Energy consumption"
            else:
                title_1 = "Energy consumption " + prep_select[select] + " " + select

        select_posi = sector_list.index(select)
        bg_color = color_5_dead_d[select]
        title = title_1 + ", per Energy Form, in " + str(ano)

    else:

        select_dd_text = "Select Energy Form:"
        df = forma_df

        # title = "Consumo de Energia por forma de consumo"
        forma_sector = 'Sector'

        if dd_select:
            if dd_select in forma_list:
                select = dd_select
            else:
                select = 'Electricity'


        elif selecao:
            pre_select = selecao['points'][0]['label']
            if pre_select in forma_list:
                select = pre_select
            else:
                select = 'Electricity'
        else:

            select = 'Electricity'

        if at == "tab-emissoes":
            title_1 = "CO2 Emissions in the consumption of"
            if select == "Other":
                title_1 = "CO2 Emissions in the other types of consumption"
        else:
            title_1 = "Consumption of "
            if select == "Other":
                title_1 = "Other types of Consumption"

        if select == "Other":
            title = title_1 + ", per Sector, in " + str(ano)
        else:
            title = title_1 + " " + select + ", per Sector, in " + str(ano)



        bg_color = color_6_dead_d[select]

    df = df.loc[(df['Year'] == ano), [forma_sector, select, 'color_fill', 'color_line']]


    df = df[(df != 0).all(1)]
    df = df.sort_values(select)
    df['percent'] = df[select]/(df[select].sum())*100

    if at == "tab-emissoes":
        values = list(df[select]/1000)
        if int(round(df[select].sum() / 1000, 0)) == 0:
            valor_total = int(round(df[select].sum(), 0))
            unidade_vt = unidade_2

        else:
            valor_total = int(round(df[select].sum() / 1000, 0))
            unidade_vt = unidade_1

    else:
        values = list(df[select]/1000)
        if int(round(df[select].sum() / 1000, 0)) == 0:
            valor_total = int(round(df[select].sum(), 0))
            unidade_vt = unidade_2

        else:
            valor_total = int(round(df[select].sum() / 1000, 0))
            unidade_vt = unidade_1

    # round(forma_anual_pr['Total'] / 1000000, 1)
    unidades = [unidade_1] * len(values)
    for a in values:
        index_pos = values.index(a)
        if a < 1:
            values[index_pos] = values[index_pos] * 1000
            unidades[index_pos] = unidade_2

    values_round = [int(v) if int(v) != 0 else round(v, 2) for v in values]

    my_text_hover = [fs + '<br>' + str(sel) + un + '<br>' + '{:.2f}'.format(pr)
                     + '%' + '<br>Year: ' + '{}'.format(ano)
                     for fs, sel,un, pr in zip(list(df[forma_sector]), values_round, unidades, list(df['percent']))]

    my_text_show = ['{:.0f}'.format(pr) + '%' for pr in list(df['percent'])]

    fig = go.Figure(data=[go.Bar(
        x=df[select],
        y=df[forma_sector],
        marker_color=df['color_fill'],
        orientation='h',
        opacity=0.8,
        marker_line_color=df['color_line'],
        marker_line_width=1.5,
        text=my_text_show,
        hovertext=my_text_hover,
        hoverinfo='text',
        hoverlabel=dict(font=dict(family=layout['font']['family'])),
        textposition='auto'

    )])
    style = {"textAlign": "center", "backgroundColor": bg_color}

    #layout_bar_single['title'] = dict(text=select, font=dict(size=13), xref='paper', x=0.3)

    fig.update_layout(layout_bar_single)

    value = "                         " + str(valor_total) + unidade_vt

    return value, select_dd_text, title, style, fig


@app.callback(
    Output("ano-line-graph", "figure"),
    [
     Input('dd-forma-sector', 'value'),
     Input('dd-primaria-final', 'value'),
     Input('tabs', 'active_tab')
     ]
)
def update_ano_line(form_sect, prim_fin, at):
    if not dash.callback_context.triggered:
        raise PreventUpdate

    if at == "tab-emissoes":
        sector_anual = sector_anual_em
        forma_anual = forma_anual_em
        unidade = unidades_emissoes
        title_1 = "Anual CO2 Emissions, per "
        unidade_1 = ton_k
        unidade_2 = " ton"

    else:

        title_1 = "Anual {} Energy consumption, per ".format(prim_fin)


        if prim_fin == 'Primary':
            unidade_1 = tep_k
            unidade_2 = " " + unidades_energia
            unidade = unidades_energia
            sector_anual = sector_anual_pr
            forma_anual = forma_anual_pr
            title_2 = prim_fin + " per year, per "

        else:
            unidade_1 = ' GWh'
            unidade_2 = " " + 'GWh'
            unidade = 'MWh'
            sector_anual = sector_anual_fi/1000
            forma_anual = forma_anual_fi/1000

    if form_sect == 'Sector':
        df = sector_anual
        lista_index = list(df.sum().sort_values().index)
        color_line = [color_5_live_d[x] for x in lista_index]
        color_fill = [color_5_dead_d[x] for x in lista_index]
        # my_text = ['Agricultura: ' + '{:.0f}'.format(agr) + '<br>Indústria: ' + '{:.0f}'.format(ind) +
        #            '<br>Transportes: ' + '{:.0f}'.format(tran) + '<br>Serviços: ' + '{:.0f}'.format(serv)
        #            + '<br>Doméstico: ' + '{:.0f}'.format(dom) + '<br>' + '_' * 18 + '<br>' + '<br>TOTAL: ' + '{:.0f}'.format(
        #     agr + ind + tran + serv + dom)
        #            for agr, ind, tran, serv, dom in zip(list(df['Agricultura']), list(df['Indústria']),
        #                                                    list(df['Transportes']), list(df['Serviços']),
        #                                                    list(df['Doméstico']))]
        title_2 = '{0} ({1})'.format(form_sect, unidade)

    else:
        df = forma_anual.iloc[:, :-1]
        lista_index = list(df.sum().sort_values().index)
        color_line = [color_6_live_d[x] for x in lista_index]
        color_fill = [color_6_dead_d[x] for x in lista_index]
        # my_text = ['Diesel: ' + '{:.0f}'.format(ds) + '<br>Electricidade: ' + '{:.0f}'.format(el) +
        #            '<br>Gás Natural: ' + '{:.0f}'.format(gn) + '<br>Gasolina: ' + '{:.0f}'.format(gl)
        #            + '<br>GPL: ' + '{:.0f}'.format(gpl) + '<br>Fuel: ' + '{:.0f}'.format(fu) + '<br>Outros: '
        #            + '{:.0f}'.format(out) + '<br>' + '_' * 18 + '<br>' + '<br>TOTAL: ' + '{:.0f}'.format(
        #     ds + el + gn + gl + gpl + fu + out)
        #            for ds, el, gn, gl, gpl, fu, out in zip(list(df['Electricidade']), list(df['Diesel']),
        #                                                    list(df['Gás Natural']), list(df['Gasolina']),
        #                                                    list(df['GPL']),
        #                                                    list(df['Fuel']), list(df['Outros']))]
        title_2 = '{0} ({1})'.format(form_sect, unidade)


    fig = go.Figure()
    i = 0
    title = title_1 + title_2


    for trace in df.sum().sort_values().index:
        if at == "tab-emissoes":
            values = list(df[trace] / 1000000)
        else:
            values = list(df[trace]/1000)

        unidades = [unidade_1] * len(values)
        if prim_fin == 'Primary':
            for a in values:
                index_pos = values.index(a)
                if a < 1:
                    values[index_pos] = values[index_pos] * 1000
                    unidades[index_pos] = unidade_2

        if prim_fin == 'Final':
            # print(values)
            values = [v*1000 for v in values]
            # for a in values:
                # index_pos = values.index(a)
                # if a < 1:
                #     values[index_pos] = values[index_pos] * 1000
                #     unidades[index_pos] = unidade_2

        my_text = [trace + ': ' + '{:.0f}'.format(tr) + un for tr, un in zip(values, unidades)]
        fig.add_trace(go.Scatter(x=anos, y=df[trace], stackgroup='one', name=trace, fillcolor=color_fill[i],
                                 line_color=color_line[i], hovertext=my_text, hoverinfo="text",
                                 hoverlabel=dict(bgcolor=color_fill[i])))
        i += 1


    # layout_ano_line['title'] = dict(text=title, xref='paper', x=0.5)

    fig.update_layout(layout_ano_line)
    return fig
#
#
# @app.callback(
#     Output("ano-line-dom", "figure"),
#     [
#      Input('dd-forma-sector', 'value'),
#      Input('dd-primaria-final', 'value'),
#      Input('tabs', 'active_tab')
#      ]
# )
# def update_ano_line(form_sect, prim_fin, at):
#     if not dash.callback_context.triggered:
#         raise PreventUpdate
#
#     if at == "tab-emissoes":
#         sector_dom_anual = sector_anual_em['Doméstico']
#         forma_dom_anual = forma_df_em.loc[forma_df_em.Sector == 'Doméstico',:]
#         unidade = unidades_emissoes
#         title_1 = "Emissões de CO2 anuais, por "
#         unidade_1 = ton_M
#         unidade_2 = ton_k
#
#     else:
#
#         title_1 = "Consumo de Energia {} anual, por ".format(prim_fin)
#
#
#         if prim_fin == 'Primária':
#             unidade_1 = tep_k
#             unidade_2 = " " + unidades_energia
#             unidade = unidades_energia
#             sector_dom_anual = sector_anual_pr['Doméstico']
#             forma_dom_anual = forma_df_pr.loc[forma_df_pr.Sector == 'Doméstico',:]
#             title_2 = prim_fin + " anual, por "
#
#         else:
#             unidade_1 = ' GWh'
#             unidade_2 = " " + 'GWh'
#             unidade = 'MWh'
#             sector_dom_anual = sector_anual_fi['Doméstico']/1000
#             forma_dom_anual = forma_df_fi.loc[forma_df_fi.Sector == 'Doméstico',:]/1000
#
#     if form_sect == 'Sector':
#         df = sector_dom_anual
#         color_line = [color_5_live_d[x] for x in lista_index]
#         color_fill = [color_5_dead_d[x] for x in lista_index]
#
#         title_2 = '{0} de Consumo ({1})'.format(form_sect, unidade)
#
#     else:
#         df = forma_dom_anual.iloc[:, :-1]
#         lista_index = list(df.sum().sort_values().index)
#         color_line = [color_6_live_d[x] for x in lista_index]
#         color_fill = [color_6_dead_d[x] for x in lista_index]
#         # my_text = ['Diesel: ' + '{:.0f}'.format(ds) + '<br>Electricidade: ' + '{:.0f}'.format(el) +
#         #            '<br>Gás Natural: ' + '{:.0f}'.format(gn) + '<br>Gasolina: ' + '{:.0f}'.format(gl)
#         #            + '<br>GPL: ' + '{:.0f}'.format(gpl) + '<br>Fuel: ' + '{:.0f}'.format(fu) + '<br>Outros: '
#         #            + '{:.0f}'.format(out) + '<br>' + '_' * 18 + '<br>' + '<br>TOTAL: ' + '{:.0f}'.format(
#         #     ds + el + gn + gl + gpl + fu + out)
#         #            for ds, el, gn, gl, gpl, fu, out in zip(list(df['Electricidade']), list(df['Diesel']),
#         #                                                    list(df['Gás Natural']), list(df['Gasolina']),
#         #                                                    list(df['GPL']),
#         #                                                    list(df['Fuel']), list(df['Outros']))]
#         title_2 = '{0} de Energia ({1})'.format(form_sect, unidade)
#
#
#     fig = go.Figure()
#     i = 0
#
#     title_3 = 'no sector doméstico'
#     title = title_1 + title_2 + title_3
#
#
#     for trace in df.sum().sort_values().index:
#         if at == "tab-emissoes":
#             values = list(df[trace] / 1000000)
#         else:
#             values = list(df[trace]/1000)
#
#         unidades = [unidade_1] * len(values)
#         if prim_fin == 'Primária':
#             for a in values:
#                 index_pos = values.index(a)
#                 if a < 1:
#                     values[index_pos] = values[index_pos] * 1000
#                     unidades[index_pos] = unidade_2
#
#         if prim_fin == 'Final':
#             # print(values)
#             values = [v*1000 for v in values]
#             # for a in values:
#                 # index_pos = values.index(a)
#                 # if a < 1:
#                 #     values[index_pos] = values[index_pos] * 1000
#                 #     unidades[index_pos] = unidade_2
#
#         my_text = [trace + ': ' + '{:.0f}'.format(tr) + un for tr, un in zip(values, unidades)]
#         fig.add_trace(go.Scatter(x=anos, y=df[trace], stackgroup='one', name=trace, fillcolor=color_fill[i],
#                                  line_color=color_line[i], hovertext=my_text, hoverinfo="text",
#                                  hoverlabel=dict(bgcolor=color_fill[i])))
#         i += 1
#
#
#     # layout_ano_line['title'] = dict(text=title, xref='paper', x=0.5)
#
#     fig.update_layout(layout_ano_line)
#     return fig

if __name__ == '__main__':
    app.run_server(debug=False)
    # app.run_server(debug=True, port=5000)
