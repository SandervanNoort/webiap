<?php

function help() 
{
    global $CONFIG;
    $files  = array("casedef", "active", "incidence", "real", "age", "attack"
            ,"plots", "extra", "casedef2");
    $regexp = "<h2\s[^>]*id=([\"\']??)([^\"\' >]*?)\\1[^>]*>(.*)<\/h2>";
    $contents = array();

    echo "<div id='col1-left'><div id='col1' class='col1'>";
    echo "<h1 id='top'>Help</h1>";
    echo "<ul class='list'>";
    foreach ($files as $file) {
        $input = @file_get_contents("{$CONFIG["local"]["html"]}/$file.html");
        if (!$input) {
            continue;
        }
        $contents[] = $input;
        if (preg_match_all("/$regexp/siU", $input, $matches)) {
            for ($i=0;$i<count($matches[2]);$i++) {
                echo "<li><a href='#{$matches[2][$i]}'
                        >{$matches[3][$i]}</a></li>";
            }
        }
    }
    echo "</ul>";

    foreach ($contents as $content) {
        echo $content; 
        echo "<p><a href='#top'>Back to top</a></p>";
        // include "{$CONFIG["local"]["html"]}/$file.html";
    }
    echo "</div></div>"; // end col1-left, col1
    epibanner();
}
