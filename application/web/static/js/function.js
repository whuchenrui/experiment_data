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

function paint_pb_save_click(result){
    $('#container').highcharts({
        title: {
            text: 'click与save的 position-bias图',
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
                    text: '概率'
                }
            }],
        tooltip: {
            formatter: function () {
                return '第 <b>' + this.point.x + '</b> 页<br> 概率: <b>' + this.point.y + '</b><br> 时刻: ' +
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
            paint_pb_save_click(result);
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

function next_page(){
    var page = $('#page').text();
    var date = $('#date').text();
    var hour = $('#hour').text();
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "page");
    form.setAttribute("target", "_blank");
    page = parseInt(page);
    page++;
    var input_page = document.createElement("input");
    input_page.setAttribute("name", "page");
    input_page.setAttribute("value", page);
    var input_date = document.createElement("input");
    input_date.setAttribute("name", "date");
    input_date.setAttribute("value", date);
    var input_hour = document.createElement("input");
    input_hour.setAttribute("name", "hour");
    input_hour.setAttribute("value", hour);
    form.appendChild(input_page);
    form.appendChild(input_date);
    form.appendChild(input_hour);
    form.submit();
}

function previous_page(){
    var page = $('#page').text();
    var date = $('#date').text();
    var hour = $('#hour').text();
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "page");
    form.setAttribute("target", "_blank");
    page = parseInt(page);
    if (page>1){
        page--;
        var input_page = document.createElement("input");
        input_page.setAttribute("name", "page");
        input_page.setAttribute("value", page);
        var input_date = document.createElement("input");
        input_date.setAttribute("name", "date");
        input_date.setAttribute("value", date);
        var input_hour = document.createElement("input");
        input_hour.setAttribute("name", "hour");
        input_hour.setAttribute("value", hour);
        form.appendChild(input_page);
        form.appendChild(input_date);
        form.appendChild(input_hour);
        form.submit();
    }else{
        alert('已经是第一页!');
    }
}


function check_validation(){
    var page = $('#page').val();
    var date = $('#date').val();
    var hour = $('#hour').val();
    if (!isNaN(page)){
        var reg = /^\d{2}$/;
        if ((hour != "") && (date != "")){
            if ( 0 <= parseInt(hour) && parseInt(hour) < 24 && (reg.test(hour))){
                return true;
            }else{
                alert("小时格式为两位数字，如04 23");
            }
        }else{
            alert("输入不能为空！");
        }
    }else{
        alert("输入页码应该为数字！");
    }
    return false;
}
