"""
A Python wrapper for rclone.
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
import tempfile

logger = logging.getLogger("RClone")
if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)






class RClone:
    """
    Wrapper class for rclone.
    """

    def __init__(self, config=None,verbose=True,dryrun=False):
        self.config = config
        self.verbose = verbose
        self.dryrun = dryrun

        #self.cfg = cfg.replace("\\n", "\n")
        #logging = logging.getLogger("RClone")

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value=None):
        self._config = value

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value = True):
        self._verbose = value

    @property
    def dryrun(self):
        return self._dryrun

    @dryrun.setter
    def dryrun(self, value=False):
        self._dryrun = value

    def configure(self, cfg):
        """
        :param cfg: use custom configuration (system config will not be used)
        :return:
        """
        self.config = cfg



    def _execute(self, command_with_args):
        """
        Execute the given `command_with_args` using Popen

        Args:
            - command_with_args (list) : An array with the command to execute,
                                         and its arguments. Each argument is given
                                         as a new element in the list.
        """
        logging.debug("Invoking : %s", " ".join(command_with_args))
        try:
            with subprocess.Popen(
                    command_with_args,
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

    def run_cmd(self, command, extra_args=[]):
        """
        Execute rclone command

        Args:
            - command (string): the rclone command to execute.
            - extra_args (list): extra arguments to be passed to the rclone command
        """

        command_with_args = ["rclone", command] + extra_args
        if self.dryrun == True:
            command_with_args.append("--dry-run")
        if self.verbose == True:
            command_with_args.append("-v")

        if self.config and isinstance(self.config, str):
            # save the configuration in a temporary file
            with tempfile.NamedTemporaryFile(mode='wt', delete=True) as cfg_file:
                # cfg_file is automatically cleaned up by python
                logging.debug("rclone config: ~%s~", self.cfg)
                cfg_file.write(self.cfg)
                cfg_file.flush()
                command_with_args += ["--config",cfg_file.name]
                command_result = self._execute(command_with_args)
                cfg_file.close()

        else:
            command_result = self._execute(command_with_args)

        return command_result


    def copy(self, source, dest, flags=[]):
        """
        Executes: rclone copy source:path dest:path [flags]

        Args:
        - source (string): A string "source:path"
        - dest (string): A string "dest:path"
        - flags (list): Extra flags as per `rclone copy --help` flags.
        """
        return self.run_cmd(command="copy", extra_args=[source] + [dest] + flags)

    def sync(self, source, dest, flags=[]):
        """
        Executes: rclone sync source:path dest:path [flags]

        Args:
        - source (string): A string "source:path"
        - dest (string): A string "dest:path"
        - flags (list): Extra flags as per `rclone sync --help` flags.
        """
        return self.run_cmd(command="sync", extra_args=[source] + [dest] + flags)

    def listremotes(self, flags=[]):
        """
        Executes: rclone listremotes [flags]

        Args:
        - flags (list): Extra flags as per `rclone listremotes --help` flags.
        """
        return self.run_cmd(command="listremotes", extra_args=flags)

    def ls(self, dest, flags=[]):
        """
        Executes: rclone ls remote:path [flags]

        Args:
        - dest (string): A string "remote:path" representing the location to list.
        """
        return self.run_cmd(command="ls", extra_args=[dest] + flags)

    def lsjson(self, dest, flags=[]):
        """
        Executes: rclone lsjson remote:path [flags]

        Args:
        - dest (string): A string "remote:path" representing the location to list.
        """
        return self.run_cmd(command="lsjson", extra_args=[dest] + flags)

    def delete(self, dest, flags=[]):
        """
        Executes: rclone delete remote:path

        Args:
        - dest (string): A string "remote:path" representing the location to delete.
        """
        return self.run_cmd(command="delete", extra_args=[dest] + flags)


def with_config(cfg):
    """
    Configure a new RClone instance.
    """
    inst = RClone(cfg=cfg)
    return inst
