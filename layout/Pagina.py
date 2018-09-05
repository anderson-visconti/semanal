# coding: utf-8
#from semanal.layout.Layout import *
#from app.config import Config
from layout.Layout import *
import plotly.graph_objs as go
import base64

from config import Config
from datetime import datetime
from dateutil.relativedelta import relativedelta
import openpyxl as pyxl
import numpy as np
import pandas as pd

class Pagina(object):
    def __init__(self):
        return None

class P1(Pagina):
    def cria(self):
        # Secao Fixa

        print_button = PrintButton().cria()
        logo = Logo().cria()
        header = Header().cria()
        menu = Menu().cria()

        pag = html.Div([
            html.Div([
                print_button,
                logo,
                header,
                # menu,
                Meteo().cria(),
                html.Div([
                    html.Div([Hidro().cria()], className='six columns'),
                    html.Div([Arm().cria()], className='six columns')
                ],
                    className='row'
                ),

            ], className='page'),

        ],
            className='page',
            id='pag_1'
        )
        return pag

class P2(Pagina):
    def cria(self):
        logo = Logo().cria()
        pag = html.Div([
            html.Div([
                logo,
                Preco().cria(),
                Forward().cria()

            ],
                className='page',

            ),

        ],
            className='page',
            id='pag_2'
        )
        return pag

class P3(Pagina):
    def cria(self):
        logo = Logo().cria()
        pag = html.Div([
            logo,
            Regulatorio().cria(),
        ],
            className='page',
            id='pag_3'
        )
        return pag


class Secao(object):
    def __init__(self):
        self.config = Config()
        return None

class Meteo(Secao):

    def cria(self):
        # Leitura dos textos
        texto = list()
        texto.append(html.P([]))
        [texto.append(html.P(i)) for i in self.config.config_meteo['texto']]

        sec = html.Div([
            # Titulo da secao
            html.Br([]),

            html.Div([
                html.H6('Meteorologia', className='gs-header gs-text-header padded')
            ],
                className='twelve columns'
            ),

            # Area de textos e figuras
            html.Div([
                # Primeira coluna
                html.Div(texto, className='six columns'),

                # Segunda Coluna - Imagens
                html.Div([

                    # col 1
                    html.Div([
                        # Primeiro grafico
                        html.Br([]),

                        html.Img(
                            src=self.config.config_meteo['path_chuva_acum'].format(
                                self.config.meses[datetime.today().month],
                                datetime.today()
                            ),
                            height='100%',
                            width='100%'
                        ),
                    ],
                        className='six columns'
                    ),

                    # col 2
                    html.Div([
                        html.Br([]),

                        # Primeiro grafico
                        html.Img(
                            src=self.config.config_meteo['path_chuva_anom'].format(
                                self.config.meses[datetime.today().month],
                                datetime.today()
                            ),
                            height='100%',
                            width='100%'
                        ),
                    ],
                        className='six columns'
                    ),

                    # Fonte
                    html.Div([
                        html.P(
                            'Fonte: INPE/CPTEC',
                            className='eleven columns right-aligned',
                            style={'text-align': 'right'}
                        )
                    ],
                        className='eleven columns right-aligned',
                        style={'text-align': 'right'}
                    )
                ],
                    className='six columns'
                )

            ],
                className='twelve columns'
            )

        ],
            className='row',
        )
        return sec

