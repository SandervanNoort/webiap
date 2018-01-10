<?php

$phpDir = '../php';
require "$phpDir/utils.php";
require_all($phpDir);

global $CONFIG;
setConfig("../config");

$page = getCheck("page", array_keys($CONFIG["page"]));

print_head();
print_navigation($page);
if ($page == "results" || $page == "_table") {
   readfile("http://beta.influenzanet.eu/results.php?" . http_build_query($_REQUEST));
} else {
    print_main($page);
}
print_footer();
