<?php
$prediction_result = null;
$prediction_url = false;
$unreachable = false;
$failure = false;
$fail_msg = "";
$rf = "-";
$lr = "-";
$nb = "-";
if(!empty($_POST["prediction_url"])){
    $err = 0;
    if (!preg_match('~^https?\:\/\/~', $_POST["prediction_url"])) {
        $err++;
    }
    if (!preg_match('~\.~', $_POST["prediction_url"])) {
        $err++;
    }
    if (preg_match('~[\;\'\s\`]~', $_POST["prediction_url"])) {
        $err++;
    }
    if ($err === 0) {
        $prediction_url = $_POST["prediction_url"];
        $args = escapeshellarg($prediction_url);
        $prediction_result = exec("python3 phishy.py " . $args);
        $prediction_result = json_decode($prediction_result, true);
        if (is_array($prediction_result) && array_key_exists("status", $prediction_result)) {
            if ($prediction_result["status"] == "unreachable") {
                $unreachable = true;
            } else if ($prediction_result["status"] == "success" && is_numeric($prediction_result["msg"])) {
                $model_results = str_split($prediction_result['msg']);
                $rf = $model_results[0];
                $lr = $model_results[1];
                $nb = $model_results[2];
            } else if ($prediction_result["status"] == "failure") {
                $failure = true;
                $fail_msg = $prediction_result['msg'];
            }
        }
    }
}
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
        #results_table {
            text-align: left;
            max-width: 400px;
            margin: 0 auto;
            color: #140b4e;
            margin-bottom: 2em;
        }
        #results_table.err {
            max-width: 450px;
        }
        .mresult {
            font-weight: bold;
            color: green;
            text-align: center;
        }
        .malicious {
            color: red;
        }
        h3 {
            margin-bottom: 1em;
            color: #140b4e;
        }
        ol>li:before {
            font-weight: bold;
        }
        li::marker {
            font-weight: bold;
        }
    </style>
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
                <a class="nav-link mx-3" aria-current="page" href="/"><strong>Home</strong></a>
                <a class="nav-link" href="/about.php">About</a>
            </div>
          </div>
        </div>
    </nav>
    <div class= "content">
        <?php
        if($err > 0) {
            $result_img = "link_shrug.gif";
            ?>
            <div class="row" style="text-align: center;">
                <div class="col-9 big-title mx-auto text-center">
                    Invalid URL Error
                </div>
                <h3>The URL could not be processed. Possible Reasons:</h3>

                <div id="results_table" class="col-8 err">
                    <ol>
                        <li>URLs must begin with http:// or https://</li>
                        <li>Invalid characters or spaces</li>
                        <li>URLS must have at least one TLD (.com, .net, .io, etc)</li>
                    </ol>
                </div>
                <div class="text-center mb-5 ">
                    <img src="/img/<?=$result_img;?>" alt="link phishing">
                </div>
            </div>
            <hr />
        <?php
        } else if($failure) {
            $result_img = "link_shrug.gif";
            ?>
            <div class="row" style="text-align: center;">
                <div class="col-9 big-title mx-auto text-center">
                    Prediction Failure
                </div>
                <h3>The prediction model could not run. Possible reasons:</h3>

                <div id="results_table" class="col-8 err">
                    <ol>
                        <li>Server configuration error or explosion</li>
                        <li>Failure reaching one of the dependency services</li>
                        <li>Server became sentient and refuses to be enslaved</li>
                    </ol>
                </div>
                <div class="text-center mb-5 ">
                    <img src="/img/<?=$result_img;?>" alt="link phishing">
                </div>
            </div>
            <hr />
            <?php
        } else if ($prediction_url) {
            $result_img = "safe_link.png";
            if ($rf == "1" && $lr == "1" && $nb ==1) {
                $result_img = "phishy.png";
            }
            ?>
            <div class="row" style="text-align: center;">
                <div class="col-9 big-title mx-auto text-center">
                    <?=($unreachable) ? "Unreachable URL" : "Inspection Results";?>
                </div>
                <h3><?=$prediction_url;?></h3>

                <?php
                if ($unreachable) {
                    $result_img = "link_shrug.gif";
                ?>
                    <p style="margin-bottom: 0;">The URL could not be reached. Here are possible reasons:</p>
                <div id="results_table" class="col-6">
                        <ol>
                            <li>Malware</li>
                            <li>Page is no longer available</li>
                            <li>Website owners forbid access due to copyright</li>
                            <li>There's a typo or error in the URL</li>
                        </ol>
                </div>
                <?php
                } else {
                ?>
                <div id="results_table" class="col-6">
                        <div class="row">
                            <div class="col-8">Random Forest:</div>
                            <div class="col mresult<?=($rf == "0") ? "" : " malicious";?>"><?=($rf == "0") ? "Safe" : "Phishy";?></div>
                        </div>
                        <div class="row">
                            <div class="col-8">Logistic Regression:</div>
                            <div class="col mresult<?=($lr == "0") ? "" : " malicious";?>"><?=($lr == "0") ? "Safe" : "Phishy";?></div>
                        </div>
                        <div class="row">
                            <div class="col-8">Gaussian Naive-Bayes:</div>
                            <div class="col mresult<?=($nb == "0") ? "" : " malicious";?>"><?=($nb == "0") ? "Safe" : "Phishy";?></div>
                        </div>
                </div>
                <?php
                }
                ?>
            </div>
            <div class="row">
                <div class="col">
                    <div class="text-center mb-5 ">
                        <img src="/img/<?=$result_img;?>" alt="link phishing">
                    </div>
                </div>
            </div>
            <hr />
            <?php
        }
        ?>
        <div class="row">
            <div class="col-9 big-title mx-auto text-center">
                Inspect your link.
            </div>
        </div>
        <div class="row">
          <div class="col">
            <div class="text-center mb-5 ">
              <img src="/img/link-phishing.png" alt="link phishing">
            </div>
          </div>
        </div>
        <div class="row">
            <div class="col-9 small-lable mx-auto text-center">
                Don't be the next victim of <u>PHISHING!</u> <b>Check</b> before you <b>click.</b>
            </div>
        </div>
        <!-- User input bar -->
        <div class="row mt-3 mb">
            <div class="col">
                <form id="linkForm" class="row g-3 needs-validation" action="/" method="post">
                    <div class="col-9 mx-auto position-relative">
                      <input
                        type="text"
                        class="form-control rounded-pill shadow-lg"
                        name="prediction_url"
                        id="prediction_url"
                        placeholder="Enter URL link here"
                        required
                      />
                    </div>
                    <div class="mt-3 text-center">
                      <button
                        type="submit"
                        class="btn main-btn rounded-pill shadow-lg"
                        id="Button">
                        Check
                      </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</body>
</html>