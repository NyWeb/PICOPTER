<?php

namespace picopter\model;

class file {
	static function getfilebyname($name, $folder) {
		return file_get_contents($folder."/".$name);
	}

	static function savefile($name, $content, $folder, $type = 0) {
		if($type==0) {
			file_put_contents($folder."/".$name, $content);
		}
	}
}