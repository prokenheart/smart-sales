import sys
from pathlib import Path
import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)