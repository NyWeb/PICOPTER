<ul class="app-style">
	<?php
		foreach(array("arm", "photo", "video", "slowmotion", "home", "emergency", "library", "sensor", "wifi") as $action):
			?>
				<li class="<?=$action?>">
					<a class="action <?=$action?>"></a>
				</li>
			<?php
		endforeach;
	?>
</ul>