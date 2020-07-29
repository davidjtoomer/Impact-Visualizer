import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import utils.preprocessing as preprocessing
import utils.figures as figures
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

# layout
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
          - View source code (GitHub) by clicking "SOURCE"
          - Upload impact files by clicking "UPLOAD DATA"
          - Upload new impact files by clicking "UPLOAD DATA" again
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
        # empty: scanline metadata
        html.Div(id = 'scanline-toolbar')
      ]
    ),
    # right sidebar
    html.Div(
      className = 'eight columns graphs',
      children = [
        # impact graph
        html.Div(id = 'impact-graph-container'),
        # scanline tabs
        html.Div(id = 'scanline-graph-container')
      ]
    )
  ]
)
 
# callbacks
@app.callback( # make graphs visible upon file submission
  Output('scanline-graph-container', 'children'),
  [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
  ]
)
def load_data(contents, filenames):
  if contents:
    datafiles = preprocessing.parse_impact(contents)
    impact = Impact(datafiles, filenames)
    impact_figure = figures.impact_graph(impact)
    return impact_figure

# run the server
if __name__ == '__main__':
  app.run_server(debug=True)