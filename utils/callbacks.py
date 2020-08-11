import plotly.graph_objects as go
from plotly import subplots
import plotly.express as px
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
      z = impact.Z
    )
  )

  figure.update_layout(
    scene = dict(
      xaxis_title = 'X (mm)',
      yaxis_title = 'Y (mm)',
      zaxis_title = 'Z (µm)',
    ),
    font_size = 10,
    height = 600,
    margin = dict(
      l = 20,
      r = 10,
      b = 50,
      t = 50
    )
  )

  return figure, [
    html.Div(
      id = 'impact-graph-header',
      className = 'impact-graph-header'
    ), 
    dcc.Graph(
      id = 'impact-graph',
      figure = figure,
      config = {
        'displaylogo': False,
        'toImageButtonOptions': {
          'format': 'png',
          'height': None,
          'width': None,
          'scale': 1
        }
      }
    )
  ]

def update_impact(impact, figure, num_contours, colorscale, projection, view, x_range, y_range, z_scale):
  # contours
  if num_contours:
    contours = dict(
      z = dict(
        show = True,
        start = impact.zmin,
        end = impact.zmax,
        size = (impact.zmax - impact.zmin) / (num_contours)
      ),
    )
  else:
    contours = dict(
      z = dict(
        show = False
      )
    )
  figure.data[0]['contours'] = contours

  # colorscale
  figure.data[0]['colorscale'] = colorscale

  # projection
  figure.update_layout(
    scene_camera = dict(
      projection = dict(
        type = projection
      )
    )
  )

  # view
  if view == 'default':
    x_eye, y_eye, z_eye = 1.25, 1.25, 1.25
    x_up, y_up, z_up = 0, 0, 1
  elif view == 'top':
    x_eye, y_eye, z_eye = 0., 0., 2.5
    x_up, y_up, z_up = 0, 1, 0
  elif view == 'bottom':
    x_eye, y_eye, z_eye = 0., 0., -2.5
    x_up, y_up, z_up = 0, 1, 0
  elif view == 'front':
    x_eye, y_eye, z_eye = 0., 2.5, 0.
    x_up, y_up, z_up = 0, 0, 1
  elif view == 'back':
    x_eye, y_eye, z_eye = 0., -2.5, 0.
    x_up, y_up, z_up = 0, 0, 1
  elif view == 'right':
    x_eye, y_eye, z_eye = 2.5, 0, 0.
    x_up, y_up, z_up = 0, 0, 1
  elif view == 'left':
    x_eye, y_eye, z_eye = -2.5, 0, 0.
    x_up, y_up, z_up = 0, 0, 1
  figure.update_layout(
    scene_camera = dict(
      up = dict(
        x = x_up,
        y = y_up,
        z = z_up
      ),
      center = dict(
        x = 0,
        y = 0,
        z = 0
      ),
      eye = dict(
        x = x_eye,
        y = y_eye,
        z = z_eye
      )
    )
  )

  # x- and y-range
  figure.update_layout(
    scene = dict(
      xaxis = dict(
        range = (x_range[0], x_range[1])
      ),
      yaxis = dict(
        range = (y_range[0], y_range[1])
      )
    )
  )

  # z_scale
  figure.update_scenes(
    aspectmode = 'manual',
    aspectratio = dict (
      x = (x_range[1] - x_range[0]) / (y_range[1] - y_range[0]),
      y = 1,
      z = 10 ** z_scale
    )
  )

  return figure

