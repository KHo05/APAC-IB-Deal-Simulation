from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

def add_bar_chart(slide, df, x, y):
    chart_data = CategoryChartData()
    chart_data.categories = df.index.astype(str)
    chart_data.add_series('PV', df["PV"])
    x, y, cx, cy = x, y, Inches(6), Inches(4.5)
    slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data)