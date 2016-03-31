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
      <h1>Bridge configuration</h1>
    </div>
    
    % if defined('error'):
      <div class="alert alert-error">{{ error }}</div>
    % end
    
    <div>
      <p>This page allows you to set the URL that the Bridge connects to. The Bridge is currently <span class="label {{ connection_state_label_class }}">{{ connection_state }}</span>.</p>
      <p>You must begin your URL with either <code>https</code> or <code>http</code> depending on whether you want the built-in SSL certificates to be used or not, and this is independent of any port you specify.</p>
      <p>Please note that any path you provide will be ignored, as the bridge is hard-coded to connect to <code>/api/v1/connection</code>.</p>
    </div>

    <form class="well form-inline" method="POST">
      <label><strong>Server URL</strong></label>
      <input type="text" class="input-xlarge" placeholder="https://bridge.bergcloud.com/" name="endpoint" value="{{ endpoint }}">
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    
  </div> <!-- /container -->
  
  <script src="/js/jquery.js"></script>
  <script src="/js/bootstrap.min.js"></script>
  
</body>
</html># 
