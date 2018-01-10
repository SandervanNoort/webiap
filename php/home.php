<?php

function home()
{
    global $MENU, $CONFIG;
    // latest_table();
    echo "<div id='col1-left'><div id='col1' class='col1'>\n";


    echo "<h1>{$CONFIG["home"]["title"]}</h1>";
    echo "{$CONFIG["home"]["description"]}";
    @include "{$CONFIG["local"]["html"]}/influenzanet.html";

    echo "<h3 style='clear: both'>Links</h3>\n";
    logolink("http://www.grotegriepmeting.nl", "griepmeting.jpg",
             "griepmeting", "Netherlands / Belgium");
    logolink("http://www.gripenet.pt", "gripenet.gif", "gripenet", "Portugal");
    logolink("http://www.influweb.it", "influweb.gif", "Influweb", "Italy");
    logolink("http://www.flusurvey.org.uk", "flusurvey.gif", "flusurvey",
            "United Kingdom");

    logolink("http://www.gripenet.com.br", "gripenetbr.png", "Gripenet Brasil",
            "Brasil");
    logolink("http://www.flutracking.net", "flutracking.jpg", "FluTracking",
            "Australia");
    logolink("http://reporta.c3.org.mx/", "reporta.jpg", "Mexico", "Mexico");
    logolink("http://grippemontreal.qc.ca/", "grippem.gif", "Montreal",
            "Montreal");
    logolink("http://www.denguenaweb.ufba.br/", "denguenaweb.jpg",
            "DenguenaWeb", "Salvador (Dengue)");
    
    logolink("http://www.epiwork.eu/", "epiwork.png", "Epiwork");
    logolink($CONFIG["urls"]["eiss"], "ecdc.jpg", "ECDC", "");
    logolink($CONFIG["urls"]["google"], "google.gif", "Google Flu Trends",
            "Flu Trends");
    //     <!-- http://aegislablogin.appspot.com/html/AegisCloud.html' -->
    logolink("http://aegis.chip.org/pages/software-flu", "aegis.gif", "Aegis",
            "Massachusetts");
    logolink("http://websenti.b3e.jussieu.fr/sentiweb/", "sentinelles.gif",
            "sentiweb", "France");

    echo "</div></div>"; // end col1-left, col1
    epibanner();
}

function logolink($href, $src, $alt, $caption="")
{
    global $MENU, $CONFIG;
    echo "<div class='logolink'>
        <a {$CONFIG["settings"]["target"]} href='$href'>
        <img src='images/logo/scaled/$src' alt='$alt'/>";
    if ($caption != "") {
        echo "<br />$caption\n";
    }
    echo "</a></div>\n";
}
