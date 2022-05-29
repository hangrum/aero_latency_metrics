#!/usr/bin/env python3.8
from prometheus_client import start_http_server, Gauge
import subprocess
import time

class PrometheusClient:
    def __init__(self):
        #     # Start up the server to expose the metrics.
        start_http_server(8001)
        self.labels = ['namespace','histogram','node','gt']
        self.g = Gauge('aerospike_latency',
          'latency of aerospike just like fucking amc showing me',self.labels)

    def getProcessOutput(self, cmd):
      process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE)
      process.wait()
      data, err = process.communicate()
      if process.returncode == 0:
        return data.decode('utf-8')
      else:
        print("Error:", err)
      return ""

    def getLatencyAsadm(self, host="10.3.5.61", cmd="/usr/bin/asadm"):
      keys = ['namespace','histogram',
      'node','time','ops','1ms','8ms','64ms']
      cmd = cmd + " -e \"show latencies\" -h " + host
      result = '\n'.join(self.getProcessOutput(cmd).split("\n")[4:])
      list_by_line = []
      for str in result.split('\n'):
        no_space_string = str.replace(' ','')
        list_by_line.append(no_space_string.split('|'))
      dictionary_by_line = []

      for line in list_by_line:
        if line[0] and ("Numberofrows" not in line[0]):
          dictionary_by_line.append(dict(zip(keys,line)))
      return dictionary_by_line

    def SetMetricsLatency(self):

      latency_dict=self.getLatencyAsadm()
      # latency greater than 1ms, 8ms ,64ms
      for i in latency_dict:
        for j in [ "1ms",'8ms','64ms','ops']:
          self.g.labels(i['namespace'],i['histogram'],i['node'],j).set(i[j])
      return self.g

# https://github.com/prometheus/client_python
# prometheus python
if __name__ == '__main__':
  p = PrometheusClient()
  while True:
    p.SetMetricsLatency()
    time.sleep(1)
