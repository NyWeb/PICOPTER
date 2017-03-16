<?php

namespace picopter\controller;

use picopter\helper, picopter\model;

class pilot {
	function onepilot() {
		helper::render("pilot", "one", false);
	}

	function savepilot() {
		//Save command
		if($_REQUEST['json']) {
			$error = 0;

			//If pilot hasn't deleted the file
			while(file_exists(helper::$commandfile)) {
				usleep(100000);
				//return error
				if($error++>10) die('{"error":{"pilot": {"message": "pilot not active"}}, "sensor":{}, "plugin":{}}');
			}

			if($_REQUEST['json']) file_put_contents(helper::$commandfile, urldecode($_REQUEST['json']));
		}

		echo file_get_contents(helper::$logfile);
		unlink(helper::$logfile);
	}
}