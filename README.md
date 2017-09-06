# dd-check-memsql
This is Agent Check for Datadog for collecting metrics of MemSQL Cluster.

## Installation
Install MemSQL client.

```
$ sudo /opt/datadog-agent/embedded/bin/pip install memsql
```

And deploy this script into `checks.d/` folder.

```
$ sudo cp ./checks.d/memsql.py /etc/dd-agent/checks.d/
```

Create a file `memsql.yaml` in the Agent's `conf.d/` folder.

```
$ cp ./conf.d/memsql.yaml.example /etc/dd-agent/conf.d/memsql.yaml
```

## Development

```console
# Install datadog-agent
$ bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/osx/install.sh)"
# Install dependencies
$ sudo /opt/datadog-agent/embedded/bin/pip install memsql
# symlink script and config to dadadog-agent config directory
$ ./script/bootstrap

# run dd-check-memsql
$ datadog-agent-check
```
