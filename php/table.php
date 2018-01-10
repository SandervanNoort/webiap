<?php

function csv_to_table($local_csv) {
    $fobj = fopen($local_csv, "r");
    $active = True;
    while ($active) {
        $active = show_csv_table($fobj);
    }
    fclose($fobj);
}

function show_csv_table($fobj) {
    // create a html-table for non-empty lines of fobj
    // return False if end of file reached
    $header = True;
    $col0_header = False;
    while (($line = fgetcsv($fobj)) !== false) {
        if (count($line) == 1 && $line[0] == "") {
            if (!$header) {
                echo "</table>\n\n";
            }
            return True;
        }
        if ($header) {
            echo "<table border='1' class='grey' style='margin-top: 1em'>\n";
        }
        echo "<tr align='right'>";
        foreach ($line as $no => $cell) {
            if ($header) {
                echo "<th>" . htmlspecialchars($cell) . "</th>";
                if ($no == 0 && in_array($cell,
                        array("", "Attack rate", "Pie diagram"))) {
                    $col0_header = True;
                }
            } else {
                if ($no == 0 and $col0_header) {
                    echo "<th>" . htmlspecialchars($cell) . "</th>";
                } else {
                    echo "<td>" . htmlspecialchars($cell) . "</td>";
                }
            }
        }
        echo "</tr>\n";
        $header = False;
    }
    return False;
}

function show_table() {
    // show table based on $_REQUEST["csv"]
    global $CONFIG;
    if (!array_key_exists("ini", $_REQUEST)) {
        echo "No ini key defined";
        return;
    }
    $ini = $_REQUEST["ini"];
    $local_csv = "{$CONFIG["local"]["csv"]}/$ini.csv";
    $public_csv = "{$CONFIG["public"]["csv"]}/$ini.csv";
    if (!file_exists($local_csv)) {
        echo "No csv for ini {$ini}";
        return;
    }

    echo "<p><a href='javascript: history.go(-1)'>Back</a></p>\n";
    if (array_key_exists("map", $_REQUEST)) {
        echo map($ini);
    } else {
        $local_img_big = "{$CONFIG["local"]["png"]}/{$ini}_big.png";
        $local_img = "{$CONFIG["local"]["png"]}/{$ini}.png";
        if (file_exists($local_img_big)) {
            $public_img_big = "{$CONFIG["public"]["png"]}/{$ini}_big.png";
            echo "<img src='$public_img_big' />";
        } else if (file_exists($local_img)) {
            $public_img = "{$CONFIG["public"]["png"]}/{$ini}.png";
            echo "<img src='$public_img' />";
        }
    }
    echo "<p style='clear:both'><a href='{$public_csv}'>Download csv</a></p>\n";
    csv_to_table($local_csv);
}

?>
