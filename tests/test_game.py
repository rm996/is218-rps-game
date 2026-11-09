"""Unit and integration tests for RPS-001."""

from unittest.mock import patch

import pytest

from app import app
from game import determine_winner


@pytest.mark.unit
@pytest.mark.parametrize(
    ("player", "computer", "expected"),
    [
        ("rock", "rock", "tie"),
        ("rock", "paper", "lose"),
        ("rock", "scissors", "win"),
        ("paper", "rock", "win"),
        ("paper", "paper", "tie"),
        ("paper", "scissors", "lose"),
        ("scissors", "rock", "lose"),
        ("scissors", "paper", "win"),
        ("scissors", "scissors", "tie"),
    ],
)
def test_all_nine_outcomes(player, computer, expected):
    """Check every possible matchup from the player's perspective."""
    assert determine_winner(player, computer) == expected


@pytest.mark.integration
def test_real_round_request():
    """Check that a real Flask request uses the winner rules."""
    app.config["TESTING"] = True

    with patch("app.random.choice", return_value="scissors"):
        with app.test_client() as client:
            response = client.post("/", data={"move": "rock"})

    assert response.status_code == 200
    assert b"You win!" in response.data
    assert b"rock" in response.data.lower()
    assert b"scissors" in response.data.lower()


@pytest.mark.integration
@pytest.mark.parametrize("data", [{}, {"move": "banana"}])
def test_invalid_moves_return_400(data):
    """Missing and unsupported moves must be rejected."""
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.post("/", data=data)

    assert response.status_code == 400
    assert b"Choose Rock, Paper, or Scissors" in response.data
