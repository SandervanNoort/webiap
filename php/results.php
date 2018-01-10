<?php

function map($realname)
{
    // make a map
    global $CONFIG;
    $local_dir = "{$CONFIG["local"]["map"]}/$realname";
    $public_dir = "{$CONFIG["public"]["map"]}/$realname";

    if (!is_dir($local_dir)) {
        return false;
    }
    $output = "";

    $width = 370;
    $height = $width;
    foreach (scandir($local_dir) as $imgname) {
        $info = pathinfo($imgname);
        if (array_key_exists("extension", $info) &&
                 in_array($info["extension"],
                          array("png", "jpg", "jpeg", "gif"))) {
            $output .= "<img src='$public_dir/$imgname' 
                    width='$width' height='$height' 
                    alt='The Netherlands / Belgium'/>";
        }
    }
    $output = "<div id='slides'>$output</div>";
    $output = "<div id='container' style='clear:both'>
        $output
        <a href='#' id='control' class='controls'>Play</a>
        </div>";

    $hrefs = array();
    $items = array();

    $csvname = "{$CONFIG["public"]["csv"]}/{$realname}.csv";
    $ininame = "{$CONFIG["public"]["ini"]}/{$realname}.ini";
    $hrefs["Download"] = array("$public_dir/movie.mp4", $csvname, $ininame);
    $items["Download"] = array("Movie", "__CSV", "__Ini");

    $hrefs["Data"] = array("?page=_table&ini=$realname&map=1");
    $items["Data"] = array("Data");

    if (count($items) > 0) {
        $buttons = buttonsDropdown($items, $hrefs);
        $output  = "<div style='float: right; padding-right: 50px'
                    >$buttons</div>
                    <div style='clear:both'>$output</div>";
    }


    $output = "<div class='diagram'>$output</div>";
    return $output;
}

function has_key($figname, $key) {
    if (is_array($figname)) {
        $has = False;
        foreach ($figname as $subfigname) {
            $has = $has || has_key($subfigname, $key);
        }
        return $has;
    }
    if (strpos($figname, "{{$key}}") === False) {
        return False;
    } else {
        return True;
    }
}

function get_fignames($vars) {
    global $MENU;
    $fignames = array();
    $all_vars = array();

    foreach(array("country", "season", "casedef") as $var) {
        if ($vars[$var] == "compare") {
            foreach (get_options($var, True) as $vars[$var]) {
                $fignames[] = get_figname($vars);
                $all_vars[] = $vars;
            }
            return array($fignames, $all_vars);
        }
    }
    foreach (get_options($vars["group"]) as $vars["type"]) {
        $fignames[] = get_figname($vars);
        $all_vars[] = $vars;
    }
    return array($fignames, $all_vars);
}

function results_first() {
    // show the first results page, with links
 
    global $MENU, $CONFIG;
 
    $vars = array("casedef" => "ilit",
            "group" => "overview",
            "type" => "disease_base__ili",
            "lang" => "en",
            "country" => "compare");

    echo "<div id='col1-left'><div id='col1' class='col1'>";
    echo "<h1>".trans("inet", "source"). " Results </h1>\n";
    echo trans("results", "website_description", True);
    echo "<div class='results'>";

    foreach (get_options("country") as $vars["country"]) {
        foreach (get_options("season") as $vars["season"]) {
            $figname = get_figname($vars);
            $basename = get_realname($figname, $vars);
            $ini = "{$CONFIG["local"]["ini"]}/{$basename}.ini";
            if (file_exists($ini)) {
                $href = "?page=results";
                foreach ($vars as $key=>$value) {
                    $href .= "&{$key}={$value}";
                }
                echo img($vars, $figname, $href, false);
                break;
            }
        }
    }

    clear();
    echo "</div>"; // end results
    echo "</div></div>"; // end col1-left, col1
    epibanner();
}
 
