<?php

function epibanner()
{
    global $CONFIG;
    echo "<div id='col3' class='col3'>
          <img alt='Epiwork' src='{$CONFIG["settings"]["media"]}/media/base/img/main/epibanner.jpg' /></div>";
}

function clear()
{
    echo "<div style='clear:both'></div>\n";
}

function get($var)
{
    if (isset($_REQUEST[$var])) {
        return $_REQUEST[$var];
    } else {
        return "";
    }
}

function set($var, $value)
{
    if (isset($_REQUEST[$var])) {
        return;
    } else {
        $_REQUEST[$var] = $value;
    }
}
    

function getCheck($var, $options)
{
    $value = get($var);
    if (in_array($value, $options)) {
        return $value;
    } else {
        return $options[0];
    }
}

function getMenu($var, $group="", $compare=True) {
    global $MENU;

    if ($group == "") {
        $group = $var;
    }
    if (get($var) == "compare" && $compare) {
        return "compare";
    } else {
        return getCheck($var, get_options($group));
    }
}

function transMenu($value, $group) 
{
    global $MENU;

    if ($value == "compare") {
        return trans("compare", "website_results");
    }

    if (strstr($value, "__")) {
        list($group, $value) = explode("__", $value);
    }
    
    if (array_key_exists("translate_{$value}", $MENU[$group])) {
        $section = "{$MENU[$group]["translate_{$value}"]}";
    } else {
        $section = "{$MENU[$group]["translate"]}";
    }
    return trans($value, $section);
}


function trans($word, $section="", $empty=False) {
    global $TRANSLATE;

    $lang = "en";

    if (strstr($word, "@")) {
        $casedefs = explode("@", $word);
        $words = array();
        foreach ($casedefs as $casedef) {
            $words[] = trans($casedef, $section, $empty);
        }
        return implode(" vs. ", $words);
    }

    if (strstr($section, "_title")) {
        $section = preg_replace("/_title/", "", $section)."_".$word;
        $word = "title";
    }
    if ($section == "intake") {
        $words = explode("_", $word);
        $word = array_pop($words);
        $section = $section . "_" . implode("_", $words);
    }

    if (strstr($section, "_value")) {
        $sections = explode("_", preg_replace("/_value/", "", $section));
        $word = array_pop($sections);
        $section = implode("_", $sections);
    }

    if ($section == "") {
        $section = "extra";
    }
    $lower = strtolower($word);

    if ($section == "control") {
        $section = "casedef";
    }


    if ($section == "casedef" && strstr($word, "_")) {
        list($column, $lower) = split("_", $lower);
        $section = "survey_{$column}";
    }

    
    if (strstr($section, "_")) {
        list($fname, $section) = explode("_", $section, 2);
    } else {
        $fname = "all";
    }

    if (in_array($fname, array("intake", "survey")) && $lower == "d") {
        list($fname, $section, $lower) = array("all", "extra", "dontknow");
    }
    if (in_array($fname, array("intake", "survey")) && $lower == "n") {
        list($fname, $section, $lower) = array("all", "extra", "none");
    }

    if ($fname == "all" && $section == "season") {
        if ($lower == "all") {
        } else {
            $year1 = $lower;
            $year2 = $year1 + 1;
            return "{$year1} - {$year2}";
        }
    }

    if (array_key_exists($lang, $TRANSLATE)
        && array_key_exists($fname, $TRANSLATE[$lang])
        && array_key_exists($section, $TRANSLATE[$lang][$fname])
        && array_key_exists($lower, $TRANSLATE[$lang][$fname][$section])
        ) {
        if (array_key_exists($lower . "_short",
                 $TRANSLATE[$lang][$fname][$section])) {
            $result =  $TRANSLATE[$lang][$fname][$section][$lower . "_short"];
        } else {
            $result =  $TRANSLATE[$lang][$fname][$section][$lower];
        }
        $result = preg_replace("/\\$\\^\\{(.*)\\}\\$/", "<sup>$1</sup>", 
                $result);
        return $result;
    }

    if ($empty) {
        return "";
    } else {
//         print "<pre>";
//         print "{$lang}:{$fname}:{$section}:{$lower}";
//         print_r($TRANSLATE);
//         print "</pre>";
//         exit();
//         return "{$lang}:{$fname}:{$lower}:{$section}:{$word}";
        return "{$section}:{$word}";
    }
//     return "{$fname} - {$section} - {$lower}";
}


