<html>
<body>

<form action="index.php" method="post">
    Username : <input type="text" name="username"><br>
    Password : <input type="password" name="password"><br>
    <input type="submit" value="Submit">
</form>

<?php
if (!empty($_POST["username"]))
{
    $username=$_POST["username"];
    $password=$_POST["password"];
    if ($username=="mahmood" && $password=="12345")
    {
        echo "<p>Successfull</p>";
    }
    else
    {
        echo "<p>Failed</p>";
    }
}
?>
</body>
</html>