function results() 
{
    global $MENU, $CONFIG;

    if (get("group") == "") {
        results_first();
        return;
    }

    $group = getMenu("group");
    $vars = array("group" => $group,
            "country" => getMenu("country"),
            "season" => getMenu("season"),
            "casedef" => getMenu("casedef"),
            "lang" => getMenu("lang"),
            "type" => getMenu("type", $group));

    list($fignames, $all_figvars) = get_fignames($vars);
    $has_casedef = has_key($fignames, "casedef");


    // unset casedef compare, if no fignames with casedef
    if (!$has_casedef && $vars["casedef"] == "compare") {
        $vars["casedef"] = getMenu("casedef", "", False);
        list($fignames, $all_figvars) = get_fignames($vars);
        $has_casedef = has_key($fignames, "casedef");
    }

    $group_name = transMenu($vars["group"], "group");
    $season_name = transMenu($vars["season"], "season");
    $country_name = transMenu($vars["country"], "country");
    $type_name = transmenu($vars["type"], $vars["group"]);

    if ($vars["lang"] != "en") {
        foreach (array("public", "local") as $dir) {
            foreach (array("ini", "png", "csv", "pdf", "map") as $ftype) {
                $CONFIG[$dir][$ftype] .= "_{$vars["lang"]}";
            }
        }
    }

    // left column
    echo "<div id='col2' class='col2'>\n";
    echo "<p class='title' style='margin-bottom: 1em'>Options</p>\n";
    $compare = ($vars["country"] == "compare"
                || $vars["season"] == "compare"
                || $vars["casedef"] == "compare");

    foreach (array("country", "season", "group", "type", "casedef") as $var) {
        // NO LANGUAGE FOR THE MOMENT

        // no type menu for non-comparisons
        if ($var == "type" && !$compare) {
            continue;
        }
        // No case definition menu for symptoms/participants
        if (!$has_casedef && $var == "casedef") {
            continue;
        }

        if ($var == "type") {
            $title = trans($vars["group"], "website_group");
        } else {
            $title = trans($var, "website_results");
        }

        list($items, $hrefs, $selected) = getMenuLinks($var, $vars);
        echo buttonOption($title, $items, $hrefs, $selected);
    }
    clear();
    echo "<p class='title'>Help</p>\n";
    echo "<p><a {$CONFIG["settings"]["target"]} href='?page=help#casedef'
            >ILI case definitions</a></p>
       <p><a {$CONFIG["settings"]["target"]} href='?page=help#activity'
            >Activity calculation</a></p>
       <p><a {$CONFIG["settings"]["target"]} href='?page=help#active'
            >Active participants</a></p>
       <p><a {$CONFIG["settings"]["target"]} href='?page=help#plots'
            >Plots</a></p>
    ";
    echo "</div>"; // end col2

    //right column
    echo "<div id='col1-right'><div id='col1' class='col1'>";

    if (count($fignames) > 0) {
        $all = trans("all", "website_results");
        if ($vars["country"] == "compare") {
            $countries = trans("countries", "website_results");
            $title = "$season_name ($all $countries) - $type_name";
        } elseif ($vars["season"] == "compare") {
            $seasons = trans("seasons", "website_results");
            $title = "$country_name ($all $seasons) - $type_name";
        } elseif ($vars["casedef"] == "compare") {
            $casedefs = trans("casedefs", "website_results");
            $title = "$all $casedefs<br/> 
                    $country_name ($season_name) - $type_name";
        } else {
            $title = "$country_name ($season_name) - $group_name";
        }
        echo "<h1>$title</h1>";
        echo "<p>
              Some results are password protected. Please
              <a href=\"https://www.influenzanet.eu/en/contact/\"
              >contact us</a> on how to obtain access.
              </p>";
        echo trans($vars["group"], "website_description", True);
        echo "<div class='results'>\n";
        foreach ($fignames as $key=>$figname) {
            echo img($all_figvars[$key], $figname, "", true);
        }
        clear();
        echo "</div>\n"; // end results
    } else {
        echo "<h1>No results</h1>";
    }

    echo "<p style='clear: both; float: right'>\n";
    echo "Sources: <a href='?page=data'>Influenzanet</a>, 
            <a {$CONFIG["settings"]["target"]}
                href='{$CONFIG["urls"]["google"]}'>Google Flu Trends</a>,
            <a {$CONFIG["settings"]["target"]}
                href='{$CONFIG["urls"]["eiss"]}'>EISN</a>,
            <a {$CONFIG["settings"]["target"]}
                href='{$CONFIG["urls"]["noaa"]}'>NOAA</a>.";
    echo "</p>";

    echo "</div></div>"; // end col1-right, col1
}

