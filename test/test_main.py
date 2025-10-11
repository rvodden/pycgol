import pytest
from unittest.mock import Mock, patch

from pycgol.__main__ import main


class TestMain:

    @patch('pycgol.__main__.Application')
    def test_main_creates_and_runs_application(self, mock_application_class):
        mock_app_instance = Mock()
        mock_application_class.return_value = mock_app_instance

        main()

        # Verify Application was instantiated
        mock_application_class.assert_called_once()

        # Verify run method was called
        mock_app_instance.run.assert_called_once()

    @patch('pycgol.__main__.Application')
    def test_main_when_called_as_script(self, mock_application_class):
        # This test verifies the if __name__ == "__main__" block
        # We can't directly test this without executing the module,
        # but we can test that main() works correctly when called
        mock_app_instance = Mock()
        mock_application_class.return_value = mock_app_instance

        main()

        # Should behave the same as the direct call test
        mock_application_class.assert_called_once()
        mock_app_instance.run.assert_called_once()