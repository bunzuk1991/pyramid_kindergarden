<!DOCTYPE html>
<html lang="{{ '${request.locale_name}' }}">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="pyramid web application">
    <meta name="author" content="Pylons Project">
    <link rel="shortcut icon" href="${request.static_url('kindergarden:static/pyramid-16x16.png')}">
    <title>PyCharm Starter project for the Pyramid Web Framework</title>
##     <link href="${request.static_url('kindergarden:static/theme.css')}" rel="stylesheet">
    <link rel="stylesheet" href="${request.static_url('kindergarden:static/css/admin/style.css')}">
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
</head>

<body>

<div class="content-wrapper">
    ${next.body()}
</div>

<div id="pDebug">
    <div id="pDebugToolbarHandle">
        <a title="Show Toolbar" id="pShowToolBarButton" href="http://127.0.0.1:6543/_debug_toolbar/3131353833363936" target="pDebugToolbar">«</a>
    </div>
</div>
<script
  src="https://code.jquery.com/jquery-3.3.1.js"
  integrity="sha256-2Kok7MbOyxpgUVvAk/HJ2jigOSYS2auK4Pfzbm7uH60="
  crossorigin="anonymous"></script>
</body>
</html>
