<?php

$phpDir = '../php';
require "$phpDir/utils.php";
require_all($phpDir);

global $CONFIG;
setConfig("../config");

$CONFIG["public"]["png"] = "/media/uploads/results/png";
$CONFIG["public"]["map"] = "/media/uploads/results/map";
$CONFIG["public"]["csv"] = "http://results.influenzanet.eu/results/csv";
$CONFIG["public"]["ini"] = "http://results.influenzanet.eu/results/ini";
$CONFIG["public"]["pdf"] = "http://results.influenzanet.eu/results/pdf";

$CONFIG["settings"]["media"]  = "http://results.influenzanet.eu/eu";

$page = getCheck("page", array_keys($CONFIG["page"]));
if ($page != "help" && $page != "_vac" && $page != "_vac2" && $page != "results") {
    $page = "results";
}

set("season", "2012");

// print_head();
// print_navigation($page);
print_main($page);
// print_footer();
