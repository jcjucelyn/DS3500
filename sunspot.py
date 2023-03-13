"""
Jocelyn Ju
DS3500 / SunDash
Sunspot Dashboard / HW 2
Created 1/31/2023 / Updated 2/10/2023
"""

# import libraries
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime

# read the csv file into a dataframe
df_monthly = pd.read_csv('data/monthly.csv', sep=';',
                         names=['Year', 'Month', 'Fraction_Date', 'Mean Sunspot',
                                'Mean STD', 'Observations', 'Marker'])

app = Dash(__name__)


# get the time and date the program is run
rn = datetime.now()
update_time = rn.strftime("%d/%m/%Y %H:%M:%S")
updated_time = "Last Updated: " + update_time


# layout for the dashboard
app.layout = html.Div([
    html.H1('Historical Sunspot Activity', style={'textAlign': 'center', 'fontFamily': 'Baskerville'}),
    html.H4('DS3500 | HW-02 | Ju', style={'textAlign': 'center', 'fontFamily': 'Baskerville'}),

    # div for the first graph and month selection slider
    html.Div([
        html.H2('Historical Sunspot Activity', style={'textAlign': 'center', 'fontFamily': 'Baskerville'}),
        dcc.Graph(id='sunspot', style={'display': 'inline-block'}),

        # month selection slider
        html.P('Months to Smooth Data Over:', style={'textAlign': 'left', 'fontFamily': 'Baskerville'}),
        dcc.Slider(id='month_select', min=1, max=20, step=1, value=6, tooltip={'placement': 'bottom'})],
        style={'display': 'inline-block'}),

    # sunspot cycle graph and sliders: cycle tuning and month
    html.Div([
        html.H2('Sunspot Cycle', style={'textAlign': 'center', 'fontFamily': 'Baskerville'}),
        dcc.Graph(id='spt_cycle', style={'display': 'inline-block'}),

        # cycle length slider
        html.P('Adjust Cycle Length', style={'textAlign': 'left', 'fontFamily': 'Baskerville'}),
        dcc.Slider(id='cycle_tune', min=1, max=20, step=1, value=11, tooltip={'placement': 'bottom'}),

        # month slider
        html.P('Adjust Months', style={'textAlign': 'left', 'fontFamily': 'Baskerville', 'display': 'inline-block'}),
        dcc.RangeSlider(1, 12, 1, marks={
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec',
        },
                        value=[2, 5], id='month_selector')],
        style={'display': 'inline-block', 'verticalAlign': 'top'}),

    # the years slider
    html.Div([
        html.P('Years:'),
        dcc.RangeSlider(1749, 2022, 20, marks={
                1749: '1749',
                1760: '1760',
                1780: '1780',
                1800: '1800',
                1820: '1820',
                1840: '1840',
                1860: '1860',
                1880: '1880',
                1900: '1900',
                1920: '1920',
                1940: '1940',
                1960: '1960',
                1980: '1980',
                2000: '2000',
                2022: '2022'
            },
            value=[1980, 2010], id='year_select', tooltip={'placement': 'bottom'})]),

    # display the sun image
    html.Div([html.H2('A Real-Time Image of the Sun', style={'textAlign': 'center', 'fontFamily': 'Baskerville'}),

              # get the update time of the image
              html.P(updated_time),
              html.Img(src='https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg',
                       width='500', id='sun_img', alt='real-time image of the sun')],
             style={'textAlign': 'center', 'display': 'inline-block', 'margin-left': 100}),

    # create the dropdown and additional images
    html.Div([
        html.H2('Select Another Image to Show', style={'fontFamily': 'Baskerville', 'display': 'inline-block',
                                                       'textAlign': 'center'}),
        dcc.Dropdown(
                id='dropdown',
                options=['EIT 171', 'EIT 195', 'EIT 284', 'EIT 304',
                         'SDO/HMI Magnetogram', 'LASCO C2', 'LASCO C3'],
                clearable=True, placeholder='Select an Image', style={'textAlign': 'left', 'fontFamily': 'Baskerville'}
        ),

        # provide additional images for user to choose from
        html.Div(id="image", children=[html.Img(
            src='https://soho.nascom.nasa.gov/data/realtime/eit_171/1024/latest.jpg',
            id='eit-171', title='EIT 171'),
                                       html.Img(
                                           src='https://soho.nascom.nasa.gov/data/realtime/eit_195/1024/latest.jpg',
                                           id='eit-195', title='EIT 195'),
                                       html.Img(
                                           src='https://soho.nascom.nasa.gov/data/realtime/eit_284/1024/latest.jpg',
                                           id='eit-284', title='EIT 284'),
                                       html.Img(
                                           src='https://soho.nascom.nasa.gov/data/realtime/eit_304/1024/latest.jpg',
                                           id='eit-304', title='EIT 304'),
                                       html.Img(
                                           src='https://soho.nascom.nasa.gov/data/realtime/hmi_mag/1024/latest.jpg',
                                           id='hmi-mag', title='SDO/HMI Magnetogram'),
                                       html.Img(src='https://soho.nascom.nasa.gov/data/realtime/c2/1024/latest.jpg',
                                                id='c2', title='LASCO C2'),
                                       html.Img(src='https://soho.nascom.nasa.gov/data/realtime/c3/1024/latest.jpg',
                                                id='c3', title='LASCO C3')],
                 style={'textAlign': 'center', 'display': 'inline-block'})
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'margin-left': 300})])


