<?php
session_start();

  // Set the download headers for the second file

  header('Content-Type: application/octet-stream');
  header('Content-Disposition: attachment; filename="205_High_enc.txt"');

  // Output the contents of the second file
  readfile('205_High_enc.txt');


  exit;
	
?>