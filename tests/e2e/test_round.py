"""Real browser tests for completed Rock, Paper, Scissors rounds."""

import pytest
from playwright.sync_api import Page, expect

import app as web

pytestmark = pytest.mark.e2e


def test_real_round_and_replay(page: Page, live_server, monkeypatch):
    """Play a winning round, then replay with a losing round."""

    computer_moves = iter(["scissors", "rock"])
    monkeypatch.setattr(
        web.random,
        "choice",
        lambda _moves: next(computer_moves),
    )

    page.goto(live_server)

    # Round 1: Rock beats scissors.
    page.get_by_role("button", name="Rock", exact=True).click()

    choices = page.get_by_label("This round’s choices")
    expect(choices).to_be_visible()
    expect(choices).to_contain_text("Rock")
    expect(choices).to_contain_text("Scissors")

    expect(page.locator("[data-outcome]")).to_have_attribute("data-outcome", "win")
    expect(page.get_by_role("heading", name="You win!")).to_be_visible()

    # Round 2: Scissors loses to rock.
    page.get_by_role("button", name="Scissors", exact=True).click()

    choices = page.get_by_label("This round’s choices")
    expect(choices).to_contain_text("Scissors")
    expect(choices).to_contain_text("Rock")

    expect(page.locator("[data-outcome]")).to_have_attribute("data-outcome", "lose")
    expect(page.get_by_role("heading", name="Computer wins")).to_be_visible()

    # Only the latest round's result should appear.
    expect(page.locator("[data-outcome]")).to_have_count(1)