function getMenuLinks($var, $vars, $show_all=False)
{
    global $MENU, $CONFIG;

    if ($var == "type") {
        $group = $vars["group"];
    } else {
        $group = $var;
    }
    $selected = transMenu($vars[$var], $group);

    $href = "?page=results";
    foreach ($vars as $key=>$value) {
        if ($key != $var) {
            $href .= "&{$key}={$value}";
        }
    }

    $hrefs = array();
    $items = array();
    foreach (get_options($group) as $vars[$var]) {
        if ($var == "group") {
            // Always show group
            $figs = true;
        } else {
            if ($vars["season"] == "all") {
                $figs = true;
            } else {
                list($fignames, $figvars) = get_fignames($vars);
                $figs = has_images($fignames, $figvars);
            }
        }
        if ($figs || $show_all) {
            $hrefs[] = "{$href}&{$var}={$vars[$var]}";
            $items[] = transMenu($vars[$var], $group);
        }
    }
    return array($items, $hrefs, $selected);
}

function get_figname($vars) 
{
    global $MENU, $CONFIG;

    if (strstr($vars["type"], "__")) {
        list($group, $type) = explode("__", $vars["type"]);
    } else {
        list($group, $type) = array($vars["group"], $vars["type"]);
    }

    if ($vars["season"] == "all" &&
            array_key_exists("figname_{$type}_all", $MENU[$group])) {
        $figname = $MENU[$group]["figname_{$type}_all"];
    } elseif (array_key_exists("figname_{$type}", $MENU[$group])) {
        $figname = $MENU[$group]["figname_{$type}"];
    } elseif ($vars["season"] == "all" &&
            array_key_exists("figname_all", $MENU[$group])) {
        $figname = $MENU[$group]["figname_all"];
    } elseif (array_key_exists("figname", $MENU[$group])) {
        $figname = $MENU[$group]["figname"];
    } else {
        return "ERROR";
    }

    return $figname;
}

function get_realname($figname, $vars) {
    return preg_replace_callback("/{(.*?)}/", 
            function($var) use ($vars) {
                if ($var[1] == "type" && strstr($vars["type"], "__")) {
                    $vals = explode("__", $vars["type"]);
                    return $vals[1];
                } elseif ($var[1] == "country" && $vars["type"] == "map"
                        && $vars["country"] == "be") {
                    return "nl";
                } elseif ($var[1] == "cold") {
                    return "cold".substr($vars["casedef"], 3);
                } elseif ($var[1] == "gastro") {
                    return "gastro".substr($vars["casedef"], 3);
                } elseif ($var[1] == "allergy") {
                    return "allergy".substr($vars["casedef"], 3);
                } else {
                    return $vars[$var[1]]; 
                }
            },
            $figname);
}

function has_images($fignames, $figvars) {
    // whether one of the images is available
    global $CONFIG;

    // First check just the basic images
    foreach ($fignames as $key=>$figname) {
        $basename = get_realname($figname, $figvars[$key]);
        $ini = "{$CONFIG["local"]["ini"]}/{$basename}.ini";
        if (file_exists($ini)) {
            return True;
        }
    }
    return false;

    // next check the more complicated images $base_<answer>
    foreach ($fignames as $figname) {
        $basename = get_realname($figname, $vars);
        $inis = glob("{$CONFIG["local"]["ini"]}/{$basename}*.ini");
        foreach ($inis as $ini) {
            $realname = substr($ini, strlen($CONFIG["local"]["ini"]) + 1, -4);
            if (substr($realname, -4) == "_big") {
                continue;
            }
            if ($realname != $basename &&
                $realname[strlen($basename)] != "_") {
                # do not catch s100_10.ini with s100_1.ini
                continue;
            }
            return True;
        }
    }

    // No valid image found
    return False;
}
    

function img($vars, $figname, $href="", $links=false)
{
    global $CONFIG;

    $basename = get_realname($figname, $vars);
    $inis = glob("{$CONFIG["local"]["ini"]}/{$basename}*.ini");
    if (count($inis) == 0) {
        if ($CONFIG["settings"]["debug"]) {
            if ($href != "") {
                return "<a href='{$href}'>{$basename}</a><br />";
            } else {
                return $basename . "<br />";
            }
        }
        return "";
    }

    $images = array();
    foreach ($inis as $ini) {
        $realname = substr($ini, strlen($CONFIG["local"]["ini"]) + 1, -4);
        if (substr($realname, -4) == "_big") {
            continue;
        }
        if ($realname != $basename &&
            $realname[strlen($basename)] != "_") {
            # do not catch s100_10.ini with s100_1.ini
            continue;
        }
        $images[] = img_ini($vars, $figname, $realname, $href, $links);
    }
    return implode("\n", $images);
}

