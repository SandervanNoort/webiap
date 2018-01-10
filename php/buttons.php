<?php

function buttonDropdown($title, $items, $hrefs) {
    return buttonsDropdown(array($title => $items), array($title => $hrefs));
}


function buttonsDropdown($allItems, $allHrefs) {
    $output = "<ul class='nav'>";

    foreach ($allItems as $title => $items) {
        $hrefs = $allHrefs[$title];
        $output .= "<li class='dropdown'>";
        if (count($items) > 1) {
            $output .= "<a>{$title} &gt;</a>
                        <ul><li>\n";
        }
        for ($i = 0; $i < count($items); $i++) {
            $name = htmlspecialchars($items[$i]);
            $href = htmlentities($hrefs[$i]);
            if (substr($name, 0, 2) === "__") {
                $name = substr($name, 2);
                $target = "target = '_blank'";
            }
            else {
                $target = "";
            }
            $output .= "<a href='{$href}' {$target}>{$name}</a>";
        }
        if (count($items) > 1) {
            $output .= "</li></ul>";
        }
        echo "</li>\n";
    }
    $output .= "</ul>\n";
    return $output;
}


function buttonOption($title, $items, $hrefs, $selected) {
    $output = "<ul class='nav' style='clear: both'>
                <li class='option'><a>{$title} &gt;</a>
                <ul><li>\n";
    $count  = count($items);
    for ($i = 0; $i < $count; $i++) {
        if ($items[$i] === $selected) {
            $class = "class='selected' ";
        } else {
            $class = '';
        }

        $output .= "<a href='".htmlentities($hrefs[$i])."'
                  $class>{$items[$i]}</a>\n";
    }

    $output .= "</li></ul></li>\n";
    $output .= "<li class='value'>$selected</li>\n";
    $output .= "</ul>
        <div style='clear: both'>&nbsp;</div>\n";
    return $output;
}
