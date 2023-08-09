<?php

session_start(); // Start a session to store the user's login status

if ($_SERVER['REQUEST_METHOD'] === 'POST') { // Check if the form has been submitted
    $username = $_POST['username']; // Get the username and password from the form data
    $password = $_POST['password'];

    // In a real application, you would validate the username and password against a database of user credentials
    if ($username === 'user' && $password === 'password') {
        $_SESSION['loggedin'] = true; // If the username and password are valid, set the $_SESSION['loggedin'] flag to true
        header('Location: welcome.php'); // Redirect the user to the welcome page
        exit;
    } else {
        $error = 'Invalid username or password'; // If the username and password are invalid, set an error message
    }
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <form class="form" method="POST" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>">
            <h1 class="form__title">Login</h1>
            <?php if (isset($error)): ?>
                <p class="form__error"><?php echo $error; ?></p>
            <?php endif; ?>
            <div class="form__group">
                <label for="username" class="form__label">Username</label>
                <input type="text" id="username" name="username" class="form__input" required>
            </div>
            <div class="form__group">
                <label for="password" class="form__label">Password</label>
                <input type="password" id="password" name="password" class="form__input" required>
            </div>
            <button type="submit" class="form__button">Login</button>
        </form>
    </div>
</body>
</html>