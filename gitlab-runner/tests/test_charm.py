# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing
import pathlib
import sys
import unittest
from unittest.mock import Mock
from unittest.mock import patch

# from ops.model import ActiveStatus

import ops.testing
from ops.testing import Harness

# Set testing environmental variable
ops.testing.SIMULATE_CAN_CONNECT = True

# Get paths
current_path = pathlib.Path.cwd()
src_path = current_path.parent.joinpath('src')
templates_path = current_path.parent.joinpath('templates')

print(f"Current path: {current_path.as_posix()}\n"
      f"src path: {src_path.as_posix()}, Valid: {src_path.is_dir()}\n"
      f"Templates path: {templates_path.as_posix()}, Valid: {templates_path.is_dir()}")

sys.path.append(src_path.as_posix())
try:
    from charm import GitlabRunnerCharm
    from gitlab_runner import get_token
except ImportError:
    print("ERROR: Import of charm.GitlabRunnerCharm failed!")
    raise


class TestCharm(unittest.TestCase):

    def setUp(self):
        self.harness = Harness(GitlabRunnerCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    @patch('subprocess.Popen')
    @patch('subprocess.run')
    @patch('gitlab_runner.get_token')
    def test_01_config_changed(self, mock_subprocess_popen, mock_subprocess_run, mock_get_token):
        # Mock return code from processes
        mock_subprocess_popen.return_value.returncode = 0
        mock_subprocess_run.return_value.returncode = 0
        mock_get_token.gitlab.runner.get_token = 'ABCDEFGH'

        harness = Harness(GitlabRunnerCharm)
        self.addCleanup(harness.cleanup)
        harness.begin()
        # self.assertEqual(list(harness.charm._stored.executor), [])
        harness.update_config({"gitlab-registration-token": "abc",
                               "gitlab-server": "https://gitlab.com",
                               "executor": "docker"})
        print(harness.charm.unit.status)
        self.assertEqual(harness.charm.config["executor"], "docker2", msg='Executor not as configured')

    def test_20_templates_runner_templates(self):
        assert True