class Hidro(Secao):

    def cria(self):

        texto = list()
        texto.append(html.Br([]))
        [texto.append(html.P(i)) for i in self.config.config_hidro['texto']]

        sec = html.Div([
            # Titulo da secao
            html.H6('Hidrologia', className='gs-header gs-text-header padded'),

            html.Div(texto, className='row'),

            html.Br([]),

            dcc.Graph(
                id='hidrologia',
                #className='row',
                figure=self.make_chart(),
                config=dict(displayModeBar=False)
            )

            ],
                className='row'
            )
        return sec

    def make_chart(self):

        df_dados = self.get_data()

        # Criação dos traços para o gráfico
        traces = []

        for subsistema in df_dados['cod_subsistema'].unique():
            text = '''{:} - {:%d/%m/%Y}<Br> {:5,d} MWm | {:3.0f}% MLT'''

            annotations = list()
            [
                annotations.append(text.format(
                    l['cod_subsistema'], l['data'], l['ena_b'], l['ena_p'] * 100)
                ) for k, l in
                df_dados[df_dados['cod_subsistema'] == subsistema].iterrows()
            ]

            trace = go.Scatter(
                x=df_dados['data'],
                y=df_dados.loc[df_dados['cod_subsistema'] == subsistema, 'ena_p'] * 100,
                mode='lines',
                name=subsistema,
                line=dict(
                    shape='hv',
                    #color='rgb(215, 48, 39)'
                ),
                text=annotations,
                textfont=dict(
                    family='sans serif',
                    size=8,
                ),
                hoverinfo='text',
                hoverlabel=dict(
                    font=dict(
                        size=10
                    )
                )
            )

            traces.append(trace)

        # Definição do layout do grafico
        layout = go.Layout(
            title='Evolução da Hidrologia',
            autosize=True,
            margin={'r': 0, 't': 40, 'l': 40, 'b': 30},
            height=270,
            xaxis=dict(
                dtick=86400000.0 * 5,
                tickformat='%d/%m/%y',
                tickfont=dict(
                    family='sans serif',
                    size=8
                ),
                showgrid=True,
                showline=True
            ),
            yaxis=dict(
                title='Energia Natural Afluente - ENA [%MLT]',
                titlefont=dict(
                    size=8
                ),
                dtick=10,
                tickformat='2d',
                #exponentformat='e',
                tickfont=dict(
                    family='sans serif',
                    size=8
                ),
                showgrid=True,
                showline=True,
            ),

            legend=dict(
                font=dict(
                    family='sans-serif',
                    size=6,
                )
            ),

        )

        # Definição da figura
        fig = go.Figure(data=traces, layout=layout)

        return fig

    def get_data(self):

        # Criação dos dados a partir do arquivo
        dados = pd.read_excel(io=self.config.config_hidro['dados'])
        df_dados = pd.DataFrame()

        for i, dados in dados.iterrows():
            dat_index = pd.date_range(start=dados['dat_inicial'], end=dados['dat_final'], freq='D')
            df_dados_aux = pd.DataFrame.from_dict(
                data=dict(
                    data=pd.date_range(start=dados['dat_inicial'], end=dados['dat_final']),
                    cod_subsistema=dat_index.shape[0] * [dados['cod_subsistema']],
                    ena_b=dat_index.shape[0] * [dados['ena_b']],
                    ena_p=dat_index.shape[0] * [dados['ena_p']],
                ),
            )

            df_dados = pd.concat([df_dados, df_dados_aux])

        df_dados['ena_p'] = df_dados['ena_p'] / 100

        return df_dados

