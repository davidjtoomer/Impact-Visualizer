import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, ALL, MATCH
import utils.preprocessing as preprocessing
import utils.callbacks as callbacks
from models.ScanLine import ScanLine
from models.Impact import Impact

app = dash.Dash(
  __name__,
  meta_tags = [{
    'name': 'viewport', 
    'content': 'width=device-width'
  }],
  suppress_callback_exceptions = True
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
        html.H1('Impact Visualizer'),
        html.P(
          '''
          - View source code (GitHub) by clicking "SOURCE"
          - Upload impact files by clicking "UPLOAD DATA"
          - Upload new impact files by clicking "UPLOAD DATA" again
          - If your files are not named by their y-position, you must also include the MATLAB script (plot.m or Surface_Plot.m) containing the ystep variable.
          ''',
          className = 'instruction-text'
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
                  target = '_blank',
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
              className = 'mobile-button',
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
        # empty: impact toolbar
        html.Div(
          id = 'impact-toolbar',
          className = 'impact-toolbar'
        ),
        # empty: scanline toolbar
        html.Div(
          id = 'scanline-toolbar',
          className = 'scanline-toolbar'
        )
      ]
    ),
    # right sidebar
    html.Div(
      className = 'eight columns graphs',
      children = [
        # impact graph
        html.Div(id = 'impact-graph-container'),
        # scanline graphs
        html.Div(id = 'scanline-graph-container')
      ]
    )
  ]
)

@app.callback(
  [
    Output('impact-graph-container', 'children'),
    Output('impact-toolbar', 'children'),
    Output('scanline-graph-container', 'children'),
    Output('scanline-toolbar', 'children')
  ],
  [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
  ]
)
def load_data(contents, filenames):
  if contents:
    matlab_contents, _ = preprocessing.extract_matlab(contents, filenames)
    ystep = preprocessing.extract_ystep(matlab_contents)
    datafiles = preprocessing.parse_impact(contents)
    global impact 
    global figure
    impact = Impact(datafiles, filenames, ystep)
    figure, impact_figure = callbacks.impact_figure(impact)
    impact_toolbar = callbacks.impact_toolbar(impact)
    scanline_toolbar = callbacks.scanline_toolbar(impact)

    scanline_graphs = [
      html.Div(
        id = 'scanline-graph-all-display',
        className = 'scanline-graph-all-display'
      )
    ]
    for i, _ in enumerate(impact.scanlines):
      scanline_graphs.append(html.Div(
        id = dict(
          type = 'scanline-graph-display',
          index = i
        )
      ))
    
    return impact_figure, impact_toolbar, scanline_graphs, scanline_toolbar 
  return None, None, None, None

@app.callback(
  Output('scanline-graph-all-display', 'children'),
  [
    Input('scanline-view-all-button', 'value'),
  ]
)
def display_all_scanlines(value):
  if value:
    if value == 'hide': return callbacks.all_scanline_figure(impact, visible = 'legendonly')
    return callbacks.all_scanline_figure(impact)
  return None

@app.callback(
  [
    Output(
      dict(
        type = 'scanline-graph-display',
        index = MATCH
      ), 
      'children'
    ),
    Output(
      dict(
        type = 'scanline-view-button',
        index = MATCH
      ), 
      'children'
    ),
    Output(
      dict(
        type = 'scanline-regression-info',
        index = MATCH
      ),
      'style'
    ),
    Output(
      dict(
        type = 'scanline-local-extrema',
        index = MATCH
      ),
      'style'
    )
  ],
  [
    Input(
      dict(
        type = 'scanline-view-button',
        index = MATCH
      ), 
      'n_clicks'
    )
  ],
  [
    State(
      dict(
        type = 'scanline-view-button',
        index = MATCH
      ), 
      'id'
    ),
    State(
      dict(
        type = 'scanline-view-button',
        index = MATCH
      ), 
      'children'
    )
  ]
)
def display_scanline(n_clicks, scanline_id, curr_text):
  if curr_text:
    if n_clicks and n_clicks % 2:
      return callbacks.scanline_figure(impact, scanline_id['index']), curr_text.replace('View', 'Hide'), {'display': 'block'}, {'display': 'block'}
    return None, curr_text.replace('Hide', 'View'), {'display': 'none'}, {'display': 'none'}
  return None, None, None

@app.callback(
  Output('scanline-graph-all', 'figure'),
  [
    Input(
      dict(
        type = 'scanline-regression-slope',
        index = ALL
      ),
      'value'
    ),
    Input(
      dict(
        type = 'scanline-regression-intercept',
        index = ALL
      ),
      'value'
    )
  ],
  [
    State('scanline-graph-all', 'figure')
  ]
)
def update_global_scanline_figure(slopes, intercepts, fig):
  if fig and dash.callback_context.triggered:
    changed = dash.callback_context.triggered[0]['prop_id']
    index = int(changed[changed.find(':') + 1 : changed.find(',')])
    if slopes[index] and intercepts[index]:
      scanline = impact.scanlines[index]
      scanline.update_regression(slopes[index], intercepts[index])
      new_data = scanline.data_corrected_smooth[:, 1]
      fig['data'][index]['y'] = new_data
  return fig

