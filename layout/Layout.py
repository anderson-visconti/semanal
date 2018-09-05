import dash_core_components as dcc
import dash_html_components as html
import os
import base64

from datetime import datetime

class Layout(object):

    def create(self):
        return None

class Header(Layout):
    def cria(self):
        header = html.Div([
            html.H1('Relatório Semanal', className='H1')
        ],
            className="row gs-header gs-text-header",
            style={'text-align': 'center'}
        )

        return header

class Footer(Layout):
    def cria(self):
        footer = html.Div([
            html.P(
                '''
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. In lacus est, finibus sed fringilla id, vestibulum non lorem. Nullam porta hendrerit vestibulum. Mauris metus turpis, consectetur sed erat vel, iaculis iaculis metus. Sed eget mattis mi. Donec rutrum lectus sed metus gravida tempor. Cras eu dui id nibh molestie fermentum. Donec lobortis fermentum nisl hendrerit porta. Phasellus quam ex, vestibulum ac ipsum nec, mattis tempor nisi. Nulla est ligula, rhoncus a magna eget, rhoncus vulputate nisl. Ut commodo finibus lorem scelerisque condimentum.

                ''',
                #className='gs-footer gs-table-footer'
            )
        ],
            className="gs-footer gs-table-footer",
        )

        return footer

class Logo(Layout):
    def cria(self):
        image_filename = os.path.join(os.path.dirname(__file__), 'images', 'logo_ideal_H_RGB.jpg')
        encoded_image = base64.b64encode(open(image_filename, 'rb').read())
        logo = html.Div([

            html.Div([
                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image.decode()),
                    height='25%',
                    width='25%'
                ),

            ], className='ten columns padded'),

            html.Div([
                html.P(
                    'Data: {:%d-%m-%Y}'.format(datetime.today()),
                style={'color': 'red', 'text-weight': 'bolder'}
        )
            ], className='two columns page-view'),

        ],
            className="row gs-header"
        )

        return logo

class Menu(Layout):

    def cria(self):
        menu = html.Div([
            dcc.Link('Condição Atual', href='/atual', className="tab first", style={'width': '25%'}),

            dcc.Link('Análise Preço', href='/preco', className="tab", style={'width': '25%'}),

            dcc.Link('Curva Forward', href='/forward', className="tab", style={'width': '25%'}),

            dcc.Link('Regulátorio', href='/regulatorio', className="tab", style={'width': '25%'}),

        ],
            className='row'
        )

        return menu

class PrintButton(Layout):
    def cria(self):
        print_button = html.Button(
            ['Print PDF'],
            className="button no-print print",
            style={'position': "absolute", 'top': '-40', 'right': '0'},
            id='print_button'
        )
        return print_button

class Tabela(Layout):
    def make_dash_table(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table