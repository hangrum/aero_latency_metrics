#!/usr/bin/env python3.8
import subprocess

def getProcessOutput(cmd):
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

def getLatencyAsadm(host):
  cmd="/usr/local/bin/asadm"
  host="10.3.5.61"
  keys = ['namespace','histogram',
  'node','time','ops','1ms','8ms','64ms']
  cmd = cmd + " -e \"show latencies\" -h " + host
  result = '\n'.join(getProcessOutput(cmd).split("\n")[4:])
  list_by_line = []
  for str in result.split('\n'):
    no_space_string = str.replace(' ','')
    list_by_line.append(no_space_string.split('|'))
  dictionary_by_line = []
  for line in list_by_line:
    dictionary_by_line.append(dict(zip(keys,line)))
  return dictionary_by_line

# https://github.com/prometheus/client_python
# prometheus python
if __name__ == '__main__':
  print(getLatencyAsadm())
