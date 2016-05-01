loader.level.dom.push(function(){pilot.initialize()});
ajax.draw.push(function(w){return pilot.fetch(w)});
loader.level.listen.push(function(){window.addEventListener("keydown", keylogger.go, false)});
var pilot = {
    json: {plugin: false, parameter: false},
    lock: false,
    command: {left: {x: 50, y: 0}, right: {x: 50, y: 50}},

    initialize: function() {
        pilot.action();

        // If we have a pilot object
        if(q('#pilot')) {
            // Disable default behaviours
            document.addEventListener("touchmove", function(e){e.preventDefault()}, false);

            var touch = q('.touches');
            for(var i=0; i<touch.length; i++) {
                touch[i].addEventListener("touchmove", function(e){pilot.draw(e, this)}, false);
                touch[i].addEventListener("touchdown", function(e){pilot.draw(e, this)}, false);
                touch[i].addEventListener("touchup", function(){pilot.reset(this)}, false);
            }

            var images = q('.background');
            for(i=0; i<images.length; i++) {
                images[i].onload = function(){pilot.image(this);};
                pilot.image(images[i]);
            }

            setInterval(pilot.push, 100);
        }
    },

    push: function() {
        //Push JSON data to server
        if(!pilot.lock) {
            pilot.lock = true;

            string = "";
            if(pilot.json) {
                var string = JSON.stringify(pilot.json);
            }

            ajax.go("/?view=savepilot&json="+string+"&format=raw");

            pilot.json = false
        }
    },

    fetch: function(w) {
        try {
            var log = JSON.parse(w);
        }

        catch(err) {
            pilot.lock = false;
            return "nolink";
        }

        //Reset JSON data so it's not sent again
        pilot.lock = false;

        //Log all error messages
        for(var error in log["error"]) if(log["error"].hasOwnProperty(error)) for(var type in log["error"][error]) if(log["error"][error].hasOwnProperty(type)) console.log(error+"-"+type+": "+log["error"][error][type])

        //Go through all sensor data
        for(var key in log["sensor"]) {
            if(log["sensor"].hasOwnProperty(key)) {
                if(plugin[key]) plugin[key](log["sensor"][key]);
            }
        }

        //Go through all plugin data
        for(key in log["plugin"]) {
            if(log["plugin"].hasOwnProperty(key)) {
                //If we get a true result, we should set the controllers to match that
                if(log["plugin"][key]) {
                    pilot.adjust({
                        left: {
                            x: log["plugin"][key]["jaw"],
                            y: log["plugin"][key]["throttle"]
                        },
                        right: {
                            x: log["plugin"][key]["roll"],
                            y: log["plugin"][key]["pitch"]
                        }
                    });
                }
            }
        }

        return "nolink";
    },

    set: function(params) {
        //Make sure everything is actually read
        if(pilot.json) setTimeout(pilot.set, 100, params);

        //Set params
        else pilot.json = params
    },

    action: function() {
        var actions = q('.action');
        for(var i=0; i<actions.length; i++) {
            if(v(actions[i], "arm")) actions[i].onclick = function(){
                pilot.set({plugin: "arm", parameter: false});
                if(v(this, "active")) this.className = this.className.replace("active", "");
                else this.className += " active";
            };

            if(v(actions[i], "photo")) actions[i].onclick = function(){pilot.set({plugin: "camera", parameter: "photo"})};

            if(v(actions[i], "slowmotion")) actions[i].onclick = function(){
                pilot.set({plugin: "camera", parameter: "slowmotion"});
                if(v(this, "active")) this.className = this.className.replace("active", "");
                else this.className += " active";
            };

            if(v(actions[i], "video")) actions[i].onclick = function(){
                pilot.set({plugin: "camera", parameter: "video"});
                if(v(this, "active")) this.className = this.className.replace("active", "");
                else this.className += " active";

            };

            if(v(actions[i], "library")) actions[i].onclick = function(){
                if(v(this, "active")) this.className = this.className.replace("active", "");
                else this.className += " active";

            };

            if(v(actions[i], "emergency")) actions[i].onclick = function(){
                if(v(this, "active")) this.className = this.className.replace("active", "");
                else this.className += " active";

            };

            if(v(actions[i], "home")) actions[i].onclick = function(){
                if(v(this, "active")) this.className = this.className.replace("active", "");
                else this.className += " active";

            };

            if(v(actions[i], "wifi")) actions[i].onclick = function(){
                if(v(this, "active")) this.className = this.className.replace("active", "");
                else this.className += " active";

            };

            if(v(actions[i], "sensor")) actions[i].onclick = function(){
                if(v(this, "active")) this.className = this.className.replace("active", "");
                else this.className += " active";

            };
        }
    },

    draw: function(e, w) {
        e.preventDefault();

        //Fetch elements positions
        var left = Math.round(((e.targetTouches[0].pageX-w.offsetLeft)/(w.offsetWidth))*100);
        var bottom = 100-Math.round((e.targetTouches[0].pageY/w.offsetHeight)*100);

        //Set values to reasonable results
        left = Math.min(left, 100);
        bottom = Math.min(bottom, 100);
        left = Math.max(left, 0);
        bottom = Math.max(bottom, 0);

        //Set left if left, right if right
        if(v(w, "left")) pilot.command["left"] = {x: left, y: bottom};
        else if(v(w, "right")) pilot.command["right"] = {x: left, y: bottom}

        //Set the JSON value
        pilot.set({plugin: "control", parameter: pilot.command});

        //Design accordingly
        pilot.adjust(pilot.command);
    },

    reset: function(w) {
        //Set left if left, right if right
        if(v(w, "left")) pilot.command["left"] = {x: 50, y: 0};
        else if(v(w, "right")) pilot.command["right"] = {x: 50, y: 50};

        //Set the JSON value
        pilot.set({plugin: "control", command: pilot.command});

        //Design accordingly
        pilot.adjust(pilot.command);
    },

    adjust: function(command) {
        // Set knob position
        q('.knob', q('.left')[0])[0].style.left = command['left']['x']+"%";
        q('.knob', q('.left')[0])[0].style.bottom = command['left']['y']+"%";
        q('.knob', q('.right')[0])[0].style.left = command['right']['x']+"%";
        q('.knob', q('.right')[0])[0].style.bottom = command['right']['y']+"%";
    },

    image: function(w) {
        var bg = q('.background');
        for(var i=0; i<bg.length; i++) {
            bg[i].className = bg[i].className.replace('active', '');
            if(bg[i]!=w) {
                var url = bg[i].src.split("?");
                bg[i].src = url[0]+"?"+Math.round(Math.random()*1000);
            }
        }
        w.className += ' active';
    }
};

