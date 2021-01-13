
var url_prefix = "http://"+returnCitySN["cip"]+":5000/";

var cookie = {
                setCookie: function (name, value) {
                    document.cookie = name + '=' + value + ';';
                },
                getCookie: function (name) {
                    var arr = document.cookie.split('; ');
                    for (var i = 0; i < arr.length; i++) {
                        var arr2 = arr[i].split('=');
                        if (arr2[0] == name) {
                            return arr2[1];
                        }
                    }

                    return '';
                },
                removeCookie: function (name) {
                    cookie.setCookie(name, '', -1)
                }
            };

function sendRequest(url_suffix, data, func) {
    var url = url_prefix + url_suffix;
    $.ajax({
        type: "post",
        url: url,
        data: data,
        dataType: "json",
        processData: false,
        contentType: false,
        success: function (data) {
            func(data);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(this);
        }
    });
    return;
}



function GetRequest() {
    var url = location.search; //获取url中"?"符后的字串
    var theRequest = new Object();
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        strs = str.split("&");
        for (var i = 0; i < strs.length; i++) {
            theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
        }
    }
    return theRequest;
}

function add(type) {
    var content = page.content;
    var name = page.name;
    var tag = page.tag;
    var order = page.textList.length;
    if (type == 'block') {
        if (content == null) {
            return;
        }
        if (CHECK_URL(content)) {
            console.log(content);
            submit(content, 'url');
        }
        else {
            submit(content, 'text');
        }

        page.content = null;
        return;
    }
    if (name == null) {
        return;
    }
    var data = new FormData();
    data.append('phonenum', phonenum);
    data.append('name', name);
    data.append('tag', tag);
    sendRequest('collection/add', data, function () {
        getContent('collection');
    });
    page.content = null;
    page.name = null;
    page.tag = null;
}


function submit(content, type, order) {
    var url = "block/add";
    var data = new FormData();
    data.append("content", content);
    data.append('type', type);
    data.append('collection_id', page.id);
    console.log(data.get('content'));

    sendRequest(url, data, function () {
        getContent('block');
    })
}


function getContent(type) {
    var url;
    url = type + "/select";
    var data = new FormData();
    if ("undefined" != typeof phonenum) {
        data.append('phonenum', phonenum);
    }
    if (page.id != null) {
        data.append('id', page.id);
    }

    var name = $("#search").val();
    if (name != "") {
        data.append('name', name);
    }
    sendRequest(url, data, function (data) {
        if (type == 'collection') {
            page.textList = data.collections;
            checkLike(page);
        }
        else {
            page.textList = data.blocks;
            getWebName();
           
        }
        for (i in page.textList) {
            page.textList[i]['order'] = i;
        }
        compile();
    });
}

async function getWebName() {
    for (i in page.textList) {
        if (page.textList[i]['type'] != 'url') {
            continue;
        }
        (function (i) {
            var dt = new FormData();
            var obj = page.textList[i];
            
            dt.append('url', obj['content']);
            sendRequest('block/get_web_name', dt, function (data) {
                obj['title'] = data.name;
                Vue.set(page.textList, obj['order'], obj);
            });
        })(i);

    }
}

async function checkLike(list) {
    for (i in page.textList) {
        (function (i) {
            var dt = new FormData();
            var obj = list.textList[i];
            dt.append('collection_id', obj['id']);
            dt.append('phonenum', phonenum);
            sendRequest('collection/isLike', dt, function (data) {
                obj['isLike'] = data.isLike;
                Vue.set(list.textList, obj['order'], obj);
            });
        })(i);

    }
}
function get_url(i) {
    var data = new FormData();
    data.append('pic',page.textList[i]['content']['$binary']);
    sendRequest('block/get_pic',data,function(f){
    console.log(f);
    let reader = new FileReader();
    console.log(f);
    reader.readAsDataURL(f);
    reader.onload = function (e) {
        return e.target.files[0] || e.dataTransfer.files[0];
    };
    })

}


