<?php

function timeseries($countries)
{
    global $MENU, $CONFIG;

    $links = array();
    foreach ($countries as $country) {
        $local = "{$CONFIG["local"]["download"]}/$country/" .
                 "incidence/{$country}_all.csv";
        if (file_exists($local)) {
            $public = "{$CONFIG["public"]["download"]}/$country/" .
                      "incidence/{$country}_all.csv";
            $country_name = trans($country, "country");
            $links[] = "<a href='$public'>$country_name</a>";
        }
    }
    if (count($links) == 0) {
        return "";
    }

    $result = "
    <h2>ILI time series</h2>
    <p>
    Files which list per country for every week
    the number of active participants and the number of ILI onsets, for up
    to four different ILI case definitions. These files can be used to
    create ILI incidence curves.
    </p>
    <p><b>Download:</b> " . implode(",\n", $links) . "</p>";

    return $result;
}

function geographical($countries)
{
    global $MENU, $CONFIG;

    $links = array();
    foreach ($countries as $country) {
        $local = "{$CONFIG["local"]["download"]}/{$country}/geo";
        if (file_exists($local)) {
            $public = "{$CONFIG["public"]["download"]}/{$country}/geo";
            $country_name = trans($country, "country");
            $links[] = "<a href='$public'>$country_name</a>";
        }
    }
    if (count($links) == 0) {
        return "";
    }

    $result = "
    <h2>Geographical spread</h2>
    <p>
    Files which list for each week,
    the total number of active participants and the number of ILI onsets
    are listed, grouped by (abbreviated) postal code of the participants.
    These files can be used to create maps to visualize the geographical
    spread of ILI.
    </p>
    <p><b>Download:</b> " . implode(",\n", $links) . "</p>";

    return $result;
}

function converted($countries)
{
    // return info on converted data sets
    global $MENU, $CONFIG;

    $links = array();
    foreach ($countries as $country) {
        $local_dir = "{$CONFIG["local"]["download"]}/$country/converted";
        if (file_exists($local_dir)) {
            $public_dir = "{$CONFIG["public"]["download"]}/$country/converted";
            $country_name = trans($country, "country");
            $links[] = "<a href='$public_dir'>$country_name</a>";
        }
    }
    if (count($links) == 0) {
        return "";
    }

    $result = "
    <h2>Full data sets (unified)</h2>
    <p>
    Files containing the full data set for each country,
    including all
    <a href='https://results.influenzanet.eu/?page=questions#intake'>Intake
    questions</a>
    and all
    <a href='https://results.influenzanet.eu/?page=questions#survey'>Weekly
    symptoms' questions</a>. The data is converted from the
    <a href='#orig'>Original data</a>, such that each country and
    season uses the same column names and values.
    This data is <a href='#restricted'>password protected</a>.
    </p>
    <p><b>Download:</b> " . implode(",\n", $links) . "</p>";

    return $result;
}

function orig($countries)
{
    // return info on converted data sets
    global $MENU, $CONFIG;

    $links = array();
    foreach ($countries as $country) {
        $local_dir = "{$CONFIG["local"]["download"]}/$country/orig";
        if (file_exists($local_dir)) {
            $public_dir = "{$CONFIG["public"]["download"]}/$country/orig";
            $country_name = trans($country, "country");
            $links[] = "<a href='$public_dir'>$country_name</a>";
        }
    }
    if (count($links) == 0) {
        return "";
    }

    $result = "
    <h2 id='orig'>Full data sets (original)</h2>
    <p>
    Files containing the full data set for each country, in the original
    database format. The database format has changed over the seasons and
    could differ per country. Since season 2011/12, all Influenzanet countries
    use the same database format. If only data since 2011/12 is required,
    it is probably better to use these original data sets, whereas if also
    data from before 2011/12 is needed, it is more convenient to download the
    <a href='#converted'>Unified data sets</a>.
    This data is <a href='#restricted'>password protected</a>.
    </p>
    <p><b>Download:</b> " . implode(",\n", $links) . "</p>";

    return $result;
}

function other() {
    // return info on other sources
    global $CONFIG;

    return "
    <h2>Other sources</h2>
    <p>
    Influenzanet uses data from various other sources.
    </p>
    <ul>
        <li><a {$CONFIG["settings"]["target"]}
            href='{$CONFIG["urls"]["eiss"]}'
            >ECDC</a>: 
            European Influenza Surveillance Network.
        </li>
        <li><a {$CONFIG["settings"]["target"]}
            href='{$CONFIG["urls"]["google"]}'
            >Google Flu Trends</a>:
            ILI activity derived from Google search volumes.
        </li>
        <li><a {$CONFIG["settings"]["target"]}
            href='{$CONFIG["urls"]["noaa"]}'
            >NOAA</a>: 
            National Oceanic and Atmospheric Administration.
        </li>
        <li><a {$CONFIG["settings"]["target"]}
            href='http://www.geonames.org'
            >GeoNames</a>:
            Geographical coordinates of postal codes.
        </li>
        <li><a {$CONFIG["settings"]["target"]}
            href='http://web.hku.hk/~bcowling/influenza/HK_NPI_study.htm'
            >Hong Kong NPI study</a>:
            ILI symptoms and viral confirmation in household study.
        </li>
    </ul>";
}

function restricted() {
    // return info on gaining access to unrestricted data
    $result = "
    <h2 id='restricted'>Restricted access</h2>
    <p>
    To obtain access to the more detailed Influenzanet data, please
    <a href='https://www.influenzanet.eu/en/contact/'>contact
    the national organisers</a> of the Influenzanet systems. Any
    privacy sensitive information, such as email-addresses, will never be
    shared with third parties.
    </p>

    <p>
    For scientists and researches who wishes to analyse data from
    multiple countries, please fill in the
    <a href='files/110627-Data_ApplicationForm.pdf'>Data Application Form</a>.
    Your application is subject to approval from the Influenzanet
    Science Committee, which aims to react within short notice to your
    request.
    </p>
    ";
    return $result;
}

function source() 
{
    $links = array();
    if (is_dir("results/source")) {
        foreach (scandir("results/source") as $fname) {
            if ($fname == "." || $fname == "..") {
                continue;
            }
            $links[] = "<a href='results/source/$fname'>$fname</a>";
        }
    }
    if (count($links) == 0) {
        return "";
    }
    $result = "
        <h2>Source code</h2>
        <p>
        You can download all the source code which is used to
        generate the results.
        </p>

        <p><b>Download:</b> " . implode(",\n", $links) . "</p>";

    return $result;
}



function data() 
{
    global $MENU, $CONFIG;

    echo "
    <div id='col1-left'><div id='col1' class='col1'>
    <h1>Data</h1>
    <p>
    When using these data please attribute it to Influenzanet as 
    follows:<br />
    <b>\"Data Source: Influenzanet (http://www.influenzanet.eu)\"</b>.
    </p>
    ";
    
    # $fnames = scandir($CONFIG["local"]["download"]);
    $countries = split(", *", $MENU["country"]["options"]);
    echo timeseries($countries);
    echo geographical($countries);
    echo converted($countries);
    echo orig($countries);

    echo restricted();
    echo other();
    echo source();

    echo "</div></div>"; // end col1-left, col1
    epibanner();
}
