# coding: utf-8
import dash
from semanal.layout.Pagina import *
from semanal.config import Config

# Dashboard
app = dash.Dash('semanal')
server = app.server

# Load informacoes
config = Config

# Criacao layouts fixos
header = Header().cria()
logo = Logo().cria()
menu = Menu().cria()

# css
external_css = ['https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.0/normalize.css',
                'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css',
                '//fonts.googleapis.com/css?family=Raleway:400,300,600',
                'https://use.fontawesome.com/releases/v5.2.0/css/all.css']
[app.css.append_css({"external_url": css}) for css in external_css]

# js
external_js = [
    "https://code.jquery.com/jquery-3.2.1.min.js",
    "https://codepen.io/bcd/pen/YaXojL.js"
]
[app.scripts.append_script({"external_url": js}) for js in external_js]

# Describe the layout, or the UI, of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', className='page-content')
])

# Update page
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.Div([
            P1().cria(),
            P2().cria(),
            P3().cria(),
        ],
            className='page'
        )


if __name__ == '__main__':
    app.run_server(debug=True)