var page = new Vue({
    el: "#textList",
    data: {
        textList: [],
        id: null,
        name: null,
        tag: null,
        content: null,
    },
    methods: {
        swap: function (obj_id, dir, type) {
            var url = type + '/swap';

            var obj = this.textList[obj_id];
            var pos = obj_id;
            var origin_pos = pos;
            if (dir == 'up' && pos > 0) {
                pos--;
            }
            if (dir == 'down' && pos < this.textList.length - 1) {
                pos++;
            }
            obj['order'] = pos;
            var swap_obj = this.textList[pos];
            swap_obj['order'] = origin_pos;
            Vue.set(this.textList, origin_pos, swap_obj);
            Vue.set(this.textList, pos, obj);

            var data = new FormData();
            data.append("new_order", pos);
            data.append("id", obj.id);
            if (type == 'block') {
                data.append('collection_id', page.id);
            }
            sendRequest(url, data, getContent(type));
        },
        delete_item: function (order, type) {
            var url = type + '/delete';
            var data = new FormData();
            data.append("collection_id", this.id);
            console.log(order);
            if (type == "block") {
                data.append("block_id", this.textList[order]['id']);
            }
            this.textList.splice(this.textList[order], 1);
            sendRequest(url, data, function () { ; });
            for (i in page.textList) {
                page.textList[i]['order'] = i;
                if (type == 'block' && page.textList[i]['type'] == 'picture') {
                    page.textList[i]['content'] = get_url(page.textList[i]['content']);
                }

            }
        },
        jump_to: function (url, block_name, collection_id) {
            cookie.setCookie('name',block_name);
            cookie.setCookie('id',collection_id);
            window.location.href = "/add";
        },
        edit: function (order, type) {
            var obj = this.textList[order]
            var pos = obj['order'];
            var url = type + '/edit';
            var data = new FormData();
            if (type == 'collection') {
                data.append('collection_id', obj['id']);

                if (this.name != null) {
                    obj['name'] = this.name;
                    data.append('name', this.name);
                }
                if (this.tag != null) {
                    obj['tag'] = this.tag;
                    data.append('tag', this.tag);
                }
            }
            else {
                data.append('collection_id', this.id);
                data.append('block_id', obj['id']);
                if (obj['content'] != null) {
                    data.append('content', obj['content']);
                }
                if(obj['type'] == 'text'){
                var converter = new showdown.Converter();
                obj['html'] = converter.makeHtml(obj['content']);
                }
            }

            Vue.set(this.textList, pos, obj);
            sendRequest(url, data, function () { ; });

            this.name = null;
            this.tag = null;
            this.content = null;
        },
        add_item: function (type) {
            add(type);
        },
        like: function (order) {
            var obj = this.textList[order];
            obj['like']++;
            obj['isLike'] = true;
            Vue.set(this.textList, order, obj);
            var data = new FormData();
            data.append('collection_id', obj['id']);
            data.append('phonenum', phonenum);
            sendRequest('collection/like', data, function () { ; });
        },
        unlike: function (order) {
            var obj = this.textList[order];
            obj['like']--;
            obj['isLike'] = false;
            Vue.set(this.textList, order, obj);
            var data = new FormData();
            data.append('collection_id', obj['id']);
            data.append('phonenum', phonenum);
            sendRequest('collection/unlike', data, function () { ; });
        }
    }
}
)



var recommend = new Vue({
    el: "#recommend",
    data: {
        textList: [],
        id: null,
        name: null,
        tag: null,
        content: null,
    },
    created: function () {
        var url;
        url = "collection/recommend";
        var data = new FormData();
        sendRequest(url, data, function (data) {
            recommend.textList = data.collections;
            checkLike(this);
            
        for (i in recommend.textList) {
            recommend.textList[i]['order'] = i;
        }
        });
    },
    methods: {
        jump_to: function (url, block_name) {
            cookie.setCookie('name',block_name);
            cookie.setCookie('id',null);
            window.location.href = "/add";
        },
        like: function (order) {
            var obj = this.textList[order];
            obj['like']++;
            obj['isLike'] = true;
            Vue.set(this.textList, order, obj);
            var data = new FormData();
            data.append('collection_id', obj['id']);
            data.append('phonenum', phonenum);
            sendRequest('collection/like', data, function () { ; });
        },
        unlike: function (order) {
            var obj = this.textList[order];
            obj['like']--;
            obj['isLike'] = false;
            Vue.set(this.textList, order, obj);
            var data = new FormData();
            data.append('collection_id', obj['id']);
            data.append('phonenum', phonenum);
            sendRequest('collection/unlike', data, function () { ; });
        }
    }
}
)

function CHECK_URL(url) {
    //url= 协议://(ftp的登录信息)[IP|域名](:端口号)(/或?请求参数)
    var strRegex = '^((https|http|ftp)://)?'//(https或http或ftp):// 可有可无
        + '(([\\w_!~*\'()\\.&=+$%-]+: )?[\\w_!~*\'()\\.&=+$%-]+@)?' //ftp的user@  可有可无
        + '(([0-9]{1,3}\\.){3}[0-9]{1,3}' // IP形式的URL- 3位数字.3位数字.3位数字.3位数字
        + '|' // 允许IP和DOMAIN（域名） 
        + '(localhost)|'	//匹配localhost
        + '([\\w_!~*\'()-]+\\.)*' // 域名- 至少一个[英文或数字_!~*\'()-]加上.
        + '\\w+\\.' // 一级域名 -英文或数字  加上.
        + '[a-zA-Z]{1,6})' // 顶级域名- 1-6位英文 
        + '(:[0-9]{1,5})?' // 端口- :80 ,1-5位数字
        + '((/?)|' // url无参数结尾 - 斜杆或这没有
        + '(/[\\w_!~*\'()\\.;?:@&=+$,%#-]+)+/?)$';//请求参数结尾- 英文或数字和[]内的各种字符

    var strRegex1 = '^(?=^.{3,255}$)((http|https|ftp)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(:\d+)*(\/)?(?:\/(.+)\/?$)?(\/\w+\.\w+)*([\?&]\w+=\w*|[\u4e00-\u9fa5]+)*$';
    var re = new RegExp(strRegex, 'i');//i不区分大小写
    console.log(re);
    //将url做uri转码后再匹配，解除请求参数中的中文和空字符影响
    if (re.test(encodeURI(url))) {
        return (true);
    } else {
        return (false);
    }
}

function compile(){
    var list = document.getElementsByClassName("standard-input");

    console.log(list,list.length);
    for(i in page.textList){
        if(page.textList[i]['type']!='text'){
            page.textList[i]['html'] = null;
            continue;
        }
        var text = page.textList[i]['content'];
        console.log(i);
        var converter = new showdown.Converter();
        var html = converter.makeHtml(text);
        page.textList[i]['html'] = html;
    }


}