class Arm(Secao):
    def cria(self):
        self.get_rdh()
        self.get_data()

        texto = list()
        texto.append(html.Br([]))
        [texto.append(html.P(i)) for i in self.config.config_arm['texto']]

        sec = html.Div([
            # Titulo da secao
            html.H6('Armazenamento', className='gs-header gs-text-header padded'),

            html.Div(texto, className='row'),

            html.Br([]),

            dcc.Graph(
                id='arm',
                className='row',
                figure=self.make_chart(),
                config=dict(displayModeBar=False)
            )

            ],
                className='row'
            )
        return sec

    def make_chart(self):
        df_dados = self.get_data()
        traces = list()

        for subsistema in df_dados['cod_subsistema'].unique():
            text = '''{:} - {:%d/%m/%Y}<Br>{:3.1f}% EARmax'''
            annotations = list()

            [
                annotations.append(text.format(l['cod_subsistema'], l['dat_data'], l['arm_p'])) for k, l in
                df_dados[df_dados['cod_subsistema'] == subsistema].iterrows()
            ]


            trace = go.Scatter(
                x=df_dados.loc[df_dados['cod_subsistema'] == subsistema, 'dat_data'],
                y=df_dados.loc[df_dados['cod_subsistema'] == subsistema, 'arm_p'],
                mode='lines',
                name=subsistema,
                text=annotations,
                textfont=dict(
                    family='sans serif',
                    size=8,
                ),
                hoverinfo='text',
                hoverlabel=dict(
                    font=dict(
                        size=10
                    )
                )
            )

            traces.append(trace)


        layout = go.Layout(
            title='Evolução Armazenamentos',
            autosize=True,
            margin={'r': 0, 't': 40, 'l': 40, 'b': 30},
            height=270,
            xaxis=dict(
                dtick=86400000.0 * 10,
                tickformat='%d/%m/%y',
                tickfont=dict(
                    family='sans serif',
                    size=8
                )
            ),
            yaxis=dict(
                title='Energia Armazenada - EAR [%EARmax]',
                titlefont=dict(
                    size=8
                ),
                dtick=2.5,
                tickformat='3.1f%',
                exponentformat='e',
                tickfont=dict(
                    family='sans serif',
                    size=8
                )
            ),

            legend=dict(
                font=dict(
                    family='sans-serif',
                    size=6,
                )
            ),

        )

        fig = go.Figure(data=traces, layout=layout)
        return fig

    def get_data(self):
        df_dados = pd.read_excel(self.config.config_arm['dados'])

        # paga os últimos três meses em dias
        #df_dados = df_dados[df_dados['dat_data'] >= (datetime.today() + relativedelta(months=-2))]

        return df_dados

    def get_rdh(self, d_dias=-90):
        hj = datetime(year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)
        dados = dict(
            cod_subsistema=list(),
            dat_data=list(),
            arm_p=list()
        )

        for data in pd.date_range(start=hj + relativedelta(days=d_dias), end=hj + relativedelta(days=-1), freq='D'):

            try:
                # abre RDH
                wb = pyxl.load_workbook(
                    filename=os.path.join(
                        self.config.config_arm['rdh'],
                        '{:%Y}'.format(data),
                        'RDH{:%d}{:}.xlsx'.format(data, self.config.meses[data.month])
                    ),
                    read_only=True,
                )

                # Pega
                for i in range(1, 5):
                    dados['cod_subsistema'].append(self.config.subsistemas[i])
                    dados['dat_data'].append(data),
                    dados['arm_p'].append(wb['Hidroenergética-Subsistemas'].cell(row=8 * i - 1, column=12).value)


            except:
                for i in range(1, 5):
                    dados['cod_subsistema'].append(self.config.subsistemas[i])
                    dados['dat_data'].append(data),
                    dados['arm_p'].append(np.nan)


            wb.close()

        # cria arquivo .xslx
        df = pd.DataFrame.from_dict(dados, orient='columns')
        df.to_excel(self.config.config_arm['dados'], index=False)
        return

class Preco(Secao):
    def cria(self):

        texto = list()
        texto.append(html.H6('Análise Preço', className='gs-header gs-text-header padded'))
        texto.append(html.Br([]))
        [texto.append(html.P(i)) for i in self.config.config_preco['texto']]

        sec = html.Div([
            html.Div(texto, className='row'),

            html.Div([

                html.Div([
                    html.Img(
                        src='data:image/png;base64,{}'.format(
                            base64.b64encode(open(self.config.config_preco['path_dispersao'], 'rb').read()).decode()
                        ),
                        height='250',
                        width='80%',
                    )
                ],
                    className='six columns'
                ),

                html.Div([
                    html.Img(
                        src='data:image/png;base64,{}'.format(
                            base64.b64encode(open(self.config.config_preco['path_histograma'], 'rb').read()).decode()
                        ),
                        height='250',
                        width='80%',
                    )
                ],
                    className='six columns'
                )

            ],
                className='twelve columns'
            )

            ], className='row'
        )

        return sec

