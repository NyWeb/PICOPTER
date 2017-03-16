loader.level.dom.push(function(){pilot.initialize()});
ajax.draw.push(function(w){return pilot.fetch(w)});
var pilot = {
    json: {plugin: false, parameter: false},
    lock: false,
    cache: {response: false, error: false},
    id: 0,

    initialize: function() {
        pilot.action();

        // If we have a pilot object
        if(q('#wrapper')) {
            setTimeout(pilot.image, 100);

            setInterval(pilot.read, 100);
        }
    },

    read: function() {
        //Push JSON data to server
        if(!pilot.lock) {
            pilot.lock = true;

            string = "";
            if(pilot.json) {
                var string = JSON.stringify(pilot.json);
            }

            ajax.go("/log/log.json");

            pilot.cache.response = setTimeout(pilot.error, 1500, "WiFi not connecting");

            pilot.json = false
        }
    },

    fetch: function(w) {
        //Reset JSON data so it's not sent again
        pilot.lock = false;

        //Remove timer
        clearTimeout(pilot.cache.response);

        try {
            var log = JSON.parse(w);
        }

        catch(err) {
            pilot.error("connect-error: WIFI not connecting");
            //We couldn't connect with drone
            return "nolink";
        }

        //Log all error messages
        for(var error in log["error"]) if(log["error"].hasOwnProperty(error)) for(var type in log["error"][error]) if(log["error"][error].hasOwnProperty(type)) {
            pilot.error(error+"-"+type+": "+log["error"][error][type]);
        }

        //Go through all sensor data
        for(var key in log["sensor"]) {
            if(log["sensor"].hasOwnProperty(key)) {
                if(sensor[key]) sensor[key](log["sensor"][key]);
            }
        }

        //Go through all plugin data
        for(key in log["plugin"]) {
            if(log["plugin"].hasOwnProperty(key)) {
                //If we get a true result, we should set the controllers to match that
                if(plugin[key]) plugin[key](log["plugin"][key]);
            }
        }

        return "nolink";
    },

    action: function() {
        var actions = q('.action');
        for(var i=0; i<actions.length; i++) {
            if(v(actions[i], "photo")) actions[i].onclick = function(){};
        }
    },

    image: function(error) {
        if(v(q('.stream')[0], "active")) {
            var image = new Image();
            image.onload = function() {
                var left = q('.photo', q('#vanster'))[0];
                var right = q('.photo', q('#hoger'))[0];

                left.src = image.src;
                right.src = image.src;

                setTimeout(pilot.image, error?0:70);

                pilot.id++;
                if(pilot.id==2) {
                    pilot.id = 0;
                }
            };

            image.onerror = function() {
                pilot.image(true);
            };

            image.src = "/tmp/image"+(pilot.id)+".jpg?"+Math.round(Math.random()*1000);
        }
        else {
            setTimeout(pilot.image, 10);
        }
    },

    error: function(msg) {
        if(msg&&msg!=pilot.cache.error) {
            console.log(msg);

            var holder = document.createElement("a");
            holder.innerHTML = msg;

            q('#error').appendChild(holder);

            setTimeout(function(){q('#error').removeChild(q('a', q('#error'))[0]); pilot.cache.error = false;}, 2000);

            pilot.cache.error = msg;
        }
    }
};

var plugin = {
    control: function(log) {
        if(!log) return;

        pilot.adjust({
            left: {
                x: log['motor']["jaw"],
                y: log['motor']["throttle"]
            },
            right: {
                x: log['motor']["roll"],
                y: log['motor']["pitch"]
            }
        });
    },

    arm: function(log) {
        if(!log&&v(q('body')[0], 'arm')) {
            q('body')[0].className = q('body')[0].className.replace("arm", "");
        }

        if(log&&!v(q('body')[0], 'arm')) {
            q('body')[0].className += " arm";
        }
    }
};

var sensor = {
    location: function(values) {
        q('.distance', q('#header'))[0].innerHTML = values["distance"];
        q('.latitude', q('#header'))[0].innerHTML = values["latitude"];
        q('.longitude', q('#header'))[0].innerHTML = values["longitude"];
        q('.altitude', q('#header'))[0].innerHTML = values["altitude"];
    }
};