loader.level.dom.push(function(){stl.initialize()});
var stl = {
    render: null,
    camera: false,
    target: false,
    scene: false,
    object: false,

    initialize: function() {
        var container = q('.stl')[0];

        //Set camera position
        stl.camera = new THREE.PerspectiveCamera(35, 1, 1, 15);
        stl.camera.position.set(0, 3, 0);
        //stl.camera.rotate(0, 0, 0);

        //Set camera-target
        stl.target = new THREE.Vector3(0, 0, 0);

        //Set scene
        stl.scene = new THREE.Scene();

        //Add mesh
        stl.mesh();

        //Set lights
        stl.scene.add(new THREE.HemisphereLight( 0x443333, 0x111122 ));
        stl.light( 1, 1, 1, 0xffffff, 1.35 );
        stl.light( 0.5, 1, -1, 0xffaa00, 1 );

        //Create renderer
        stl.render = new THREE.WebGLRenderer({antialias: true, alpha: true});
        stl.render.setPixelRatio( window.devicePixelRatio);
        stl.render.setSize(container.offsetWidth, container.offsetHeight);

        //Basic design-points
        stl.render.gammaInput = true;
        stl.render.gammaOutput = true;
        stl.render.shadowMap.enabled = true;
        stl.render.shadowMap.cullFace = THREE.CullFaceBack;

        //Add element to DOM
        container.appendChild(stl.render.domElement);

        setTimeout(stl.animate, 1000);
    },

    animate: function(){
        requestAnimationFrame(
            function(){
                stl.camera.lookAt(stl.target);
                stl.render.render(stl.scene, stl.camera);
            }
        );
    },

    light: function(x, y, z, color, intensity) {

        var directionalLight = new THREE.DirectionalLight( color, intensity );
        directionalLight.position.set( x, y, z );

        stl.scene.add(directionalLight);
        directionalLight.castShadow = true;

        var d = 1;
        directionalLight.shadowCameraLeft = -d;
        directionalLight.shadowCameraRight = d;
        directionalLight.shadowCameraTop = d;
        directionalLight.shadowCameraBottom = -d;
        directionalLight.shadowCameraNear = 1;
        directionalLight.shadowCameraFar = 4;
        directionalLight.shadowMapWidth = 1024;
        directionalLight.shadowMapHeight = 1024;
        directionalLight.shadowBias = -0.005;
    },

    mesh: function() {
        var loader = new THREE.STLLoader();
        loader.load(
            'picopter.stl',
            function(geometry) {
                var mesh = new THREE.Mesh(geometry, new THREE.MeshPhongMaterial({color:0xEEEEEE,specular:0x000000,shininess:0}));

                mesh.position.set( 0, 0, 0);
                mesh.rotation.set( 0, 0, 0 );
                mesh.scale.set(.005, .005, .005);
                mesh.receiveShadow = true;

                stl.object = stl.scene.add(mesh);
            }
        );
    },

    rotate: function(x, y, z) {
        stl.object.rotation.set(x, y, z);

        stl.camera.lookAt(stl.target);
        stl.render.render(stl.scene, stl.camera);
    }
};

var plugin = {
    accelerometer: function(values) {
        stl.rotate(values['x']*Math.PI/180, values['y']*Math.PI/180, values['z']*Math.PI/180);
        stl.animate();
    },

    location: function(values) {
        q('.distance', q('#header'))[0].innerHTML = values["distance"];
        q('.latitude', q('#header'))[0].innerHTML = values["latitude"];
        q('.longitude', q('#header'))[0].innerHTML = values["longitude"];
        q('.altitude', q('#header'))[0].innerHTML = values["altitude"];
    }
};