<?php
  $cmdArgs = "";

  // check if there was any user input
  if(isset($_POST["userInputs"])){
    $input = $_POST["userInputs"];

    // add double quotes around the inputs to preserve double words (in-place op)
    // don't change the last arg; it is already formatted
    for($i=0; $i<count($input)-1; ++$i){
      $input[$i] = "'".$input[$i][0].",".$input[$i][1]."'";
    }

    // join all the elements in the arr with a space
    $cmdArgs = implode(" ", $input);
  }

  // call the python script to get recommendations
  $command = escapeshellcmd('python modifiedPearsonAndCosine.py '.$cmdArgs);
  $output = shell_exec($command);
  if(shell_exec($command)){
    echo $output;
  }
  else{
    echo 'ERROR: cannot execute Python script.';
  }
?>
