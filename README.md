<!--
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
-->

# python-rclone

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![Build Status](https://travis-ci.org/ddragosd/python-rclone.svg?branch=master)](https://travis-ci.org/ddragosd/python-rclone)

A Python wrapper for [rclone](https://rclone.org/).
This is a fork of https://github.com/ddragosd/python-rclone. 
Main change from that work is there is no longer a requirement to pass a custom configuration - though it is still optional. 


`rclone` must be already [installed](https://rclone.org/install/) and discoverable in `$PATH`. 

## Status
Work in progress. Experimental.

## Usage

```python
from rclone import RClone

rclone = RClone()


# configuration can now be passed as an optional keyword argument
cfg = """[local]
type = local
nounc = true"""

rclone = RClone(config=cfg)
result = rclone.listremotes()

print(result.get('out'))
# b'local:\n'
print(result.get('code'))
# 0
print(result.get('error'))
# b''
```

###  Implemented commands:

* `copy`            Copy files from source to dest, skipping already copied
* `sync`            Make source and dest identical, modifying destination only.
* `listremotes`     List all the remotes in the config file.
* `ls`              List the objects in the path with size and path.
* `lsjson`          List directories and objects in the path in JSON format.
* `delete`          Remove the contents of path.

Even if not all `rclone` commands have been exposed, it's possible to invoke any command using `run_cmd` method directly, as shown in the example bellow:

```python
result = rclone.run_cmd(command="lsd", extra_args=["local:/tmp", "-v", "--dry-run"])
```

### Logging and Debugging

To see more info about which commands are executed, or what other messages they print, you can enable logging as the example bellow shows: 

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s [%(levelname)s]: %(message)s")

```

## Developer guide

```bash
$ pip install -r requirements.txt
$ make test
```
