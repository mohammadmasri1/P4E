<?php
$allowed_ips = array('192.168.1.0', '192.168.1.255'); // Replace with your lab's IP range
if (in_array($_SERVER['REMOTE_ADDR'], $allowed_ips)) {
    // Allow access to the form
    echo '<iframe src="https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform" width="100%" height="800" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>';
} else {
    echo 'Access denied';
}
?>