# Question 1: Historical Sunspot Dashboard ---------------------------------------------
def filt_yrs(df, years):
    """
    filter the user-selected years from the dataframe
    :param df: (dataframe) a dataframe with years and additional attributes
    :param years: (list) two user-defined years, a min and max
    :return: df_updated: (dataframe) the dataframe filtered to just include the years
            within the user specified range
    """

    min = years[0]
    max = years[1]
    df_updated = df[df['Year'].between(min, max)][['Year', 'Month', 'Mean Sunspot']]

    # return the updated dataframe to user
    return df_updated


def avg_mth(months, df_new):
    """
    Find the rolling average across some number of months
    :param months: (int) a user-selected integer in range[0,20] over which to find the rolling average
    :param df_new: (dataframe) a dataframe with a minimum of months and mean sunspot values
    :return: df_new: (dataframe) the dataframe updated with a Rolling Average column
    """

    # create a new column with the rolling average sunspots
    df_new['Rolling Avg'] = df_new['Mean Sunspot'].rolling(months).mean()

    df_new.dropna(inplace=True)

    return df_new


# update the plot when the slider is changed
@app.callback(
    Output('sunspot', 'figure'),
    Input('year_select', 'value'),
    Input('month_select', 'value')
)
def update_plt(years, months):
    """
    Update the Historical Sunspot Activity graph when the slider(s) are changed
    :param years: (list) two user-defined years, a min and max
    :param months: (int) a user-selected integer in range[0,20] over which to find the rolling average
    :return: update the Historical Sunspot Activity graph to show the number of years/change in smoothness
    """

    # filter out the appropriate years
    df_new = filt_yrs(df_monthly, years)

    df_avg = avg_mth(months, df_new)

    # plot the data
    fig = px.line(df_new, x='Year', y='Mean Sunspot')

    # add the smoothed line
    fig.add_scatter(x=df_avg['Year'], y=df_avg['Rolling Avg'], name='Smoothed')

    return fig


# Question 2: Sunspot Cycle --------------------------------------------------------------
def get_mod(years, months, cycle_yrs):
    """
    Find the modulus for each date
    :param years: (list) two user-defined years, a min and max
    :param months: (list) two user-defined months, a min and max
    :param cycle_yrs: (int) the user-defined length of the cycle to plot over
    :return: year_list: (list) a list of years moduli were found for
    :return: month_list: (list) a list of months moduli were found for
    :return: modulus_list: (list) a list of calculated moduli
    :return: sunspot_list: (list) a list of corresponding mean sunspot values
    """

    # turn the years and months given into iterable lists
    years = range(years[0], years[-1])
    months = range(months[0], months[-1])

    # initialize lists to store values
    year_list = []
    modulus_list = []
    month_list = []
    sunspot_list = []

    for i in years:
        for j in months:

            # get the Fraction_Date from the data
            df_new = df_monthly[df_monthly['Year'] == i]
            df_new = df_new[df_new['Month'] == j]
            frac_yr = df_new['Fraction_Date']
            frac_yr = float(frac_yr)

            # find modulus of the years for the cycle
            modulus = frac_yr % cycle_yrs

            # get the value of the mean sunspots
            ms = df_new['Mean Sunspot'].values
            ms = ms.tolist()

            # add the values to their corresponding list
            modulus_list.append(modulus)
            month_list.append(j)
            year_list.append(i)
            sunspot_list = sunspot_list + ms

    return year_list, month_list, modulus_list, sunspot_list