function setConfig($configDir)
{
    global $TRANSLATE, $CONFIG, $MENU;

    $CONFIG = parse_ini_file("$configDir/config.ini", true);
    if (file_exists("$configDir/local.ini") === true) {
        $local  = parse_ini_file("$configDir/local.ini", true);
        $CONFIG = arrayOverlay($CONFIG, $local);
    }
    // $lang = get("lang");

    $TRANSLATE = array();

    $langDir = "{$CONFIG["local"]["data"]}/lang";
    $handle = opendir($langDir);
    while (false !== ($lang = readdir($handle))) {
        if (in_array($lang, array(".", ".."))) {
            continue;
        }
        if (in_array($lang, array("nl", "pt"))) {
            continue;
        }
        if (!array_key_exists($lang, $TRANSLATE)) {
            $TRANSLATE[$lang] = array();
        }
        $handle2 = opendir("$langDir/$lang");
        while (false !== ($fname = readdir($handle2))) {
            if (in_array($fname, array(".", ".."))) {
                continue;
            }
            $base = (explode(".", $fname));
            $base = $base[0];
            $TRANSLATE[$lang][$base] = parse_ini_file(
                    "$langDir/$lang/$fname", true);
        }
    }

    if (file_exists("$configDir/menus_{$lang}.ini") === true) {
        $fname = "$configDir/menus_{$lang}.ini";
    } else {
        $fname = "$configDir/menus.ini";
    }
    $MENU = parse_ini_file($fname, true);
}

function get_options($group, $extra=False) {
    global $MENU;
    foreach (array("options", "extra") as $key) {
        if (array_key_exists($key, $MENU[$group]) &&
                !is_array($MENU[$group][$key])) {
            $values = array();
            foreach (split(", *", $MENU[$group][$key]) as $option) {
                if (substr_compare($option, "__all",
                                   strlen($option)-5, 5) === 0) {
                    $subgroup = substr($option, 0, strlen($option)-5);
                    foreach (get_options($subgroup) as $suboption) {
                        $values[] = "{$subgroup}__{$suboption}";
                    }
                } else {
                    $values[] = $option;
                }
            }
            $MENU[$group][$key] = $values;
        }
    }
    if ($extra && array_key_exists("extra", $MENU[$group])) {
        return array_merge(
             $MENU[$group]["options"],
             $MENU[$group]["extra"]);
    } else {
        return $MENU[$group]["options"];
    }
}

function arrayOverlay($array1, $array2)
{
    foreach ($array1 as $key1 => $value1) {
        if (!array_key_exists($key1, $array2)) {
            continue;
        } elseif (is_array($value1) && is_array($array2[$key1])) {
            $array1[$key1] = arrayOverlay($value1, $array2[$key1]);
        } else {
            $array1[$key1] = $array2[$key1];
        }
    }
    return $array1;
}

function require_all($phpDir)
{
    require "$phpDir/home.php";
    require "$phpDir/results.php";
    require "$phpDir/buttons.php";
    require "$phpDir/data.php";
    require "$phpDir/questions.php";
    require "$phpDir/help.php";
    require "$phpDir/table.php";
    // require "$phpDir/check.php"
    // require "$phpDir/map.php"
}

