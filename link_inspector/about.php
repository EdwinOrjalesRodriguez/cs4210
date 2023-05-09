<?php
?>
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
  <link rel="stylesheet" href="styles.css"/>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>
  <title>Link Inspector</title>
    <style>
        nav {
            z-index: 999;
        }
        .website {
            background: #000;
        }
        header {
            -o-transition-duration: 0.3s;
            -moz-transition-duration: 0.3s;
            -webkit-transition-duration: 0.3s;
            transition-duration: 0.3s;
            padding:  0px 0;
            position: fixed;
            top: 0;
            width: 100%;
            background: #333;
            border-bottom: 3px solid #dad;
        }
        /* GRADIEND */
        .ap {
            position: fixed;
            right: 0;
            bottom: 0;
            left: 0;
            height: 40px;
            margin: auto;
            font-family: Arial, sans-serif;
            font-size: 14px;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            color: #333;
            background: #222;
            border-top: 2px solid #f0f;
            z-index: 9999;
        }
        /*END*/

        @import url(https://fonts.googleapis.com/css?family=Open+Sans+Condensed:300);
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            height: 100%;
        }

        body {
            background: radial-gradient(ellipse at top left, #334455 0%, #112233 100%);
            overflow: hidden;
        }

        .wrapper {
            position: absolute;
            top: 100%;
            left: 50%;
            width: 100%;
            margin-left: -50%;
            font: 300 30px/1 'Open Sans Condensed', sans-serif;
            text-align: center;
            text-transform: uppercase;
            color: #fff;
            animation: 90s credits linear infinite;
            z-index: 0;
        }

        .movie {
            margin-bottom: 50px;
            font-size: 50px;
        }

        .job {
            margin-bottom: 5px;
            font-size: 18px;
        }

        .name {
            margin-bottom: 50px;
            font-size: 35px;
        }

        .disclaimer {
            font-size: 16px;
            line-height: 1.3em;
        }

        @keyframes credits {
            0% {
                top: 100%;
            }
            100% {
                top: -500%;
            }
        }
    </style>
    <script>
    </script>
</head>
<body class= "website">
    <!-- Navigation bar -->
    <nav class="navbar bg-light navbar-expand-lg shadow-lg">
        <div class="container-fluid mx-5">
          <a class="navbar-brand" href="index.html">
            <img src="/img/ml-logo.png" alt="logo" width="75">
          </a>
          <div class="nav-title"><b>Link Inspector</b></div>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse">
            <div class="navbar-nav">
                <a class="nav-link mx-3" aria-current="page" href="/">Home</a>
                <a class="nav-link" href="/about.php"><strong>About</strong></a>
            </div>
          </div>
        </div>
    </nav>
    <div class= "content">
        <div class='wrapper'>
            <div class='movie'>
                CPP4210 Development Team</div>
            <div class='job'>
                Team Lead</div>
            <div class='name'>
                Sherelene De Belen</div>
            <div class='job'>
                Systems Programming</div>
            <div class='name'>
                Edwin O. Rodriguez</div>
            <div class='job'>
                ML Logistics</div>
            <div class='name'>
                Alexander Rodriguez</div>
            <div class='job'>
                UI Coordinator</div>
            <div class='name'>
                Pablo Duenas</div>
            <div class='job'>
                Dan</div>
            <div class='name'>
                Dan Nguyen</div>
            <div class='job'>
                AWS Consultant</div>
            <div class='name'>
                Edwin O. Rodriguez</div>
            <div class='job'>
                Research Coordinator #1</div>
            <div class='name'>
                Dan Nguyen</div>
            <div class='job'>
                Research Coordinator #2</div>
            <div class='name'>
                Alexander Rodriguez</div>
            <div class='job'>
                AI &amp; Fashion Consultant</div>
            <div class='name'>
                Hussain Zaidi</div>
            <div class='job'>
                Model Training</div>
            <div class='name'>
                Sherelene De Belen</div>
            <div class='job'>
                Hat Consultant</div>
            <div class='name'>
                Joey Cindass</div>
            <div class='job'>
                Visual Effects</div>
            <div class='name'>
                Edwin O. Rodriguez</div>
            <div class='job'>
                Presenter</div>
            <div class='name'>
                Pablo Duenas</div>
            <div class='job'>
                Hotel</div>
            <div class='name'>
                Trivago</div>
            <div class='credits_logo'>
                <img src="/img/credits_logos.jpg" style="width: 100%">
            </div>
            <div class='disclaimer'>
                Presented in Technicolor, where available. The events, characters, and algorithms in this project may be ficticious. And any similarity to actual persons, living or dead, or to actual events is purely coincidental.
            </div>

    </div>
</body>
</html>