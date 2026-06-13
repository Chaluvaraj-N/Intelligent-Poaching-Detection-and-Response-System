# TODO - AnimalPoachingDetectionandresponse enhancements

## Plan (approved)
- [ ] 1) Add `config.json` support (threat classes, confidence threshold, email enabled)
- [ ] 2) Add alert de-duplication / throttling (alerts_log.json)
- [ ] 3) Add risk scoring + severity label in UI and history logging
- [ ] 4) Add history filtering UI (date range, admin, severity, detected object contains)
- [ ] 5) Add history CSV export
- [ ] 6) Improve security: remove hardcoded Gmail app password; use Streamlit secrets/env
- [ ] 7) Speed up video processing: process every Nth frame + Stop button + progress
- [ ] 8) Update README to document new features + setup for SMTP via secrets
- [ ] 9) Quick smoke test (run streamlit, verify upload flows and history)

