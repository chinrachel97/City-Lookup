<?php
  // call the python script to get recommendations
  $input = $_POST["userInputs"];
  $cmdArgs = implode(" ", $input);
  $command = escapeshellcmd('python test.py '.$cmdArgs);
  $output = shell_exec($command);
  if(shell_exec($command)){
    echo $output;
  }
  else{
    echo 'ERROR: cannot execute Python script.';
  }
?>
