
# Rock, Paper, Scissors

## RPS-001: Play a Round

**Purpose:** One person plays a quick round of Rock, Paper, Scissors against the computer.

- The player chooses rock, paper, or scissors.
- The computer randomly chooses one move for that round.
- The game displays both choices and the result: **You win!**, **Computer wins**, or **It's a tie**.
- Choosing another move starts an independent round.
- No score or saved history is required.
- The supplied Flask server and game interface must remain unchanged.

### Expected Results

Results are from the player's perspective. The function `determine_winner(player, computer)` in `game.py` returns `win`, `lose`, or `tie`.

| Player | Computer | Expected Return |
| --- | --- | --- |
| rock | rock | tie |
| rock | paper | lose |
| rock | scissors | win |
| paper | rock | win |
| paper | paper | tie |
| paper | scissors | lose |
| scissors | rock | lose |
| scissors | paper | win |
| scissors | scissors | tie |

### Prediction

Before implementing the game rules, I predicted that if I chose Rock and the computer chose Scissors, I would win because Rock beats Scissors.

I also predicted that Paper would lose to Scissors because Scissors cuts Paper.

If the player and computer chose the same move, the result should be a tie.

### Agreed Implementation Plan

1. Implement `determine_winner(player, computer)` in `game.py`.
2. Return `win`, `lose`, or `tie` from the player's perspective.
3. Preserve the supplied Flask application and game interface.
4. Display both moves and the correct result after each round.
5. Allow the player to choose again to start a new independent round.
6. Add nine unit tests covering every possible matchup.
7. Add integration tests checking real requests and responses.
8. Add real-browser tests checking a complete round and replay.
9. Preserve HTTP 400 responses for missing and unsupported moves.
10. Run the full project checks and manually test the game.

### Test Plan

| Level | Cases and Evidence |
| --- | --- |
| Unit - positive | Test all nine possible combinations of Rock, Paper, and Scissors, including wins, losses, and ties. |
| Integration - positive | Submit a real Flask request and verify the displayed result. Control the computer's random move while using the real game rules. |
| Integration - negative | Verify that missing and unsupported moves return HTTP 400 with a helpful message. |
| E2E - positive | Use Playwright with the supplied `live_server` and `page` fixtures to play a round and replay through the real browser and HTTP server. |

The tests use the `unit`, `integration`, and `e2e` pytest markers.

### Invalid Input Prediction

If a player submits an unsupported move such as `banana`, the server should reject the request with HTTP 400 and a helpful error message.

A request with no player move should also return HTTP 400.

The server should not call the game rules for invalid moves.

### Scope

This feature implements one independent round at a time.

No scoring system, database, accounts, additional frameworks, or AI API will be added.

## RPS-001: Implementation and Verification

### Implementation

I implemented the Rock, Paper, Scissors rules in `game.py` using the function `determine_winner(player, computer)`.

The function returns `"win"`, `"lose"`, or `"tie"` from the player's perspective.

If both players choose the same move, the function returns `"tie"`.

Otherwise, the function uses the winning relationships:

- Rock beats Scissors.
- Paper beats Rock.
- Scissors beats Paper.

If the player's move beats the computer's move, the function returns `"win"`. Otherwise, it returns `"lose"`.

The implementation handles all nine possible combinations.

I preserved the supplied Flask application and game interface.

### Unit Testing

I added unit tests in `tests/test_game.py` to verify all nine possible outcomes.

The tests check wins, losses, and ties using the actual `determine_winner()` function.

All nine outcome tests passed.

### Integration Testing

I added integration tests in `tests/test_game.py` to verify that the Flask application processes a submitted move and displays the correct result.

The positive integration test fixes the computer's random move to Scissors and submits Rock.

The expected result is `"You win!"`, because Rock beats Scissors.

I also tested missing and unsupported moves to verify that the server returns HTTP 400 with a helpful error message.

These tests passed.

### Real-Browser Testing

I added `tests/e2e/test_round.py` using Playwright and the supplied browser fixtures.

The test opens the actual application in a browser and plays two rounds.

**Round 1:**

- Player: Rock
- Computer: Scissors
- Expected result: Win
- Verified result: You win!

**Round 2:**

- Player: Scissors
- Computer: Rock
- Expected result: Lose
- Verified result: Computer wins

The test also verifies that the displayed choices update and only the current round's result is shown.

The real game rules are used. Only the computer's random choices are controlled.

All six browser tests passed, including the supplied tests.

### Automated Check Results

I ran the full project check using:

`PYTEST_ADDOPTS="--browser chromium --browser-channel chrome" .venv/bin/python check.py`

Results:

| Check | Result |
| --- | --- |
| Black formatting | PASS |
| Pylint code analysis | PASS |
| Non-browser pytest | 25 passed |
| Real-browser pytest | 6 passed |
| Total automated tests | 31 passed |

The full check completed successfully with the message:

`All configured checks passed.`

I used the installed Google Chrome browser because Playwright's bundled Chromium was not supported on my Mac's operating system.

### Manual Browser Testing

I started the application using:

`.venv/bin/python -m flask --app app run --port 5050`

I opened the game in Chrome at:

`http://127.0.0.1:5050`

I manually played a round with these results:

- My move: Rock
- Computer's move: Scissors
- Displayed result: Win
- Expected result: Win

The displayed result was correct because Rock beats Scissors.

I also played another round and confirmed that replay worked without restarting the application.

I tested keyboard controls using Tab and Enter. The controls worked successfully.

### Testing and Debugging Reflection

During testing, Black reported formatting issues in three Python files, and Pylint reported a trailing-newline warning in `game.py`.

I fixed these issues by running Black on the modified Python files and then reran the full checks.

I also encountered a browser compatibility issue because Playwright's bundled Chromium was not supported on my Mac.

I resolved this local testing issue by configuring pytest to use my installed Chrome browser.

The automated tests helped verify that the game rules were correct for all nine combinations and that invalid requests were handled correctly.

The manual browser test confirmed that the interface displayed the expected result and supported replay and keyboard interaction.

One important test was the Rock-versus-Scissors unit test. It checked that `determine_winner("rock", "scissors")` returned `"win"`. This verified one of the basic winning relationships used by the game.

### AI Assistance

I used ChatGPT to help develop the implementation plan, write the game rules, create unit and integration tests, add real-browser testing, and troubleshoot formatting and browser compatibility problems.

I reviewed the code by running the automated checks and manually playing the game.

### Work Record

- **Issue:** https://github.com/rm996/is218-rps-game/issues/1
- **Branch:** `rps-001`
- **Implementation:** Completed in `game.py`.
- **Unit and integration tests:** `tests/test_game.py`
- **Real-browser tests:** `tests/e2e/test_round.py`
- **Checks:** PASS - Black, Pylint, 25 non-browser tests, and 6 browser tests.
- **Manual verification:** Rock beat Scissors, replay worked, and keyboard controls worked.
- **Pull request:** https://github.com/rm996/is218-rps-game/pull/2
- **CI:** Add the URL of the successful GitHub Actions run.
- **Final status:** Implementation, local testing, and initial GitHub Actions checks passed. Final review and merge are pending.
