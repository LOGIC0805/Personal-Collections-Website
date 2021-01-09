
var url_prefix = "http://127.0.0.1:5000/";
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
        submit(content, 'text');
        page.content = null;
        return;
    }
    if (name == null) {
        return;
    }
    var data = new FormData();
    data.append('name', name);
    data.append('tag', tag);
    sendRequest('collection/add', data, function () {
        getContent('collection');
    });
    page.content = null;
    page.name = null;
    page.tag = null;
}


function submit(content, type,order) {
    var url = "block/add";
    var data = new FormData();
    data.append("content", content);
    data.append('type', type);
    data.append('order', order);
    sendRequest(url,data,function () {
        getContent('block');
    })
}


function getContent(type) {
    var url;
    url = type+"/select";
    var data = new FormData();
    if ("undefined" != typeof phonenum) {
        data.append('phonenum',phonenum);    
    }
    
    var name = $("#search").val();
    if(name != ""){
        data.append('name',name);
    }
    sendRequest(url, data, function (data) {
        if (type == 'collection') {
            page.textList = data.collections;
        }
        else {
            page.textList = data.blocks;
        }
        for (i in page.textList) {
            page.textList[i]['order'] = i;
            if (type == 'block' && page.textList[i]['type'] == 'picture') {
                page.textList[i]['content'] = get_url(page.textList[i]['content']);
            }

        }
        checkLike();
    });
}

async function checkLike() {
    for (i in page.textList) {
        (function (i) {
            var dt = new FormData();
            var obj = page.textList[i];
            dt.append('collection_id', obj['id']);
            sendRequest('collection/isLike', dt, function (data) {
                obj['isLike'] = data.isLike;
                Vue.set(page.textList, obj['order'], obj);
            });
        })(i);
        
    }
}
function get_url(f) {
    let reader = new FileReader();
    reader.readAsDataURL(f);
    reader.onload = function(e) {
        return e.target.result;
    };
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
        swap: function (obj_id, dir,type) {
            var url = type+'/swap';
            
            var obj = this.textList[obj_id];
            var pos = obj_id;
            var origin_pos = pos;
            if (dir == 'up' && pos > 0) {
                pos--;
            }
            if (dir == 'down' && pos < this.textList.length-1) {
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
            if (type == "block") {
                sendRequest(url, data, getBlock);    
            }
            else{
                sendRequest(url, data, getCollection);
            }
            
        },
        delete_item: function(order,type) {
            var url;
            var data = new FormData();
            data.append("collection_id", this.id);
            console.log(order);
            if (type == "block") {
                data.append("block_id", this.textList[order]['id']);
                url = "block/delete";
            }
            else {
                url = "collection/delete";
            }
            this.textList.splice(this.textList[order], 1);
            sendRequest(url, data, function () { ;});
            
        },
        jump_to: function (url,block_name,collection_id) {
            window.location.href = url+"?name="+block_name+"&id="+collection_id;
        },
        edit: function (order,type) {
            var obj = this.textList[order]
            var pos = obj['order'];
            var url = type + '/update';
            var data = new FormData();
            if (type == 'collection') {
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
                if (this.content != null) {
                    obj['content'] = this.content;
                    data.append('content', this.content);
                }
            }
            
            Vue.set(this.textList, pos, obj);
            sendRequest(url, data, function () { ; });

            this.name = null;
            this.tag = null;
            this.content = null;
        },
        add_item:function (type) {
            add(type);
        },
        like: function (order) {
            var obj = this.textList[order];
            obj['like']++;
            obj['isLike'] = true;
            Vue.set(this.textList, order, obj);
            var data = new FormData();
            data.append('collection_id', obj['id']);
            sendRequest('collection/like', data, function () { ; });
        },
        unlike: function (order) {
            var obj = this.textList[order];
            obj['like']--;
            obj['isLike'] = false;
            Vue.set(this.textList, order, obj);
            var data = new FormData();
            data.append('collection_id', obj['id']);
            sendRequest('collection/unlike', data, function () { ; });
        }
    }
}
)
