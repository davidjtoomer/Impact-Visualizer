import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq

def impact_graph(impact):
  figure = go.Figure()

  figure.add_trace(
    go.Surface(
      x = impact.X,
      y = impact.Y,
      z = impact.Z,
      colorscale = 'Viridis',
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
      dict(
        buttons = list(
          [
            dict(
              args = ['colorscale', 'Viridis'],
              label = 'Viridis',
              method = 'restyle'
            ),
            dict(
              args = ['colorscale', 'Cividis'],
              label = 'Cividis',
              method = 'restyle'
            ),
            dict(
              args = ['colorscale', 'RdBu'],
              label = 'Red-Blue',
              method = 'restyle'
            ),
            dict(
              args = ['colorscale', 'Reds'],
              label = 'Red',
              method = 'restyle'
            ),
            dict(
              args = ['colorscale', 'Greens'],
              label = 'Green',
              method = 'restyle'
            ),
            dict(
              args = ['colorscale', 'Blues'],
              label = 'Blue',
              method = 'restyle'
            )
          ]
        ),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        y = 0.8
      ),
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
        y = 0.6
      ),
      dict(
        buttons = list(
          [
            dict(
              args = ['scene.camera.eye', dict(
                x = 1.25, 
                y = 1.25, 
                z= 1.25
              )],
              label = 'Default View',
              method = 'relayout'
            ),
            dict(
              args = list(
                [
                  'scene.camera.eye', dict(
                    x = 0., 
                    y= 0., 
                    z= 2.5
                  ),
                  'scene.camera.'
                ]
              ),
              label = 'Top View (+XY)',
              method = 'relayout'
            ),
            dict(
              args = ['scene.camera.eye', dict(
                x = 0., 
                y = 0., 
                z = -2.5
              )],
              label = 'Bottom View (-XY)',
              method = 'relayout'
            ),
            dict(
              args = ['scene.camera.eye', dict(
                x = 0., 
                y = 2.5, 
                z = 0.
              )],
              label = 'Front View (+XZ)',
              method = 'relayout'
            ),
            dict(
              args = ['scene.camera.eye', dict(
                x = 0., 
                y = -2.5, 
                z = 0.
              )],
              label = 'Back View (-XZ)',
              method = 'relayout'
            ),
            dict(
              args = ['scene.camera.eye', dict(
                x = 2.5, 
                y = 0., 
                z = 0.
              )],
              label = 'Right View (+YZ)',
              method = 'relayout'
            ),
            dict(
              args = ['scene.camera.eye', dict(
                x = -2.5, 
                y = 0., 
                z = 0.
              )],
              label = 'Left View (-YZ)',
              method = 'relayout'
            )
          ]
        ),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        y = 0.4
      )
    ]
  )

  return dcc.Graph(
    id = 'impact-graph',
    figure = figure,
  )

'''
def scanline_graph(impact):
  return

def scanline_toolbar(impact):
  scanline_info = []
  for i, scanline in enumerate(impact.scanlines):
    # create the view and the button
    scanline_info.append(
      html.Div(
        id = f'scanline-info-{i}'
      )
    )
  return [
    # regression line on or off
    html.Div(
      id = 'scanline-toolbar-regression',
      className = 'scanline-toolbar-regression',
      children = []
    ),
    # moving average values
    html.Div(

    ),
    html.Div(
      id = '',
      children = [scanline for scanline in scanline_info]
    )
  ]
'''