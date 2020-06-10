from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
from pyecharts import options as opts
bar = (

    Bar(opts.InitOpts(width = '1000px',height = '500px',theme=ThemeType.INFOGRAPHIC))

    .add_xaxis(top_n.index.tolist())
    .add_yaxis('点评数量',top_n['点评数量'].tolist())
    .add_yaxis('攻略提到数量',top_n['攻略提到数量'].tolist())
    .add_yaxis('星级',top_n['星级'].tolist())
    .set_global_opts(
        toolbox_opts = opts.ToolboxOpts(is_show = True),
        datazoom_opts= [opts.DataZoomOpts(range_start=10, range_end=80,is_zoom_lock=False)],
        )
    .set_series_opts(
       markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                ]
            ),
        markline_opts = opts.MarkLineOpts(
            data = [
                opts.MarkLineItem(type_ = 'average', name= '平均值')
            ]
            )
        )
    )
bar.render_notebook()