class Forward(Secao):
    def cria(self):

        texto = list()
        [texto.append(html.P(i)) for i in self.config.config_forward['texto']]

        sec = html.Div([
            html.H6('Curva Forward', className='gs-header gs-text-header padded'),
            html.Br([]),
            html.Div(texto, className='twelve columns'),

            html.Div([
                dcc.Graph(
                    id='forward',
                    className='center',
                    figure=self.make_chart(),
                    config=dict(displayModeBar=False),
                    style={'width': '85%'}
                )
            ],
                className='twelve columns'
            ),

            ], className='twelve columns'
        )

        return sec

    def get_data(self):

        df_dados = pd.DataFrame(pd.read_excel(io=self.config.config_forward['dados']))
        df_dados.sort_values(by=['dat_medicao', 'dat_data'], ascending=True, inplace=True)

        semanas = df_dados['dat_medicao'].unique()[-2:]
        week_2 = semanas[0]

        df_dados = df_dados.loc[df_dados['dat_medicao'] >= week_2, :]

        return df_dados

    def make_chart(self):
        df = pd.DataFrame(self.get_data())

        # Criação dos tracos
        traces = list()
        for semana in df['dat_medicao'].unique():
            txt_semana = pd.to_datetime(str(semana)).strftime('%d-%m-%Y')
            txt = 'Medição: {:}<Br>{:%m/%Y} - {:3.2f} R$/MWh'

            # annotations
            annotations = list()
            [annotations.append(
                txt.format(
                    txt_semana, l['dat_data'],
                    l['preco'])
            ) for i, l in df.loc[df['dat_medicao'] == semana].iterrows()]

            trace = go.Scatter(
                x=df.loc[df['dat_medicao'] == semana, 'dat_data'],
                y=df.loc[df['dat_medicao'] == semana, 'preco'],
                yaxis='y1',
                mode='lines+markers',
                name='SE CONV - {:}'.format(txt_semana),
                text=annotations,
                textfont=dict(
                    family='sans serif',
                    size=8,
                ),
                hoverinfo='text',
                hoverlabel=dict(
                    font=dict(
                        size=10
                    )
                )
            )
            traces.append(trace)

        # Criação do traço de diferenças
        df_diferencas = df.pivot(index='dat_data', columns='dat_medicao', values='preco')
        df_diferencas['diff'] = df_diferencas.iloc[:, 1] - df_diferencas.iloc[:, 0]

        trace_diff = go.Bar(
            x=df_diferencas.index,
            y=df_diferencas['diff'],
            text=df_diferencas['diff'],
            yaxis='y2',
            name='Variação',
            textfont=dict(
                family='sans serif',
                size=8,
            ),
            hoverinfo='text',
            hoverlabel=dict(
                font=dict(
                    size=10
                )
            )
        )

        # Criação do layout
        layout = go.Layout(
            title='Curva Forward',
            autosize=True,
            margin={'r': 0, 't': 40, 'l': 40, 'b': 30},
            height=270,
            xaxis=dict(
                showgrid=True,
                showticklabels=True,
                dtick='M1',
                tickformat='%m/%Y',
                tickfont=dict(
                    family='sans serif',
                    size=8
                ),
            ),

            yaxis1=dict(
                title='SE/CO CONV [R$/MWh]',
                titlefont=dict(
                    size=8
                ),
                showgrid=True,
                tickformat='3.2f',
                dtick=50,
                tickfont=dict(
                    family='sans serif',
                    size=8
                ),
                domain=[0.30, 1.0]
            ),

            yaxis2=dict(
                title='Variação',
                titlefont=dict(
                    size=8
                ),
                showgrid=True,
                tickformat='3.2f',
                tickfont=dict(
                    family='sans serif',
                    size=8
                ),
                domain=[0.0, 0.20]
            ),

            legend=dict(
                x=0.80,
                y=1.00,
                font=dict(
                    family='sans-serif',
                    size=10,
                )
            ),

        )

        # Criação da figura
        fig = go.Figure(data=[traces[0], traces[1], trace_diff], layout=layout)
        return fig

class Regulatorio(Secao):
    def cria(self):
        df = pd.read_excel(io=self.config.config_reg['path_reg'])
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                if i == 0:
                    html_row.append(html.Td([row[i]]))

                else:
                    html_row.append(
                        html.Td([
                            html.I([

                            ],
                                className=self.config.config_reg['classes'][row[i]]
                            )
                        ],
                            className='table'
                        )
                    )

            table.append(html.Tr(html_row))

        texto = list()
        texto.append(html.Br([]))
        [texto.append(html.P(i)) for i in self.config.config_reg['texto']]

        sec = html.Div([
            html.H6(["Regulatório"], className="gs-header gs-table-header padded"),

            html.Div([

                html.Div(texto, className='six columns'),

                html.Div([
                    html.Br([]),
                    html.Table(
                        table,
                        className="table"
                    )
                ],
                    className='six columns'
                ),

            ],
                className='row'
            ),

            ],

            className='row'
        )

        return sec

