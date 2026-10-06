# Offline continuation labs

These programs use constructed fixtures and the Python standard library. They perform no network calls and use no real credentials or external side effects.

```sh
python3 examples/curriculum-v3/engineering_service.py
python3 examples/curriculum-v3/research_calculations.py
python3 scripts/verify-v3-continuation.py
```

`engineering_service.py` supports Grade 11 request/schema checks, authorisation, pure functions, integration traces, cache rules, state transitions, retry budgets and an in-memory idempotency exercise. The role argument simulates a trusted server session; it is not a login mechanism. The ledger is not durable and does not claim production delivery guarantees.

`research_calculations.py` supports Grade 12 sampling variability, known-sigma intervals, paired effects, tiny exact sign-flip tests and multiple-comparison decisions. Read each function's assumptions before applying it. The known-sigma interval assumes independent normal sampling with known population sigma. The sign-flip exercise requires independent symmetric sign exchangeability.

Student activity: run a relevant function on a supplied worked case, predict a new boundary case before execution, preserve both outputs and state the limitation. Do not open the verification script before submitting independent workbook tasks; it contains teacher checking values.
