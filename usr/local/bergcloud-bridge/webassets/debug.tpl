<html>
<head>
  <title>Bridge status</title>
  <link href="/css/bootstrap.css" rel="stylesheet" />
  <style type="text/css">
    body { font-family: Helvetica, Arial, sans-serif; padding-top: 60px; }
  </style>
</head>
<body>
  <div class="navbar navbar-fixed-top">
    <div class="navbar-inner">
      <div class="container">
        <a class="brand" href="#">BERG Cloud Bridge</a>
        <div class="nav-collapse">
          <ul class="nav">
            <li class="active"><a href="#">Status</a></li>
          </ul>
          <ul class="nav pull-right">
            <li><a href="#"><strong>{{system_version}}</strong></a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>
  </div> 
  
  <div class="container">
    <div class="page-header">
      <h1>Watchdog <small>Automatic reboot is {{watchdog_status}}</small></h1>
    </div>
    
    <table class="table table-bordered table-striped">
      <thead>
        <tr>
          <th>Key name</th>
          <th>Key freshness</th>
        </tr>
      </thead>
      <tbody>
        {{!watchdog_key_table}}
      </tbody>
    </table>
    
    <div class="page-header">
      <h1>Ethernet</h1>
    </div>
    
    <div class="well">
      <!-- <a class="btn btn-primary" style="float: right" href="/action/toggle_ethernet_speed/">Force {{next_eth_speed}}</a> -->
      <p><strong>{{eth_speed}}BaseT</strong> Full-Duplex: {{eth_duplex}} Auto-Speed: {{eth_auto}}  Carrier: {{eth_up}}</p>
    </div>
    
%if command_transferring:
    <div class="page-header">
      <h1>Zigbee</h1>
    </div>

    <div class="alert alert-info">
      Transferring a command to <span class="label">{{command_destination_eui64}}</span> with <span class="badge badge-success">{{command_tx_speed}} bytes/sec</span> with <span class="badge badge-warning">{{command_packet_errors}}</span>
    </div>
%end

    <div class="page-header">
      <h1>Device radio summary</h1>
    </div>
    
    <table class="table table-bordered table-striped">
      <thead>
        <tr><th>Hardware address</th><th>Avg. RSSI</th><th>Min. RSSI</th><th>Max. RSSI</th></tr>
      </thead>
      <tbody>
%for key in device_radio_stats.keys():
        <tr><td>{{key}}<td>{{device_radio_stats[key][0]}}</td> <td>{{device_radio_stats[key][1]}}</td> <td>{{device_radio_stats[key][2]}}</td></tr>
%end
      </tbody>
    </table>

    <div class="page-header">
      <h1>Packet list</h1>
    </div>
    
    <table class="table table-bordered table-striped">
      <thead>
        <tr><th>Hardware address</th><th>Time</th><th>LQI</th><th>RSSI</th></tr>
      </thead>
      <tbody>
%for key in packet_telemetry.keys():
  %for pkt in packet_telemetry[key]:
          <tr><td>{{key}}<td>{{pkt[1]}}</td> <td>{{pkt[2]}}/255</td> <td>{{pkt[3]}}</td></tr>
  %end
%end
      </tbody>
    </table>

    <hr />
    
    <div class="page-header">
      <h1>Logs</h1>
    </div>
    
    <table class="table table-bordered table-striped">
      <thead>
        <tr><th>Time</th><th>Name</th><th>Level</th><th>Message</th></tr>
      </thead>
      <tbody>
%for row in log_statements:
        {{!row}}
%end
      </tbody>
    </table>
    
  </div> <!-- /container -->
  
  <script src="/js/jquery.js"></script>
  <script src="/js/bootstrap.min.js"></script>
  
</body>
</html>