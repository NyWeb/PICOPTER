var loader = {
    run: 0,
    level: {listen:[], dom:[function(){setTimeout(function(){q('body')[0].className += " loaded";}, 10)}], load:[]},

    initialize: function (level) {
        var i;

        if(1==1) {
            for (i = 0; i < loader.level.listen.length; i++) loader.level.listen[i]();
            loader.level.listen = [];
        }
        if(level=="dom"||level=="load") {
            for (i = 0; i < loader.level.dom.length; i++) loader.level.dom[i]();
            loader.level.dom = [];
        }
        if(level=="load") {
            for (i = 0; i < loader.level.load.length; i++) loader.level.load[i]();
            loader.level.load = [];
        }

        loader.run = level;
    },

    domready: function () {
        if (document.readyState === "complete") {
            setTimeout(function(){loader.initialize('load')}, 1);
        }

        if (document.addEventListener) {
            document.addEventListener("DOMContentLoaded", loader.checkstate, false);
            window.addEventListener("load", function(){loader.initialize('load')}, false);
        }

        else if (document.attachEvent) {
            document.attachEvent("onReadyStateChange", loader.checkstate);
            window.attachEvent("onload", function(){loader.initialize('load')});
        }
    },

    checkstate: function () {
        if (document.addEventListener) {
            document.removeEventListener("DOMContentLoaded", loader.checkstate, false);
            loader.initialize('load');
        }

        else if (document.attachEvent) {
            if (document.readyState === "complete") {
                document.detachEvent("onReadyStateChange", loader.checkstate);
                loader.initialize('load');
            }
        }
    },

    legacy: function (a, d) {
        d = document;
        b = d.createStyleSheet();

        d.querySelectorAll = function (r, c, i, j, a) {
            a = d.all;
            c = [];
            r = r.replace(/\[for\b/gi, '[htmlFor').split(',');

            for (i = r.length; i--;) {
                b.addRule(r[i], 'k:v');
                for (j = a.length; j--;) {
                    if (a[j].currentStyle.k) c.push(a[j]);
                }
                b.removeRule(0);
            }
            return c;
        };
    }
};

loader.level.dom.push(function(){ajax.initialize();});
var ajax = {
    object: null,
    url: '',
    draw: [],
    caller: false,
    initialize: function () {
        if (window.XMLHttpRequest) ajax.object = new XMLHttpRequest();
        else if (window.ActiveXObject) ajax.object = new ActiveXObject("Microsoft.XMLHTTP");
        for (var i = 0; i < q('.ajax').length; i++) {
            q('.ajax')[i].onclick = function () {
                ajax.go(this.href + '?&format=raw');
                return false;
            };
        }
    },

    go: function (url) {
        q('body')[0].className = q('body')[0].className.replace(" loaded", '');
        ajax.url = url;
        if (ajax.object.length === 0) ajax.initialize();
        ajax.object.open("GET", url, true);
        ajax.object.onreadystatechange = function(){ajax.execute();};
        ajax.object.send(null);
    },

    execute: function () {
        if (ajax.object.readyState != 4) return;
        q('body')[0].className = q('body')[0].className.replace('loaded', "")+" loaded";
        updatelink = true;
        for(var i = ajax.draw.length - 1; i > 0; i--) {
            if (ajax.draw[i](ajax.object.responseText) == "nolink") updatelink = false;
        }
    }
};

/* DOM query selector string in object */
function q(a, d) {
    if (!d) d = document;
    if (d && !d.querySelectorAll) loader.legacy(a, d);
    switch (a.substr(0, 1)) {
        case "#":
            return d.getElementById(a.substr(1));
        case ".":
            return d.querySelectorAll(a);
        case "-":
            return d.getElementsByName(a.substr(1));
        default:
            return d.getElementsByTagName(a);
    }
}

/* Classname has substring */
function v(z, g) {
    return z.className.indexOf(g) != -1;
}

/*Create element*/
function g(tag, cname, inner, url, src, click, type, hover) {
    /*var e = document.createElement(tag);
     if(cname) e.className = cname;
     if(inner) e.innerHTML = inner;
     if(url) e.href = url;
     if(src) e.src = src;
     if(click) e.onclick = click;
     if(hover) e.onmouseover = hover;
     if(type) e.type = type;
     return e;*/
}

/*Get DOMREADY*/
loader.domready();