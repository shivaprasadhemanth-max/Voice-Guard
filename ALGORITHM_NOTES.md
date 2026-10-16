# VoiceGuard AI — Algorithm Notes

## Algorithm used in this prototype
The current prototype uses a **rule-based risk-scoring pipeline** as a placeholder for a trained voice anti-spoofing model. It is NOT a validated deep-learning detector and must not be presented as one.

### Current pipeline
1. Receive an audio upload or analysis request.
2. Derive prototype feature scores for acoustic characteristics, prosody, speaker consistency, and contextual risk.
3. Combine the feature scores using a weighted formula.
4. Convert the result into a risk score and category.
5. Record an incident and allow a response action such as review, verify, callback, MFA, or block.

### Current risk-score formula
`risk = 0.35 × acoustic + 0.30 × prosody + 0.20 × consistency + 0.15 × context + short-duration adjustment`

The present `score_features()` implementation uses deterministic placeholder values rather than analyzing the actual audio waveform. The `/api/analyze-audio` endpoint derives a seed from the file bytes, so its result is a **demo output only**, not evidence that the audio is cloned.

### Intended production algorithm
A validated implementation would decode audio, normalize/resample it, extract features such as log-Mel spectrograms and prosodic statistics, and pass them to a trained anti-spoofing classifier (for example, a CNN or Transformer trained and evaluated on appropriate spoofed/genuine speech datasets). If trusted enrollment samples exist, speaker embeddings may be compared as a separate consistency signal. A calibrated risk layer can then combine classifier confidence and relevant context.

### Important limitations
- CNN/Transformer inference is not currently implemented in this prototype.
- No trained model weights are included.
- The displayed risk score is simulated and must not be used for real financial, identity, or security decisions.
- The incident list is held in memory and is cleared when the backend restarts.

## Run locally
Backend: see `README.md`; requires a compatible Python runtime.
Frontend: install Node.js LTS, then run `npm install` and `npm run dev` inside `frontend`.
