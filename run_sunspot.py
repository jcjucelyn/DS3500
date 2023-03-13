import sunspot as hw
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)


@app.callback(
    Output('sunspot', 'figure'),
    Input('year_select', 'value'),
    Input('month_select', 'value')
)
def main(years, months):
    hw.update_plt(years, months)


app.run_server(debug=True)


# call functions to make the sankey diagrams
if __name__ == '__main__':
    main()
