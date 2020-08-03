import plotly.graph_objects as go
from plotly import subplots
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq

def impact_figure(impact):
  figure = go.Figure()

  figure.add_trace(
    go.Surface(
      x = impact.X,
      y = impact.Y,
      z = impact.Z,
      colorscale = 'Jet',
    )
  )

  figure.update_layout(
    scene_camera = dict(
      projection = dict(
        type = 'orthographic'
      )
    )
  )

  figure.update_scenes(
    aspectmode = 'manual',
    aspectratio = dict(
      x = impact.xrange / impact.yrange,
      y = 1,
      z = 1
    )
  )

  figure.update_layout(
    updatemenus = [
      # surface
      dict(
        buttons = list(
          [
            dict(
              args = ['type', 'surface'],
              label = '3D Surface',
              method = 'restyle'
            ),
            dict(
              args = ['type', 'contour'],
              label = 'Contour',
              method = 'restyle'
            )
          ]
        ),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        y = 1
      ),
      # contours
      dict(
        buttons = list(
          [
            dict(
              args = ['contours', dict(
                z = dict(
                  show = False
                )
              )],
              label = 'No Contours',
              method = 'restyle'
            ),
            *[
              dict(
                args = ['contours', dict(
                  z = dict(
                    show = True,
                    start = impact.zmin,
                    end = impact.zmax,
                    size = (impact.zmax - impact.zmin) / (i - 1)
                  )
                )],
                label = f'{i} Contour Lines',
                method = 'restyle'
              ) for i in range(5, 31, 5)
            ]
          ]
        ),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        y = 0.8
      ),
      # colorscale
      dict(
        buttons = list(
          [
            dict(
              args = ['colorscale', 'Jet'],
              label = 'Jet',
              method = 'restyle'
            ),
            dict(
              args = ['colorscale', 'Viridis'],
              label = 'Viridis',
              method = 'restyle'
            ),
            dict(
              args = ['colorscale', 'RdBu'],
              label = 'Red-Blue',
              method = 'restyle'
            )
          ]
        ),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        y = 0.6
      ),
      # projection
      dict(
        buttons = list(
          [
            dict(
              args = ['scene.camera.projection.type', 'orthographic'],
              label = 'Orthographic Projection',
              method = 'relayout'
            ),
            dict(
              args = ['scene.camera.projection.type', 'perspective'],
              label = 'Perspective Projection',
              method = 'relayout'
            )
          ]
        ),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        y = 0.4
      ),
      # view
      dict(
        buttons = list(
          [
            dict(
              args = [
                {
                  'scene.camera.eye': dict(
                    x = 1.25, 
                    y = 1.25, 
                    z = 1.25
                  ),
                  'scene.camera.up': dict(
                    x = 0,
                    y = 0,
                    z = 1
                  )
                }
              ],
              label = 'Default View',
              method = 'relayout'
            ),
            dict(
              args = [
                {
                  'scene.camera.eye': dict(
                    x = 0., 
                    y = 0., 
                    z = 2.5
                  ),
                  'scene.camera.up': dict(
                    x = 0,
                    y = 1,
                    z = 0
                  )
                }
              ],
              label = 'Top View (+XY)',
              method = 'relayout'
            ),
            dict(
              args = [
                {
                  'scene.camera.eye': dict(
                    x = 0., 
                    y = 0., 
                    z = -2.5
                  ),
                  'scene.camera.up': dict(
                    x = 0,
                    y = 1,
                    z = 0
                  )
                }
              ],
              label = 'Bottom View (-XY)',
              method = 'relayout'
            ),
            dict(
              args = [
                {
                  'scene.camera.eye': dict(
                    x = 0., 
                    y = 2.5, 
                    z = 0.
                  ),
                  'scene.camera.up': dict(
                    x = 0,
                    y = 0,
                    z = 1
                  )
                }
              ],
              label = 'Front View (+XZ)',
              method = 'relayout'
            ),
            dict(
              args = [
                {
                  'scene.camera.eye': dict(
                    x = 0., 
                    y = -2.5, 
                    z = 0.
                  ),
                  'scene.camera.up': dict(
                    x = 0,
                    y = 0,
                    z = 1
                  )
                }
              ],
              label = 'Back View (-XZ)',
              method = 'relayout'
            ),
            dict(
              args = [
                {
                  'scene.camera.eye': dict(
                    x = 2.5, 
                    y = 0., 
                    z = 0.
                  ),
                  'scene.camera.up': dict(
                    x = 0,
                    y = 0,
                    z = 1
                  )
                }
              ],
              label = 'Right View (+YZ)',
              method = 'relayout'
            ),
            dict(
              args = [
                {
                  'scene.camera.eye': dict(
                    x = -2.5, 
                    y = 0., 
                    z = 0.
                  ),
                  'scene.camera.up': dict(
                    x = 0,
                    y = 0,
                    z = 1
                  )
                }
              ],
              label = 'Left View (-YZ)',
              method = 'relayout'
            )
          ]
        ),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        y = 0.2
      )
    ]
  )

  return [
    html.Div(
      id = 'impact-graph-header',
      className = 'impact-graph-header'
    ), 
    dcc.Graph(
      id = 'impact-graph',
      figure = figure,
    )
  ]

def impact_toolbar():
  return [
    html.H2('Impact Toolbar'),
    # axis limit double sliders (???)
    # control z scale
      # see if you can access the figure from outside of the callback so the whole graph doesn't have to rerender
  ]

def scanline_toolbar(impact):
  scanline_info = []
  for i, scanline in enumerate(impact.scanlines):
    scanline_info.append(
      html.Div(
        id = f'scanline-toolbar-info-{i}',
        children = [
          html.Button(
            f'View Scanline {i + 1}: {scanline.ypos:.5f}mm',
            className = 'scanline-view-button',
            id = dict(
              type = 'scanline-view-button',
              index = i
            )
          )
        ]
      )
    )
  
  return [
    html.H2('Scanline Toolbar'),
    html.Div(
      id = 'scanline-toolbar-scanlines',
      className = 'scanline-toolbar-scanlines',
      children = [scanline for scanline in scanline_info]
    )
  ]

def scanline_figure(impact, index):
  scanline = impact.scanlines[index]

  figure = subplots.make_subplots(
    rows = 3,
    subplot_titles = (
      'Raw Data',
      'Slope-Corrected Data',
      'Smoothened Slope-Corrected Data'
    )
  )

  figure.add_traces(
    [
      go.Scatter(
        x = scanline.data[:, 0],
        y = scanline.data[:, 1],
      ),
      go.Scatter(
        x = scanline.data_corrected[:, 0],
        y = scanline.data_corrected[:, 1],
      ),
      go.Scatter(
        x = scanline.data_corrected_smooth[:, 0],
        y = scanline.data_corrected_smooth[:, 1],
      )
    ],
    rows = [1, 2, 3],
    cols = [1, 1, 1]
  )

  figure.update_layout(
    height = 800, 
    title_text = f'Scanline {index + 1}: {scanline.ypos:.5f}mm',
    showlegend = False
  )
  
  # regression button (yes no dropdown)
  # change moving average scale (dropdown with values between 100-500)
  # something with slope and intercept values

  return [
    html.Div(
      id = 'scanline-graphs-header',
      className = 'scanline-graphs-header'
    ),
    dcc.Graph(
      id = 'scanline-graph',
      figure = figure
    )
  ]