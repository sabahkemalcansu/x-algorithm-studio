# extensions/

Safe sandbox for community / agent work. **English only.**

```text
scorers/   # explain.py, reweight.py
filters/   # demo-only filters (add here)
```

```bash
make demo-fixture
make explain
python3 extensions/scorers/reweight.py --weights presets/weights/anti_negative.json
```

See `docs/extend-guide.md`, `docs/agent-loop.md`, and `agent/tasks/`.