function img_ini($vars, $figname, $realname, $href, $links) {
    global $MENU, $CONFIG;


    if ($vars["type"] == "map") {
        return map($realname);
    }
    $ini = "{$CONFIG["local"]["ini"]}/{$realname}.ini";
    $ini_big = "{$CONFIG["local"]["ini"]}/{$realname}_big.ini";
    $title   = trans($vars["country"], "country") . " " 
            . trans($vars["season"], "season") 
            . " " . transMenu($vars["type"], $vars["group"]);

    if ($CONFIG["settings"]["mtime"]) {
        $mtime = "?mtime="
            . filemtime("{$CONFIG["local"]["png"]}/{$realname}.png");
    } else {
        $mtime = "";
    }
    $output = "<img src='{$CONFIG["public"]["png"]}/{$realname}.png{$mtime}'
            alt='$title' />";
    if ($href != "") {
        $output = "<a href='$href'>" . $output . "</a>";
    } elseif (file_exists($ini_big)) {
        if ($CONFIG["settings"]["mtime"]) {
            $mtime = "?mtime="
                . filemtime("{$CONFIG["local"]["png"]}/{$realname}_big.png");
        } else {
            $mtime = "";
        }
        $output = "<a rel='group1' class='group' 
                href='{$CONFIG["public"]["png"]}/{$realname}_big.png{$mtime}'
                title='$title'>$output</a>";
    }
    if ($links) {
        $hrefs = array();
        $items = array();

        if ($CONFIG["settings"]["download"]) {
            $hrefs["Download"] = array(
                "{$CONFIG["public"]["csv"]}/{$realname}.csv",
                "{$CONFIG["public"]["csv"]}/{$realname}_big.csv",
                "{$CONFIG["public"]["pdf"]}/{$realname}.pdf",
                "{$CONFIG["public"]["pdf"]}/{$realname}_big.pdf",
                "{$CONFIG["public"]["ini"]}/{$realname}.ini",
                "{$CONFIG["public"]["ini"]}/{$realname}_big.ini");
            $large = trans("large", "website_results");
            $items["Download"] = array("__CSV", "__CSV ($large)",
                    "PDF", "PDF ($large)", "__INI" ,"__INI ($large)");
        }

        if ($CONFIG["settings"]["compare"]) {
            $compare = trans("compare", "website_results");
            $hrefs[$compare]   = array();
            $items[$compare]   = array(); 

            $hrefs[$compare][] = "?page=results&country=compare"
                      . "&season={$vars["season"]}"
                      . "&casedef={$vars["casedef"]}"
                      . "&type={$vars["type"]}"
                      . "&group={$vars["group"]}"
                      . "&lang={$vars["lang"]}";
            $items[$compare][] = trans("countries", "website_results");

            $hrefs[$compare][] = "?page=results&season=compare"
                      . "&country={$vars["country"]}"
                      . "&casedef={$vars["casedef"]}"
                      . "&type={$vars["type"]}"
                      . "&group={$vars["group"]}"
                      . "&lang={$vars["lang"]}";
            $items[$compare][] = trans("seasons", "website_results");

            if (has_key($figname, "casedef")) {
                $hrefs[$compare][] = "?page=results&casedef=compare"
                      . "&country={$vars["country"]}"
                      . "&season={$vars["season"]}"
                      . "&type={$vars["type"]}"
                      . "&group={$vars["group"]}"
                      . "&lang={$vars["lang"]}";
                $items[$compare][] = trans("casedefs", "website_results");
            }
        }
        $hrefs["Data"]   = array();
        $items["Data"]   = array(); 
        $hrefs["Data"][] = "?page=_table&ini=$realname";
        $items["Data"][] = "Data";

        if (count($items) > 0) {
            $buttons = buttonsDropdown($items, $hrefs);
            $output  = "<div style='float: right'>$buttons</div>
                       <div style='clear:both'>$output</div>";
        }
    }
    $output = "<div class='diagram'>". $output ."</div>\n";
    return $output;
}