def impact_toolbar(impact):
  return [
    html.H2('Impact Toolbar'),
    # contours
    html.Div(
      id = 'impact-contour-container',
      className = 'impact-toolbar-subcontainer',
      children = [
        html.H6('Number of Contours'),
        html.Div(
          id = 'contour-slider-container',
          className = 'contour-slider-container',
          children = [
            dcc.Slider(
              id = 'num-contours-slider',
              className = 'num-contours-slider',
              min = 0,
              max = 30,
              step = 1,
              value = 0
            ),
            html.Div(id = 'display-num-contours')
          ]
        )
      ]
    ),
    # colorscale
    html.Div(
      id = 'impact-colorscale-container',
      className = 'impact-contour-container',
      children = [
        html.H6('Colorscale'),
        dcc.Dropdown(
          id = 'colorscale-dropdown',
          className = 'colorscale-dropdown',
          options = [
            {
              'label': 'Jet', 
              'value': 'Jet'
            },
            {
              'label': 'Viridis', 
              'value': 'Viridis'
            },
            {
              'label': 'Red-Blue', 
              'value': 'RdBu'
            }
          ],
          value = 'Jet'
        )
      ]
    ),
    # projection
    html.Div(
      id = 'impact-projection-container',
      className = 'impact-projection-container',
      children = [
        html.H6('Projection'),
        dcc.Dropdown(
          id = 'projection-dropdown',
          className = 'projection-dropdown',
          options = [
            {
              'label': 'Orthographic',
              'value': 'orthographic'
            },
            {
              'label': 'Perspective',
              'value': 'perspective'
            }
          ],
          value = 'orthographic'
        )
      ]
    ),
    # view
    html.Div(
      id = 'impact-view-container',
      className = 'impact-view-container',
      children = [
        html.H6('View'),
        dcc.Dropdown(
          id = 'view-dropdown',
          className = 'view-dropdown',
          options = [
            {
              'label': 'Default View',
              'value': 'default'
            },
            {
              'label': 'Top View (+XY)',
              'value': 'top'
            },
            {
              'label': 'Bottom View (-XY)',
              'value': 'bottom'
            },
            {
              'label': 'Front View (+XZ)',
              'value': 'front'
            },
            {
              'label': 'Back View (-XZ)',
              'value': 'back'
            },
            {
              'label': 'Right View (+YZ)',
              'value': 'right'
            },
            {
              'label': 'Left View (-YZ)',
              'value': 'left'
            }
          ],
          value = 'default'
        )
      ]
    ),
    # x-range
    html.Div(
      id = 'impact-xrange-container',
      className = 'impact-xrange-container',
      children = [
        html.H6('X-Axis Range'),
        html.Div(
          id = 'x-range-slider-container',
          className = 'x-range-slider-container',
          children = [
            html.Div(id = 'left-x-range-slider'),
            dcc.RangeSlider(
              id = 'x-range-slider',
              className = 'x-range-slider',
              min = 0,
              max = impact.xrange,
              step = impact.xrange / 25,
              value = [0, impact.xrange]
            ),
            html.Div(id = 'right-x-range-slider')
          ]
        )
      ]
    ),
    # y-range
    html.Div(
      id = 'impact-yrange-container',
      className = 'impact-yrange-container',
      children = [
        html.H6('Y-Axis Range'),
        html.Div(
          id = 'y-range-slider-container',
          className = 'y-range-slider-container',
          children = [
            html.Div(id = 'left-y-range-slider'),
            dcc.RangeSlider(
              id = 'y-range-slider',
              className = 'y-range-slider',
              min = 0,
              max = impact.yrange,
              step = impact.yrange / 25,
              value = [0, impact.yrange]
            ),
            html.Div(id = 'right-y-range-slider')
          ]
        )
      ]
    ),
    # z-scale
    html.Div(
      id = 'impact-zscale-container',
      className = 'impact-zscale-container',
      children = [
        html.H6('Z-Axis Scale (Logarithmic)'),
        html.Div(
          id = 'z-scale-slider-container',
          className = 'z-scale-slider-container',
          children = [
            dcc.Slider(
              id = 'z-scale-slider',
              className = 'z-scale-slider',
              min = -1,
              max = 1,
              step = 0.1,
              value = 0
            ),
            html.Div(id = 'display-z-scale')
          ]
        )
      ]
    )
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
      id = 'scanline-toolbar-view-all',
      className = 'scanline-toolbar-view-all',
      children = [
        html.H6('All Scanlines'),
        dcc.RadioItems(
          id = 'scanline-view-all-button',
          className = 'scanline-view-all-button',
          options = [
            {
              'label': 'Display All Scans',
              'value': 'show'
            },
            {
              'label': 'Hide All Scans',
              'value': 'hide'
            }
          ],
          value = 'show'
        )
      ]
    ),
    html.Div(
      id = 'scanline-toolbar-scanlines',
      className = 'scanline-toolbar-scanlines',
      children = [
        html.H6('Individual Scanlines'),
        *[scanline for scanline in scanline_info]
      ]
    )
  ]

def all_scanline_figure(impact, visible = None):
  figure = go.Figure()

  figure.add_traces(
    [
      go.Scatter(
        x = scanline.data_corrected_smooth[:, 0],
        y = scanline.data_corrected_smooth[:, 1],
        name = f'Scanline {i + 1}',
        visible = visible
      )
      for i, scanline in enumerate(impact.scanlines)
    ]
  )

  figure.update_layout(
    height = 500,
    title_text = 'Superimposed Scanlines'
  )

  return [
    html.Div(
      id = 'scanline-graphs-header',
      className = 'scanline-graphs-header'
    ),
    dcc.Graph(
      id = 'scanline-graph-all',
      figure = figure
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