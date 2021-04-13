import base64
import datetime
import io
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
import pickle
import dash_auth
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'fly': '0000'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


with open("doctm.pkl",'rb') as f:
    doctm = pickle.load(f)
with open("df_30.pkl",'rb') as f:
    top_word = pickle.load(f)

w= 5
F= []
for i in range(30):
    F.append(doctm[i+1][w])

slctid =0
trace1 = go.Bar(
    x = list(range(1,31)),
    y=F,
    name='Topic score'
)


app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1',children =[html.Div([
html.Div([
    html.H2(children='Topic model  with Dash'),
    dcc.Dropdown(
                    id='docid',
                    options=[{'label': i, 'value': i} for i in doctm.index],
                    placeholder='Search a document id',
                    searchable=True,
                    value=1
                ),
    dcc.Graph(id='topic_doc',figure=go.Figure(data=trace1) 
              )],style={'width': '40%', 'display': 'inline-block',  'float': 'left', 'height':'100%',"textAlign":'left'}),
              

html.Div([dash_table.DataTable(  
    id='view_doc',                    
                    columns=[{'name':i, 'id':i} for i in doctm[['paper']].columns],
                    data=doctm[doctm.index == slctid][['paper']].to_dict('records'),
                    # fixed_rows={ 'headers': True, 'data': 0 },
                    style_table={ 'height':'500px','overflow':'scroll'},
                    style_cell={
        'whiteSpace': 'normal',
        'height': 'auto',
        'width':'55%',
        "textAlign":"left",
        'font_size': '20px',
        "font-family":'Microsoft JhengHei'
    },
                    )]
, style={'width': '55%', 'display': 'inline-block',  'float': 'right', 'height':'100%',"textAlign":'left','padding-top': '50px',}),

html.Div([dash_table.DataTable(  
    id='topic word',
 columns=[{'name':i, 'id':i} for i in top_word.columns],
                    data=top_word.to_dict('records'),

                    style_table={ 'height':'500px','overflow':'scroll'},
                    style_cell={
        'whiteSpace': 'normal',
        'height': 'auto',
        "textAlign":"left"
    },
                    # page_current=0,
                    # page_size=PAGE_SIZE,
                    )]
, style={'width': '100%', 'display': 'inline-block',  'float': 'left', 'height':'100%',"textAlign":'left','padding-top': '50px',})


])]),
        dcc.Tab(label='Tab two', value='tab-2',children = [html.Div([
            dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
        ])]),
        ]),
    html.Div(id='main_page')
])


@app.callback(
    dash.dependencies.Output('topic_doc', 'figure'),
    [dash.dependencies.Input('docid', 'value')]
    )
def update_figure(selected_docid):
    # filtered_df = doctm[doctm.index == selected_docid]
    F= []
    for i in range(30):
        F.append(doctm[i+1][selected_docid])

    trace = []
    trace.append(go.Bar(
    x=list(range(1,31)),
    y=F,
    name='Topic score'
    ))
    return {'data':trace}
@app.callback(
    dash.dependencies.Output('view_doc', 'data'),
    [dash.dependencies.Input('docid', 'value')
     ])
def update_table(selected_docid):
    data=doctm[doctm.index == selected_docid][['paper']].to_dict('records')
    return data



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        # elif 'pdf' in filename:
        #     df = io.BytesIO(decoded)
        #     print(e)
    except Exception as e:
        print(e)
        print(df)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



if __name__ == '__main__':
    app.run_server(debug=True,port=8080,host='192.168.7.104')