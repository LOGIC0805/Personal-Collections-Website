
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
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
            console.log(this);
        }
    });
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

function getBlock() {
    var url = "block/select";
    var data = new FormData();
    data.append("collection_id",id);
    sendRequest(url, data,
        function (data) {
            var list = $("#textList");
            var blocks = data.blocks;
            for (i in blocks) {
                var content;
                var block = blocks[i];
                if (block.type == 'img') {
                    content = document.createElement('img');
                    content.src = block.content;
                }
                else if (block.type == 'text') {
                    content = document.createElement('div');
                    content.innerText = block.content;
                }
                else {
                    content = document.createElement('div');
                    content.innerText = block.content;
                }
                content.id = block.id;
                var block = gengerate_block(content,"block");
                list.append(block);
            }
        });
}

function submit(obj, content, type, order) {
    var url = "http://127.0.0.1:5000/block/add";
    var data = new FormData();
    data.append("content", content);
    data.append('type', type);
    data.append('order', order);
    var that = obj;
    $.ajax({
        type: "post",
        url: url,
        data: data,
        dataType: "json",
        processData: false,
        contentType: false,
        success: function (data) {
            that.id = data.id;
        },

        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
            console.log(this);
        }
    });
}

function swap(obj, dir,type) {
    var url;
    if (type == "block") {
        url = "block/swap";
    }
    else {
        url = "collection/swap";
    }
    var pos = obj.parentNode.id;
    if (dir == 'up' && pos > 0) {
        pos--;

    }
    if (dir == 'down' && dir < $("#textList").childElementCount - 1) {
        pos++;
    }
    var data = new FormData();
    data.append("new_order", pos);
    data.append("id", obj.id);
    if (type == "block") {
        sendRequest(url, data, getBlock);    
    }
    else{
        sendRequest(url, data, getCollection);
    }
    
}
function delete_block(obj,type) {
    var url;
    var data = new FormData();
    data.append("collection_id", id);
    if (type == "block") {
        data.append("block_id", obj.id);
        url = "block/delete";
    }
    else {
        url = "collection/delete";
    }
    
    sendRequest(url, data, function () { ;});
    
}
function gengerate_block(content,type) {
    var obj = document.createElement("div");
    obj.className = "standard-input";
    obj.id = document.getElementById('textList').childElementCount;
    var up = document.createElement("div");
    up.addEventListener("click", function () { swap(content, 'up',type); });
    up.innerText = "swap up";
    obj.appendChild(up);
    obj.appendChild(content);
    var down = document.createElement("div");
    down.addEventListener("click", function () { swap(content, 'down',type) });
    down.innerText = "swap down";
    obj.appendChild(down);
    var delete_item = document.createElement("div");
    delete_item.addEventListener("click", function () { delete_block(content,type); });
    delete_item.innerText = "delete";
    obj.appendChild(delete_item);
    return obj;
}

function add(type) {
    var text = $("#myInput").val();
    $("#myInput").val("");
    if (text == "") {
        return;
    }
    let div = document.createElement('div');
    div.innerText = text;
    var block = gengerate_block(div,type)
    $('#textList').append(block);
    var data = new FormData();
    data.append('type', 'text');
    data.append('name', text);
    data.append('order', block.id);
    data.append('content', text);

    var url;

    if (type == 'block') {
        data.append('collection_id');
        url = "block/add";
    }
    else {
        url = "collection/add";
    }

    sendRequest(url,data,function (data) {
        div.id = data.id;
    })
}


function getCollection() {
    var url = "collection/select";
    var data = new FormData();
    if ("undefined" != typeof phonenum) {
        data.append('phonenum',phonenum);    
    }
    
    var name = $("#search").val();
    if(name != ""){
        data.append('name',name);
    }
    $("#textList").children().remove();
    sendRequest(url, data, function (data) {
        console.log(data);
        var list = $("#textList");
        var collections = data.collections;
        for (i in collections) {
            var content = document.createElement('div');
            var collection = collections[i];
            content.innerText = collection.name;
            content.onclick = function () {
                console.log("?");
                window.location.href = "add.html?id=" + collection.id + "&name=" + collection.name;
            };
            content.className = "standard-box";
            content.id = collection.id;
            $('#textList').append(gengerate_block(content,"collection"));
        }
    });
}