function print_head() 
{
    global $CONFIG;
    $media = $CONFIG["settings"]["media"];
    echo "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN'
    'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>

    <html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en' dir='ltr'>
    <head> 
    <title>{$CONFIG['home']['title']}</title> 
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8' /> 
    <meta name='viewport' content='initial-scale=0.75, user-scalable=yes' /> 
    <meta name='robots' content='index, follow' /> 
    
    <link rel='shortcut icon' type='image/x-icon' 
        href='$media/media/base/img/favicon.ico' /> 
    <link rel='icon' type='image/x-icon' 
        href='$media/media/base/img/favicon.ico'  /> 
    <link rel='apple-touch-icon' 
        href='$media/media/base/img/apple-touch-icon.png' />      
    
    <meta name='description' content='Influenzanet is a system to
    monitor the activity of influenza-like-illness (ILI) with the aid
    of volunteers via the internet. It has been operational in The
    Netherlands and Belgium (GroteGriepmeting), Portugal (Gripenet),
    Italy (Influweb), and United Kingdom (FluSurvey).' />
    <meta name='keywords' content='influenzanet, influenza, ili,
    internet monitoring, epiwork, grotegriepmeting, gripenet, influweb,
    flusurvey' />
    <meta name='language' content='english' />
    <meta name='author' content='S.P. van Noort' />
    
    <link type='text/css' rel='stylesheet' media='all'
        href='$media/media/base/css/default.css' /> 
    <link type='text/css' rel='stylesheet' media='all'
        href='$media/colors.css' /> 
    <link type='text/css' rel='stylesheet' media='screen'
         href='$media/media/base/js/fancybox/jquery.fancybox-1.3.4.css' />
    <link type='text/css' rel='stylesheet' media='all'
         href='$media/media/sander/dropdown.css' />
    <link type='text/css' rel='stylesheet' media='all'
         href='$media/media/sander/style.css' />
    <link type='text/css' rel='stylesheet' media='all'
         href='$media/media/sander/slides/style.css' />
    
    <script type='text/javascript' 
         src='$media/media/base/js/jquery-1.5.1.min.js'></script>
    <script type='text/javascript' 
         src='$media/media/base/js/fancybox/jquery.fancybox-1.3.4.pack.js'></script>
    <script type='text/javascript' 
         src='$media/media/base/js/fancybox/jquery.mousewheel-3.0.4.pack.js'></script>
    <script type='text/javascript' 
         src='$media/media/sander/slides/slides.js'></script>
    <script type='text/javascript' 
         src='$media/media/sander/fancybox.js'></script>
    <script type='text/javascript' 
         src='$media/media/sander/dropdown.js'></script>
    <script type='text/javascript' 
         src='$media/media/sander/slides.js'></script>
    </head>

    <body>
    <div id='page'>";
}

function print_navigation($page)
{
    global $CONFIG;
    echo "<div class='influenzabar' id='influenzabar'></div>
    <div id='header'>
        <div id='navigation'>
            <div id='menubar'>
                <ul>
    ";

    foreach ($CONFIG['page'] as $key=>$title) {
        if ($key[0] == "_") {
            continue;
        }
        if ($page === $key) {
            $class = 'selected';
        } else {
            $class = 'sibling';
        }
        echo "<li class='$class'>
            <a href='?page=$key'>$title</a></li>\n";
    }
    echo "</ul>"; // end ul-menu
    echo "</div>"; // end menubar
    echo "</div>"; // end naviation
    echo "</div>"; // end header
}

function print_footer() {
    echo "<div id='footer'>
            <div id='footerclose'>
                &copy; 2012 Influenzanet &nbsp;|&nbsp;
                <a href='?page=home' title='Contact us'>Contact</a>
            </div>
        </div>

        </div>
        </body>
        </html>";
}

function print_main($page)
{
    echo "<div id='main'>";
    if ($page === 'home') {
        home();
    } else if ($page === 'results') {
        results();
    } else if ($page === 'data') {
        data();
    } else if ($page === 'questions') {
        questions();
    } else if ($page === 'help') {
        help();
    } else if ($page === '_vac') {
        echo "<div id='col1-left'><div id='col1' class='col1'>\n";
        include "vac/index.html";
        echo "</div></div>";
    } else if ($page === '_vac2') {
        echo "<div id='col1-left'><div id='col1' class='col1'>\n";
        include "vac/oddr.html";
        echo "</div></div>";
    } else if ($page === '_map') {
        echo "<div id='col1-left'><div id='col1' class='col1'>\n";
        include "maps/index.html";
        echo "</div></div>";
    } else if ($page === '_forum') {
        echo "<div id='col1-left'><div id='col1' class='col1'>\n";
        include "forum.html";
        echo "</div></div>";
    } else if ($page === '_table') {
//         echo "<div id='col1-left'><div id='col1' class='col1'>\n";
        show_table();
//         echo "</div></div>";
    } else if ($page === '_vac2') {
//     } else if ($page === '_forum') {
//         echo "<div id='col1-left'><div id='col1' class='col1'>\n";
//         include "forum.html";
//         echo "</div></div>";
    }

    clear();
    echo "</div>"; // end main
}
