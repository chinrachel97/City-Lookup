<?php
  // call the python script to get recommendations
  $command = escapeshellcmd('python test.py');
  $output = shell_exec($command);
  if(shell_exec($command)){
    echo $output;
  }
  else{
    echo 'ERROR: cannot execute Python script.';
  }
?>
