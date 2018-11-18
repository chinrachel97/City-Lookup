<?php
  $cmdArgs = "";

  // check if there was any user input
  if(isset($_POST["userInputs"])){
    $input = $_POST["userInputs"];
    $cmdArgs = implode(" ", $input);
  }

  // call the python script to get recommendations
  $command = escapeshellcmd('python test.py '.$cmdArgs);
  $output = shell_exec($command);
  if(shell_exec($command)){
    echo $output;
  }
  else{
    echo 'ERROR: cannot execute Python script.';
  }
?>
