# Chat Export & Statistics Dashboard

## Features
- Export chat history as JSON (with timestamps) and Markdown (human-readable)
- View chat statistics: total messages, most used assistant, average messages per session, time ranges

## Usage
1. Use the export button in the UI to download chat history as JSON or Markdown.
2. Visit the `Stats` page to view chat metrics.

## Testing
Run unit tests:
```
python -m unittest tests/test_export.py
```

## Implementation
- Export helpers: `app/utils/export.py`
- Stats dashboard: `pages/stats.py`
- Tests: `tests/test_export.py`
