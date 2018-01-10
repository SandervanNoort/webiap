<?php

function check()
{
    global $menus;
    $base = "http://beta.influenzanet.info/index.php?";
    $uri  = "http://validator.w3.org/check?ss=1";
    echo "<ul>";
    foreach (array_keys($menus["page"]) as $page) {
        echo "<li><a href='$uri&amp;uri=".urlencode($base."page={$page}")
            ."'>$page</a></li>";
        if (in_array($page, array_keys($menus))) {
            echo "<ul>";
            foreach (array_keys($menus[$page]) as $subpage) {
                echo "<li><a href='$uri&amp;uri="
                    .urlencode($base."page={$page}&{$page}={$subpage}")
                    ."'>$page - $subpage</a></li>";
            }
            echo "</ul>";
        }
        if ($page == "publications") {
            echo "<ul>";
            echo "<li><a href='$uri&amp;uri="
                .urlencode($base."page={$page}&abstract=marquet2006")
                ."'>$page - Marquet</a></li>";
            echo "</ul>";
        }
    }
    echo "</ul>";
}