@app.callback(
    Output('spt_cycle', 'figure'),
    Input('year_select', 'value'),
    Input('month_selector', 'value'),
    Input('cycle_tune', 'value')
)
def update_cycle(years, months, cycle_yrs):
    """
    Update the Sunspot Cycle scatterplot visualization given the parameters
    :param years: (list) two user-defined years, a min and max
    :param months: (list) two user-defined months, a min and max
    :param cycle_yrs: (int) the length of the cycle to plot sunspots over, from 1 to 20
    :return: update the Sunspot Cycle scatterplot according to the parameters
    """

    # create lists and find the moduli from get_mod
    year_list, month_list, modulus_list, sunspot_list = get_mod(years, months, cycle_yrs)

    # update the plot with the modulus list and sunspot list
    mod_fig = px.scatter(x=modulus_list, y=sunspot_list,
                         labels={'x': 'Years',
                                 'y': '# of Sunspots'})
    return mod_fig


# Question 3: Current Image of the Sun -----------------------------------------------------
''' in Div id='sun-img' within app.layout
source will be called when webpage is reloaded,
keeping the image up to date '''


# Extra Credit: show the selected image from the dropdown ----------------------------------
@app.callback(
    Output('image', 'children'),
    Input('dropdown', 'value'),
)
def show_imgs(selected_val):
    """
    Show the selected image from the dropdown
    :param selected_val: (str) user selection from the dropdown menu
    :return: (image) the image that corresponds with the user's selection
    """

    # initialize a list of images and titles to compare to selected_val
    title_list = ['EIT 171', 'EIT 195', 'EIT 284', 'EIT 304', 'SDO/HMI Magnetogram', 'LASCO C2', 'LASCO C3']
    img_list = [html.Img(src='https://soho.nascom.nasa.gov/data/realtime/eit_171/1024/latest.jpg',
                width=500, id='eit-171', title='EIT 171'),
                html.Img(src='https://soho.nascom.nasa.gov/data/realtime/eit_195/1024/latest.jpg',
                width=500, id='eit-195', title='EIT 195'),
                html.Img(src='https://soho.nascom.nasa.gov/data/realtime/eit_284/1024/latest.jpg',
                width=500, id='eit-284', title='EIT 284'),
                html.Img(src='https://soho.nascom.nasa.gov/data/realtime/eit_304/1024/latest.jpg',
                width=500, id='eit-304', title='EIT 304'),
                html.Img(src='https://soho.nascom.nasa.gov/data/realtime/hmi_mag/1024/latest.jpg',
                width=500, id='hmi-mag', title='SDO/HMI Magnetogram'),
                html.Img(src='https://soho.nascom.nasa.gov/data/realtime/c2/1024/latest.jpg',
                width=500, id='c2', title='LASCO C2'),
                html.Img(src='https://soho.nascom.nasa.gov/data/realtime/c3/1024/latest.jpg',
                width=500, id='c3', title='LASCO C3')]

    # display the image that corresponds to the selected value from the dropdown
    if selected_val == title_list[0]:
        return img_list[0]
    elif selected_val == title_list[1]:
        return img_list[1]
    elif selected_val == title_list[2]:
        return img_list[2]
    elif selected_val == title_list[3]:
        return img_list[3]
    elif selected_val == title_list[4]:
        return img_list[4]
    elif selected_val == title_list[5]:
        return img_list[5]
    elif selected_val == title_list[6]:
        return img_list[6]


# run the server
app.run_server(debug=True)