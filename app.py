import io
import base64
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from models.ScanLine import ScanLine
from models.Impact import Impact

app = dash.Dash(
  __name__,
  meta_tags = [{
    'name': 'viewport', 
    'content': 'width=device-width'
  }]
)
server = app.server

# use daq boolean switch for regression line

# layout
# come back to column number names when writing css
app.layout = html.Div(
  className = 'row twelve columns',
  children = [
    # left sidebar
    html.Div(
      # main instructions
      className = 'four columns instruction',
      children = [
        html.H1(children = 'Impact Visualizer'),
        html.P(
          '''
          - View source code (GitHub) by clicking "SRC"
          - Upload impact files by clicking "Upload Files"
          - Edit the impact metadata through the sidebar
            - Default smoothing range: 100
            - Y-positions are calculated from the filenames
          - Edit individual scanline metadata by selecting that scanline's dropdown 
          - Upload new impact files by clicking "Upload Files" again
          '''
        ),
        # source and upload buttons
        html.Div(
          className = 'mobile-buttons',
          children = [
            # source button
            html.Div(
              className='mobile-button',
              children = [
                dcc.Link(
                  href = 'https://github.com/davidjtoomer/Impact-Visualizer',
                  children = [
                    html.Button(
                      'SOURCE',
                      className = 'src-button',
                      id = 'source-code'
                    )
                  ]
                ),
              ]
            ),
            # upload button
            dcc.Upload(
              id = 'upload-data',
              multiple = True,
              className='mobile-button',
              children = [
                html.Button(
                  'UPLOAD DATA',
                  className = 'upload-button',
                  id = 'upload'
                )
              ]
            )
          ]
        ),
        '''
        # impact metadata
        html.Div(
          className = 'impact-metadata',
          children = [
            # impact graph type
            html.Div(
              children = [
                html.Label('Impact Graph Type'),
                dcc.Dropdown(
                  id = 'impact-display-type',
                  options = [
                    {
                      'label': '3D Surface Plot',
                      'value': '3D Surface Plot'
                    },
                    {
                      'label': '2D Contour Plot',
                      'value': '2D Contour Plot'
                    }
                  ]
                )
              ]
            ),
            # interpolation factor (num of lines placed between lines)
            html.Div(
              children = [
                html.Label('Interpolation Factor'),
                dcc.Input(
                  id = 'interpolation-factor',
                  type = 'number',
                  value = 0,
                  name = 'Interpolaion Factor',
                  min = 0,
                  step = 1
                )
              ]
            )
          ]
        ),
        '''
        # empty: scanline metadata
        html.Div(
          children = [
            html.Div(id = 'scanline-info', children = [])
            # scanline META meta (regression, smooth factor, colors...)
            # individual scanline data (slope, intercept, which form of data)
          ]
        )
      ]
    ),
    # right sidebar
    html.Div(
      className = 'eight columns graphs',
      children = [
        # impact graph
        html.Div(
          id = 'impact-graph-container',
          children = [
            dcc.Graph(
              id = 'impact-graph'
            )
          ]
        ),
        # scanline tabs
        '''
        html.Div(
          children = [
            html.H1('Scanlines'),
            # tabs with scanlines
            html.Div(
              children = []
            )
          ]
        )
        '''
      ]
    )
  ]
)
 
# callbacks
@app.callback( # make graphs visible
  Output('impact-graph-container', 'children'),
  [Input('upload-data', 'contents'),
  Input('upload-data', 'filename')]
)
def load_data(contents, filenames):
  if contents:
    datafiles = []
    for content in contents:
      content_type, content_string = content.split(',')
      decoded = base64.b64decode(content_string)
      datafiles.append(pd.read_excel(io.BytesIO(decoded), sheet_name = 'DATA', header = None, nrows = 6000, usecols = 'E:F', keep_default_na = False))

    impact = Impact(datafiles, filenames)
    figure = go.Figure(
      data = [
        go.Surface(
          x = impact.xgrid, 
          y = impact.ygrid,
          z = impact.zgrid
        )
      ]
    )
    figure.update_layout(scene_aspectmode='data')
    return html.Div(
      children = [
        dcc.Graph(
          id = 'impact-graph',
          figure = figure,
        )
      ]
    )

# run the server
if __name__ == '__main__':
  app.run_server(debug=True)