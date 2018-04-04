import subprocess
import unittest
import mock

from check_celery import CeleryWorkerCheck


@mock.patch('check_celery.subprocess.check_output')
class TestCeleryWorkerCheck(unittest.TestCase):
    def setUp(self):
        self._service = 'service'
        self._workers = ['worker1', 'worker2']
        self._cwc = CeleryWorkerCheck(self._workers, self._service)

        # Mock the NagiosPlugin methods and how they would behave - i.e. SystemExit is raised
        self._cwc.ok_state = mock.Mock()
        self._cwc.critical_state = mock.Mock(side_effect=SystemExit)
        self._cwc.unknown_state = mock.Mock(side_effect=SystemExit)

    def test_service_status_exception(self, mock_check_output):
        mock_check_output.side_effect = subprocess.CalledProcessError(2, 'test')
        with self.assertRaises(SystemExit):
            self._cwc.run_check()
        self._cwc.unknown_state.assert_called_once_with(self._cwc.UNKNOWN_STATUS_MSG)

    def test_all_workers_running(self, mock_check_output):
        mock_check_output.return_value = '{} (node {}) (pid 1) is running\n{} (node {}) (pid 2) is running\n'.format(self._service, self._workers[0], self._service, self._workers[1])
        self._cwc.run_check()
        self._cwc.ok_state.assert_called_once_with(self._cwc.OK_STATUS_MSG)

    def test_workers_down(self, mock_check_output):
        mock_check_output.return_value = ''
        with self.assertRaises(SystemExit):
            self._cwc.run_check()
        self._cwc.critical_state.assert_called_once_with(
            self._cwc.CRITICAL_STATUS_MSG_TPL.format(', '.join(self._workers))
        )

    def test_all_workers_running_mixing_init_script_outputs(self, mock_check_output):
        mock_check_output.return_value = '{} (pid 1) is up\n{} (node {}) (pid 2) is running\n'.format(
            self._service, self._service, self._workers[1]
        )

        self._cwc.run_check()
        self._cwc.ok_state.assert_called_once_with(self._cwc.OK_STATUS_MSG)

    def test_mixed_worker_status_with_mixed_init_script_outputs(self, mock_check_output):
        mock_check_output.return_value = '{} (pid 1) is down\n{} (node {}) (pid 2) is running\n'.format(
            self._service, self._service, self._workers[1]
        )

        with self.assertRaises(SystemExit):
            self._cwc.run_check()
        self._cwc.critical_state.assert_called_once_with(
            self._cwc.CRITICAL_STATUS_MSG_TPL.format(self._workers[0])
        )

    def test_10_1_init_script_exit_status_check_gets_parsed(self, mock_check_output):
        cmd_output = '{} down: no pidfiles found\n'.format(self._service)
        mock_check_output.side_effect = subprocess.CalledProcessError(
            cmd='cmd', returncode=1, output=cmd_output
        )

        with self.assertRaises(SystemExit):
            self._cwc.run_check()
        self._cwc.critical_state.assert_called_once_with(
            self._cwc.CRITICAL_STATUS_MSG_TPL.format(', '.join(self._workers))
        )
