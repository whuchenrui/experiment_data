/**
 * Created by CRay on 2014/12/21.
 */

function get_data() {
    var min_show = $('#min_show').val();
    var min_page = $('#min_page').val();
    $.ajax({
        type: 'post',
        dataType: 'json',
        async: true,
        url: '/pb',
        data: {
            'min_show': min_show,
            'min_page': min_page
        },
        success: function(result){
            paint(result);
        }
    });
}

function paint(result){
    $('#container').highcharts({
        title: {
            text: 'position-bias图',
            x: -20 //center
        },
        xAxis: {
            title: {
                text: '图片所在页数'
            },
            tickInterval: 1
        },
        yAxis:[{
                title: {
                    text: '点击概率'
                }
            }],
        tooltip: {
            formatter: function () {
                return '第 <b>' + this.point.x + '</b> 页<br> 概率: <b>' + this.point.y + '</b><br> 小时: ' +
                        this.point.z;
          }
        },
        series: result
    });
}