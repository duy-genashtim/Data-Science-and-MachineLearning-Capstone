# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
launch_list = spacex_df['Launch Site'].unique()
launch_sites = []
launch_sites.append({'label': 'All Sites', 'value': 'All Sites'})
for site in launch_list:
    launch_sites.append({'label': site, 'value': site})
min_payload = spacex_df["Payload Mass (kg)"].min()
max_payload = spacex_df['Payload Mass (kg)'].max()
# new_df = spacex_df[spacex_df["Launch Site"] == 'CCAFS LC-40']
# new_df["name"] = new_df["class"].apply(lambda x: 'Failure' if x == 0 else 'Success')
# count = new_df["name"].value_counts().reset_index().rename(columns={"index":"name","name":"values"})

# print(new_df.shape)
# print(count)
# exit(0)

# print(launch_sites)
# exit(0)
# [{'label': 'All Sites', 'value': 'All Sites'}, {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}, {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}]
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',options=launch_sites,value="All Sites", placeholder = "Select a Launch Site here", searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id="payload-slider", min=0, max=10000,step=1000,marks={0:'0',2500:'2500',5000:'5000',7500:'7500',10000:'10000'}, value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id="success-pie-chart",component_property="figure"),
Input(component_id="site-dropdown",component_property="value"))
def get_pie_chart(entered_site):

    if entered_site=="All Sites":
        new_df = spacex_df.groupby(['Launch Site'])["class"].sum().to_frame()
        new_df = new_df.reset_index()
        print("All Sites",new_df)
        fig = px.pie(new_df, values='class', names='Launch Site', title='Total Success Launches by Site')
    else:
        new_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        new_df["name"] = new_df["class"].apply(lambda x: 'Failure' if x == 0 else 'Success')
        new_df = new_df["name"].value_counts().reset_index().rename(columns={"index":"name","name":"class"})
        # print(new_df)
        # new_df = spacex_df[spacex_df["Launch Site"] == entered_site]["class"].value_counts().to_frame()
        # new_df["name"] = ["Failure", "Success"]
        print("Site",new_df)
        # exit(0)
        fig = px.pie(new_df,values="class",names="name",title="Total Success Launches by "+entered_site)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id="success-payload-scatter-chart",component_property="figure"),
[Input(component_id="site-dropdown", component_property="value"), Input(component_id="payload-slider", component_property="value")])

def draw_plotly_scatter(launch_site,payload_mass):
    min_val = payload_mass[0]
    max_val = payload_mass[1]
    scatter_df = spacex_df
    if launch_site=="All Sites":
        scatter_df = spacex_df.loc[(spacex_df["Payload Mass (kg)"] >= min_val) & (scatter_df["Payload Mass (kg)"] <= max_val)]
        # scatter_df = spacex_df[spacex_df["Payload Mass (kg)"] >= min_val & scatter_df["Payload Mass (kg)"] <= max_val] 
        fig = px.scatter(scatter_df,x="Payload Mass (kg)",y="class",color="Booster Version Category")
    else:
        scatter_df = spacex_df.loc[(spacex_df["Payload Mass (kg)"] >= min_val) & (scatter_df["Payload Mass (kg)"] <= max_val) & spacex_df["Launch Site"] == launch_site]
        scatter_df = spacex_df.loc[(spacex_df["Payload Mass (kg)"] >= min_val) & (scatter_df["Payload Mass (kg)"] <= max_val) & spacex_df["Launch Site"] == launch_site]
        # scatter_df = spacex_df[spacex_df["Launch Site"] == launch_site & (spacex_df["Payload Mass (kg)"]>= min_val & spacex_df["Payload Mass (kg)"]<= max_val)]
        fig = px.scatter(scatter_df,x="Payload Mass (kg)",y="class",color="Booster Version Category")
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