@app.callback(
  Output(
    dict(
      type = 'scanline-graph',
      index = MATCH
    ),
    'figure'
  ),
  [
    Input(
      dict(
        type = 'scanline-regression-slope',
        index = MATCH
      ),
      'value'
    ),
    Input(
      dict(
        type = 'scanline-regression-intercept',
        index = MATCH
      ),
      'value'
    )
  ],
  [
    State(
      dict(
        type = 'scanline-graph',
        index = MATCH
      ),
      'figure'
    ),
    State(
      dict(
        type = 'scanline-graph',
        index = MATCH
      ),
      'id'
    )
  ]
)
def update_individual_scanline_regression(slope, intercept, fig, scanline_id):
  if fig and dash.callback_context.triggered and slope and intercept:
    scanline = impact.scanlines[scanline_id['index']]
    scanline.update_regression(slope, intercept)
    fig['data'][1]['y'] = scanline.data_corrected[:, 1]
    fig['data'][2]['y'] = scanline.data_corrected_smooth[:, 1]
  return fig

@app.callback(
  [
    Output(
      dict(
        type = 'scanline-local-minima',
        index = MATCH
      ),
      'children'
    ),
    Output(
      dict(
        type = 'scanline-local-maxima',
        index = MATCH
      ),
      'children'
    )
  ],
  [
    Input(
      dict(
        type = 'scanline-regression-slope',
        index = MATCH
      ),
      'value'
    ),
    Input(
      dict(
        type = 'scanline-regression-intercept',
        index = MATCH
      ),
      'value'
    )
  ],
  [
    State(
      dict(
        type = 'scanline-regression-slope',
        index = MATCH
      ),
      'id'
    ),
    State(
      dict(
        type = 'scanline-local-minima',
        index = MATCH
      ),
      'children'
    ),
    State(
      dict(
        type = 'scanline-local-maxima',
        index = MATCH
      ),
      'children'
    )
  ]
)
def update_local_extrema(slope, intercept, scanline_id, minima, maxima):
  if dash.callback_context.triggered and slope and intercept:
    scanline = impact.scanlines[scanline_id['index']]
    scanline.update_regression(slope, intercept)
    minima = [html.P(f'({minima[0]:.5f}, {minima[1]:.5f})') for minima in scanline.minima[0]]
    maxima = [html.P(f'({maxima[0]:.5f}, {maxima[1]:.5f})') for maxima in scanline.maxima[0]]
  return minima, maxima


@app.callback(
  Output('impact-graph', 'figure'),
  [
    Input('num-contours-slider', 'value'),
    Input('colorscale-dropdown', 'value'),
    Input('projection-dropdown', 'value'),
    Input('view-dropdown', 'value'),
    Input('x-range-slider', 'value'),
    Input('y-range-slider', 'value'),
    Input('z-scale-input', 'value'),
    Input(
      dict(
        type = 'scanline-regression-slope',
        index = ALL
      ),
      'value'
    ),
    Input(
      dict(
        type = 'scanline-regression-intercept',
        index = ALL
      ),
      'value'
    )
  ]
)
def update_impact_graph(num_contours, colorscale, projection, view, x_range, y_range, z_scale, slopes, intercepts):
  if dash.callback_context.triggered and slopes and intercepts:
    for i in range(len(impact.scanlines)):
      scanline = impact.scanlines[i]
      scanline.update_regression(slopes[i], intercepts[i])
      figure.data[0].z[i] = scanline.data_corrected_smooth[:, 1]
  return callbacks.update_impact(impact, figure, num_contours, colorscale, projection, view, x_range, y_range, z_scale)

@app.callback(
  Output('display-num-contours', 'children'),
  [
    Input('num-contours-slider', 'value')
  ]
)
def display_num_contours(num_contours):
  return [
    html.P(f'{num_contours}')
  ]

@app.callback(
  [
    Output('left-x-range-slider', 'children'),
    Output('right-x-range-slider', 'children')
  ],
  [
    Input('x-range-slider', 'value')
  ]
)
def display_xrange(value):
  return [
    html.P(f'{value[0]:.3f}')
  ], [
    html.P(f'{value[1]:.3f}')
  ]

@app.callback(
  [
    Output('left-y-range-slider', 'children'),
    Output('right-y-range-slider', 'children')
  ],
  [
    Input('y-range-slider', 'value')
  ]
)
def display_yrange(value):
  return [
    html.P(f'{value[0]:.3f}')
  ], [
    html.P(f'{value[1]:.3f}')
  ]

# run the server
if __name__ == '__main__':
  app.run_server(debug = True)