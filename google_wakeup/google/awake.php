<?php
if(isset($_GET['play']) && !empty($_GET['play'])){

    if ( $_GET['play'] == " with music"){
		system('sudo /home/brenden/Tools/wowlan/php_awake 1');
	}
	else {
		system('sudo /home/brenden/Tools/wowlan/php_awake');
	}
} else {
    system('sudo /home/brenden/Tools/wowlan/php_awake');
}

?>

