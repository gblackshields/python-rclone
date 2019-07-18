"""
A very basic Python wrapper for rclone.
"""
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

# pylint: disable=W0102,W0703,C0103

import logging
import subprocess
import shlex

logger = logging.getLogger("RClone")
if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)


def execute(command, options=[]):
    """
    Execute the given `command_with_args` using Popen

    Args:
        - command_with_args (list) :
            An array with the command to execute, and its arguments.
            Each argument is given as a new element in the list.
    """

    chopped = shlex.split(command) + options
    logging.debug(f'command to be executed : {" ".join(chopped)}')

    try:
        with subprocess.Popen(
                chopped,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE) as proc:
            (out, err) = proc.communicate()

            logging.debug(out)

            if err:
                logging.warning(err.decode("utf-8").replace("\\n", "\n"))

            return {
                "code": proc.returncode,
                "out": out,
                "error": err
            }
    except FileNotFoundError as not_found_e:
        logging.error("Executable not found. %s", not_found_e)
        return {
            "code": -20,
            "error": not_found_e
        }
    except Exception as generic_e:
        logging.exception("Error running command. Reason: %s", generic_e)
        return {
            "code": -30,
            "error": generic_e
        }

def copy(source, dest, options=[]):
    """
    copy data from source to destination.

    :param source: string in the rclone format source:path
    :param dest: string in the rclone format dest:path
    :param options: any optional flags that will be passed to rclone
    :return:
    """
    return execute(f"rclone copy {source} {dest}", options=options)
    

def move(source, dest, options=[]):
    """
    move data from source to destination.

    :param source: string in the rclone format source:path
    :param dest: string in the rclone format dest:path
    :param options: any optional flags that will be passed to rclone
    :return:
    """
    return execute(f"rclone move {source} {dest}", options=options)


def sync(source, dest, options=[]):
    """
    sync data between source and destination.

    :param source: string in the rclone format source:path
    :param dest: string in the rclone format dest:path
    :param options: any optional flags that will be passed to rclone
    :return:
    """
    return execute(f"rclone sync {source} {dest}", options=options)


def size(target, options = []):
    """
    return the size of a target folder .

    :param target: string in the rclone format source:path
    :param options: any optional flags that will be passed to rclone
    :return:
    """
    return execute(f"rclone size {target}", options=options)


def listremotes(options=[]):
    return execute(f"rclone listremotes", options=options)


def ls(target, options = []):
    return execute(f"rclone ls {target}", options=options)


def lsjson(target, options = []):
    return execute(f"rclone lsjson {target}", options=options)


def delete(target, options=[]):
    return execute(f"rclone delete {target}", options=options)



