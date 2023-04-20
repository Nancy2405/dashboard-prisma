import os

import dash
import dash_core_components as dcc
import dash_html_components as html

# Configuración de la aplicación Dash
app = dash.Dash(__name__)
server = app.server
app.title = 'Mi Panel de Control Dash'

# Define el layout de la aplicación
app.layout = html.Div([
    html.H1('Mi Panel de Control'),
    dcc.Graph(
        id='ejemplo',
        figure={
            'data': [{
                'x': [1, 2, 3],
                'y': [4, 1, 2],
                'type': 'bar',
                'name': 'Ejemplo'
            }],
            'layout': {
                'title': 'Ejemplo de Gráfico de Barras'
            }
        }
    )
])

if __name__ == '__main__':
    # Puerto asignado por Heroku
    puerto = int(os.environ.get('PORT', 8050))
    # Ejecuta la aplicación
    app.run(host='0.0.0.0', port=puerto)
