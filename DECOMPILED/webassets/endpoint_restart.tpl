<html>
<head>
  <title>Bridge endpoints</title>
  <link href="/css/bootstrap.css" rel="stylesheet" />
  <style type="text/css">
    body { font-family: Helvetica, Arial, sans-serif; padding-top: 60px; }
  </style>
</head>
<body>
  <div class="navbar navbar-fixed-top">
    <div class="navbar-inner">
      <div class="container">
        <a class="brand" href="/">BERG Cloud Bridge</a>
        <div class="nav-collapse">
          <ul class="nav">
            <li class="active"><a href="/configure">Configure</a></li>
          </ul>
          <ul class="nav pull-right">
            <li><a href="/"><strong>{{system_version}}</strong></a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>
  </div> 
  
  <div class="container">
    <div class="page-header">
      <h1>Endpoint updated</h1>
    </div>

      <p>The endpoint has been updated to point to <code>{{ endpoint }}</code>. Please wait while the Bridge software restarts for the change to take effect.</p>

    <div id="progress-bar" class="progress progress-striped active" style="margin-top: 50px; width: 400px">
        <div id="progress-bar-line" class="bar" style="width: 0%;"></div>
    </div>
    
  </div> <!-- /container -->
  
  <script src="/js/jquery.js"></script>
  <script src="/js/bootstrap.min.js"></script>
  <script>
    $( document ).ready(function() {
      var progress = setInterval(function () {
          var $line = $('#progress-bar-line');
          if ($line.width() >= 400) {
              clearInterval(progress);
              $('#progress-bar').removeClass('active');
              document.location.href="/";
          } else {
              $line.width($line.width() + 10);
          }
      }, 1000);
    });
  </script>
</body>
</html>
