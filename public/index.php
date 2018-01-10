<?php

$phpDir = '../php';
require "$phpDir/utils.php";
require_all($phpDir);

global $CONFIG;
setConfig("../config");
// $CONFIG["settings"]["debug"] = True;

$page = getCheck("page", array_keys($CONFIG["page"]));

// if ($page == "_table") {
//     print_head();
//     print_navigation($page);
//     show_table();
//     print_footer();
//     exit();
// }

print_head();
print_navigation($page);
print_main($page);
print_footer();
