/**
 * Created by CRay on 2014/12/21.
 */

function get_pb_data() {
    var min_show = $('#min_show').val();
    var min_page = $('#min_page').val();
    var max_pic_num = $('#max_pic_num').val();
    $.ajax({
        type: 'post',
        dataType: 'json',
        async: true,
        url: '/pb',
        data: {
            'min_show': min_show,
            'min_page': min_page,
            'max_pic_num': max_pic_num,
            'total': 0
        },
        success: function(result){
            paint_pb(result);
        }
    });
}

function paint_pb(result){
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


function get_pb_data_total(){
    var min_show = $('#min_show').val();
    var min_page = $('#min_page').val();
    var max_pic_num = $('#max_pic_num').val();
    $.ajax({
        type: 'post',
        dataType: 'json',
        async: true,
        url: '/pb',
        data: {
            'min_show': min_show,
            'min_page': min_page,
            'max_pic_num': max_pic_num,
            'total': 1
        },
        success: function(result){
            paint_pb_normal(result);
        }
    });
}

function get_pb_hour_data(){
    $.ajax({
        type: 'post',
        dataType: 'json',
        async: true,
        url: '/hour',
        data: {
            'test': 'test'
        },
        success: function(result){
//            str_result = JSON.stringify(result);
            paint_pb_normal(result);
        }
    });
}


function paint_pb_normal(result){
    $('#container').highcharts({
        title: {
            text: 'position-bias小时分布图'
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
        series: [{
            'name' : 'distribution per hour',
            'data': result
        }]
    });
}