<?php

function questions() {
    echo "<div id='col1-left'><div id='col1' class='col1'>
        <h1>Questionnaires</h1>
        <ul class='list'>
        <li><a href='#intake'>Intake questionnaire</a></li>
        <li><a href='#survey'>Weekly symptoms questionnaire</a></li>
        </ul>";

    echo "<h2 id='intake'>Intake questionnaire</h2>
        <p>
        At the beginning of each season, each participant is
        required to complete an intake questionnaire once.
        Not all questions and answers are presented in every season.
        Some questions have the extra possible answers
        'Other' (o), 'Don't know' (d) and/or 'None' (n).
        </p>
        ";
    echo make_table("intake");

    echo "<h2 id='survey'>Weekly symptoms' questionnaire</h2>
        <p>
        Every participant is reminded weekly to complete a
        symptoms questionnaire. The final questions are only
        asked if the participant reported any symptoms.
        Not all questions were present in every country
        or season.
        </p>";
    echo make_table("survey");
    echo "</div></div>"; // end col1-left, col1
    epibanner();
}

function make_table($table, $caption="") {
    global $CONFIG, $TRANSLATE;

    $ini = parse_ini_file("{$CONFIG["local"]["data"]}/{$table}.ini",
             true);
    $res = "<table class='grey-left'>
        <caption>$caption</caption>
        <thead>
        <tr>
            <th>Column</th>
            <th>Question</th>
            <th>Answers</th>
        </tr>
        </thead>
        <tbody>
         ";


    foreach ($ini as $column=>$values) {
        if (!is_array($values))
            continue;
        if ($values["type"] == "options")
            continue;
//         if (array_key_exists("src", $values))
//             continue;
//
        $title = trans("title", "{$table}_{$column}");
        $res .= "<tr>
            <th>$column</th>
            <td>$title</td>
        ";
        $res .= "<td>";
        if (in_array($column, array_keys($TRANSLATE["en"][$table]))) {
            foreach (array_keys($TRANSLATE["en"][$table][$column]) as $answer) {
                if (in_array($answer, array("title", "question"))) {
                    continue;
                }
                if ($answer != "" && substr($answer, -6) == "_short") {
                    continue;
                }
                $val = str_pad($answer, 3, " ", STR_PAD_LEFT);
                $val = str_replace(" ", "&nbsp;", $val);
                    //$label
                $res .= "$val. " 
                        . htmlentities(trans($answer, "{$table}_{$column}")) 
                        . " <br />";
            }
        }
        $res .= "</td>\n";
        $res .= "</tr>\n";
    }
    $res .= "</tbody></table>\n";
    return $res;
}
