<?php

function contact() {
    $cols    = 50;
    $rows    = 5;
    $name    = get("name");
    $email   = get("email");
    $comment = get("comment");

    if ($comment != "") {
        if ($name == "") {
            $name = "Anonymous";
        }

        $msg = "Name: $name\n"
            . "Email: $email\n\n"
            . "$comment";
        mail("sander.van.noort@gmail.com",
                "Influenzanet.info comment",
                $msg,
                "From: Influenzanet <Sander.van.Noort@gmail.com>\r\n");

        echo "<h2>Thanks for sending your comment</h2>
            <p>The following comment has been delivered:</p>
            <p>
            <b>$name</b>($email)
            <blockquote><i>".nl2br($comment)."</i></blockquote>
            </p>
            ";
    } else {
        echo "<h2>Contact information</h2>
    
            <p>
            <b>Influenzanet analyses</b><br/>
            Sander van Noort <br/>
            Sander.van.Noort [at] gmail.com
            </p>
        
            <p>
            <b>The Netherlands and Belgium</b><br/>
            Project leader: Carl Koppeschaar <br/>
            <a href='http://www.degrotegriepmeting.nl/public/index.php?thisarticle=128'>Organisers Grote Griepmeting</a><br/>
            pr [at] grotegriepmeting.nl
            </p>
            
            <p>
            <b>Portugal</b> <br/>
            Project leader: Vitor Faustino <br/>
            <a href='http://www.gripenet.pt/index.php?option=com_content&amp;task=view&amp;id=18&amp;Itemid=33'>Organisers Gripenet</a><br/>
            info [at] gripenet.pt
            </p>
            
            <p>
            <b>Italy</b> <br/>
            Project leaders: Vittoria Collizza and Daniela Paolotti<br/>
            <a href='http://www.influweb.it/index.php?option=com_content&amp;task=view&amp;id=125&amp;Itemid=199'>Organisers InfluWeb</a><br/>
            info [at] influweb.it
            </p>
        
            <p>
            <b>United Kingdom</b><br />
            Project leader: John Edmunds<br />
            <a href='http://www.flusurvey.org.uk/index.php?option=com_content&amp;task=view&amp;id=306&amp;Itemid=33'>Organizers FluSurvey</a><br />
            webmaster [at] flusurvey.org.uk
            </p>
    
            <h3>Leave a comment</h3>
            <div>
            <form action='index.php'>
            <div>
            <input type='hidden' name='page' value='contact' />
            <table>
            <tr>
                <th>Name</th>
                <td><input size='$cols' name='name' 
                    value='$name' /></td>
            </tr>
            <tr>
                <th>Email</th>
                <td><input size='$cols' value='$email'
                    name='email' /></td>
            </tr>
            <tr>
                <th>Message</th>
                <td><textarea cols='$cols' rows='$rows' name='comment'
                    ></textarea></td>
            </tr>
            <tr><td colspan='2' style='text-align: right'>
                <input name='submit' type='submit' value='Send' />
            </td></tr>
            </table>
            </div>
            </form>
            </div>
        ";
    }
}
