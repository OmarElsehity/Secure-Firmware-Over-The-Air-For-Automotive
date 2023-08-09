<?php
session_start();
$flag=1;
// Check if the login form has been submitted

if (isset($_POST['login'])) {
  // Get the username and password from the form
  $username = $_POST['username'];
  $password = $_POST['password'];

  // Validate the username and password (you can add your own validation rules here)
  if ($username === 'admin' && $password === 'password') {
    // Authentication successful - set session variables
    $_SESSION['loggedin'] = true;
    $_SESSION['username'] = $username;

    // Redirect to the dashboard or any other protected page
    header('Location: mydashboard2.php');
    exit;
  } else {
    // Authentication failed - show error message
    $error = 'Invalid username or password';
  }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Swift Act SFOTA</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f7f7f7;
    }
    
    h1 {
      font-size: 36px;
      font-weight: bold;
      color: #333;
      margin-top: 50px;
      margin-bottom: 20px;
      text-align: center;
    }
    
    img {
      display: block;
      margin: 0 auto;
      border: 5px solid #fff;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    }
    
    p {
      font-size: 18px;
      color: #666;
      margin-top: 20px;
      margin-bottom: 0;
      text-align: center;
    }
    
    a {
      color: #0099ff;
      text-decoration: none;
    }
    
    a:hover {
      text-decoration: underline;
    }

    /* Style the tab */
    .tab {
      overflow: hidden;
      border: 1px solid #ccc;
      background-color: #f1f1f1;
    }

    /* Style the buttons inside the tab */
    .tab button {
      background-color: inherit;
      float: right;
      border: none;
      outline: none;
      cursor: pointer;
      padding: 14px 16px;
      transition: 0.3s;
      font-size: 17px;
    }

    /* Change background color of buttons on hover */
    .tab button:hover {
      background-color: #ddd;
    }

    /* Create an active/current tablink class */
    .tab button.active {
      background-color: #ccc;
    }
  </style>
</head>
<body>
  <h1>Welcome To Swift Act SFOTA Server</h1>
  <img src="ss.png" alt="Screenshot" width="350" height="220">
  <p>For more info, <a href="https://courses.swift-act.com/">visit my page</a>.</p>

  <!-- Add the login and register tabs -->
  <div class="tab">
    <button class="active">Login</button>
    <button>Register</button>
  </div>

  <div style="padding: 20px;">
    <!-- Add the login form -->
    <form action="script.php" method="POST">
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" required>

      <label for="password">Password:</label>
      <input type="password" id="password" name="password" required>

      <button type="submit" class="form__button" name="login">Login</button>
    </form>

    <!-- Add the registration form -->
    <form action="register.php" method="POST" style="display: none;">
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" required>

      <label for="password">Password:</label>
      <input type="password" id="password" name="password" required>

      <label for="confirm_password">Confirm Password:</label>
      <input type="password" id="confirm_password" name="confirm_password" required>

      <button type="submit" class="form__button" name="register">Register</button>
    </form>

    <?php if (isset($error)): ?>
      <p><?php echo $error; ?></p>
    <?php endif; ?>
  </div>
	<?php if ($flag==0): ?>
	<p>For SFOTA services, <a href="script.php">press here</a>.</p>
	<?php endif; ?>
</body>
</html>