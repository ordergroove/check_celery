import mock
import subprocess
import unittest

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
        mock_check_output.return_value = '(node {}) (pid 1) is running\n(node {}) (pid 2) is running\n'.format(self._workers[0], self._workers[1])
        self._cwc.run_check()
        self._cwc.ok_state.assert_called_once_with(self._cwc.OK_STATUS_MSG)

    def test_workers_down(self, mock_check_output):
        mock_check_output.return_value = ''
        with self.assertRaises(SystemExit):
            self._cwc.run_check()
        self._cwc.critical_state.assert_called_once_with(
            self._cwc.CRITICAL_STATUS_MSG_TPL.format(', '.join(self._workers))
        )
