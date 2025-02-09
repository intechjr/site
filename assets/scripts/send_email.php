<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars($_POST['contact-name']);
    $email = htmlspecialchars($_POST['contact-email']);
    $message = htmlspecialchars($_POST['contact-message']);

    $to = "aajracam@gmail.com";
    $subject = "Contato do site";
    $body = "Nome: $name\nEmail: $email\n\nMensagem:\n$message";
    $headers = "From: $email";

    if (mail($to, $subject, $body, $headers)) {
        echo "Email enviado com sucesso!";
    } else {
        echo "Falha ao enviar o email.";
    }
}
else {
    echo "<script>
        alert('Método de requisição inválido.');
        window.history.back();
    </script>";
}
?>