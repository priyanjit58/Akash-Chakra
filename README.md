# ⚡ AKASH CHAKRA

### Belief-Aware Predictive Spectrum Intelligence for Adaptive Electronic Warfare

<p align="center">

**AKASH CHAKRA**
*Powered by BAPS — Belief-Aware Predictive Scan Scheduler*

</p>

<p align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](#)
[![PyTorch](https://img.shields.io/badge/PyTorch-ML-EE4C2C?style=for-the-badge\&logo=pytorch\&logoColor=white)](#)
[![EW](https://img.shields.io/badge/EW-Spectrum%20Intelligence-111827?style=for-the-badge)](#)
[![BAPS](https://img.shields.io/badge/Core-BAPS-00C9D7?style=for-the-badge)](#)
[![Prototype](https://img.shields.io/badge/Status-Research%20Prototype-22C55E?style=for-the-badge)](#)

</p>

> **AKASH CHAKRA is a research prototype for intelligent spectrum sensing that continuously observes the RF environment, maintains a belief about emitter activity, predicts future activity, and adaptively schedules the next scan using BAPS.**

---

# 🛰️ The Big Picture

```text
                         ⚡ AKASH CHAKRA
                               │
                               ▼
                    ┌────────────────────┐
                    │   RF ENVIRONMENT   │
                    │                    │
                    │  Dynamic Emitters  │
                    │  Signals / Noise   │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │    ESM RECEIVER    │
                    │                    │
                    │ Spectrum • PDWs    │
                    │ Time • Power       │
                    └─────────┬──────────┘
                              │
                              ▼
                 ╔══════════════════════════╗
                 ║          BAPS            ║
                 ║                          ║
                 ║ Belief → Prediction      ║
                 ║ Uncertainty → Scheduling ║
                 ╚════════════╤═════════════╝
                              │
                              ▼
                    ┌────────────────────┐
                    │ ADAPTIVE SCANNER   │
                    │                    │
                    │ Frequency + Dwell  │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │   DETECTION        │
                    │                    │
                    │     HIT / MISS     │
                    └─────────┬──────────┘
                              │
                              ▼
                         ┌─────────┐
                         │  LEARN  │
                         └────┬────┘
                              │
                              └──────────► 🔄
```

---

# 🧠 What Makes AKASH CHAKRA Different?

Traditional scanning:

```text
F1 → F2 → F3 → F4 → F5 → F6 → F7 → F8
```

AKASH CHAKRA:

```text
       OBSERVE
          ↓
    UPDATE BELIEF
          ↓
       PREDICT
          ↓
   ┌───────────────┐
   │ BAPS DECISION │
   └───────┬───────┘
           ↓
     SELECT BAND
           ↓
      SELECT DWELL
           ↓
        SCAN
           ↓
      HIT / MISS
           ↓
        LEARN
           ↺
```

### The key idea:

> **Don't scan everything equally. Decide what is worth scanning next.**

---

# 🧠 BAPS — The Intelligence Behind AKASH CHAKRA

## Belief-Aware Predictive Scan Scheduler

BAPS is the **decision-making engine** of AKASH CHAKRA.

It answers three questions:

```text
┌─────────────────────────────────────┐
│  1. WHERE should we scan?           │
│                                     │
│  2. WHEN should we revisit it?      │
│                                     │
│  3. HOW LONG should we dwell?       │
└─────────────────────────────────────┘
```

BAPS combines:

| Intelligence            | Purpose                                       |
| ----------------------- | --------------------------------------------- |
| 🧠 **Belief State**     | What do we currently believe about each band? |
| 🔮 **Prediction**       | Where is activity likely to occur next?       |
| ❓ **Uncertainty**       | What do we still not know?                    |
| 🔄 **Revisit Urgency**  | Which bands need another look?                |
| 💡 **Information Gain** | Which scan could teach us the most?           |
| ⚙️ **Switching Cost**   | How expensive is changing frequency?          |

The prototype explicitly exposes these components in its **BAPS score breakdown**.

---

# 🎯 BAPS Decision Engine

```text
                  CANDIDATE BAND
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
     Prediction     Uncertainty    Revisit
          │             │             │
          └─────────────┼─────────────┘
                        ↓
                 Information Gain
                        │
                        ↓
                 Switching Cost
                        │
                        ▼
              ┌─────────────────┐
              │   BAPS SCORE    │
              └────────┬────────┘
                       ↓
                Highest Value
                       ↓
                NEXT SCAN
```

Conceptually:

```text
BAPS(f) =
    Activity Prediction
  + Uncertainty
  + Revisit Urgency
  + Information Gain
  − Switching Cost
```

The prototype visualizes these individual terms before presenting the selected frequency and recommended dwell time.

---

# 📡 AKASH CHAKRA OPERATOR VIEW

The prototype is designed as a spectrum-operations console rather than a simple ML demo.

```text
┌─────────────────────────────────────────────────────────────┐
│                    ⚡ AKASH CHAKRA                          │
│          BELIEF-AWARE SPECTRUM OPERATIONS                   │
├────────────────────────────┬────────────────────────────────┤
│                            │                                │
│     🌈 LIVE SPECTRUM       │       🧠 BAPS DECISION         │
│                            │                                │
│ Frequency × Time           │  NEXT BAND                    │
│ Activity Heatmap            │  Frequency                    │
│                            │  Dwell                        │
│                            │  Prediction                   │
│                            │  Uncertainty                  │
├────────────────────────────┼────────────────────────────────┤
│                            │                                │
│      📡 RADAR              │       📈 SIGINT               │
│                            │                                │
│ Detection Sweep             │ Waterfall                    │
│                            │ Oscilloscope                  │
├────────────────────────────┴────────────────────────────────┤
│                                                              │
│ CURRENT SCAN       │ TRACKS       │ EVENT / DECISION LOG    │
│ Frequency          │ Contacts     │ Observe                 │
│ Dwell              │ Hits         │ Predict                 │
│ HIT / MISS         │ Misses       │ Schedule                │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│             ⚖️ BAPS vs BASELINE POLICIES                    │
├──────────────────────────────────────────────────────────────┤
│ BAPS │ Sequential │ Random │ Greedy                         │
├──────────────────────────────────────────────────────────────┤
│       🧠 BELIEF STATE + CLOSED LOOP REASONING               │
└──────────────────────────────────────────────────────────────┘
```

These elements correspond directly to the uploaded prototype, including the spectrum heatmap, BAPS decision panel, radar, waterfall, current scan, tracks, event log, baseline comparison, belief state and closed-loop reasoning panels.

---

# 🔥 Core Features

### 🌈 Live Spectrum Intelligence

```text
Frequency
   ↑
   │     ███
   │  ██ ████
   │ █████████
   │   ███
   └────────────────→ Time
```

Tracks activity across frequency and time.

The prototype implements a **Frequency × Time Activity Map** with the current scan highlighted.

---

### 🧠 BAPS Decision Panel

```text
        ┌───────────────┐
        │   B-07        │
        │   NEXT        │
        └──────┬────────┘
               ↓
          3.91 GHz
            80 ms
```

Shows:

* Selected band
* Frequency
* Recommended dwell
* Predicted activity
* Uncertainty
* Revisit urgency
* Information gain
* Switching cost
* Total decision score

---

### 📡 Radar Detection

```text
                 ·
           ·           ·

        ·       ◉       ·

           ·           ·
                 ·
```

Provides a visual representation of detections and activity during the simulation.

The prototype includes a live 2D radar sweep.

---

### 🌊 SIGINT Waterfall

```text
TIME ↓

████░░██░░░████
██░░░████░░██░░
░░████░░████░░░
████░░██████░░
```

Maintains a rolling history of spectral activity.

---

# 🔄 Closed-Loop BAPS

The heart of AKASH CHAKRA:

```text
             ┌──────────────┐
             │   OBSERVE    │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │    UPDATE    │
             │    BELIEF    │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │   PREDICT    │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │    SCORE     │
             │   BAPS       │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │     SCAN     │
             └──────┬───────┘
                    ↓
              ┌─────┴─────┐
              ↓           ↓
            HIT          MISS
              │           │
              └─────┬─────┘
                    ↓
             ┌──────────────┐
             │    LEARN     │
             └──────┬───────┘
                    │
                    └────────────► OBSERVE
```

The prototype represents this explicitly as:

**OBSERVE → UPDATE → PREDICT → SCORE → SCAN → LEARN**.

---

# 📊 Performance Evaluation

AKASH CHAKRA evaluates adaptive scanning using:

```text
                 PERFORMANCE
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
       PI           AIT       Detection
        │            │            │
 Probability    Average Time   Hit Rate
 of Intercept   to Intercept
```

Additional measurements:

* False Alarm Rate
* Scan Cycles
* Hits / Misses
* Scan efficiency
* Band coverage
* Belief convergence

The prototype exposes PI, AIT, detection probability, false-alarm rate and scan cycles as live metrics.

---

# ⚖️ BAPS vs Baselines

AKASH CHAKRA does not evaluate BAPS in isolation.

```text
                 SAME RF ENVIRONMENT
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
      Sequential       Random         Greedy
          │              │              │
          └──────────────┼──────────────┘
                         ↓
                       BAPS
                         │
                         ▼
                  PERFORMANCE
                   COMPARISON
```

### Policies

| Policy            | Strategy                          |
| ----------------- | --------------------------------- |
| 🧠 **BAPS**       | Belief + prediction + uncertainty |
| ➡️ **Sequential** | Fixed scan order                  |
| 🎲 **Random**     | Random band selection             |
| 🎯 **Greedy**     | Select highest current belief     |

The prototype provides a live baseline table comparing **PI, AIT, hits and efficiency**.

---

# 🔮 Prediction + Belief

```text
Past Observations
       │
       ▼
┌───────────────┐
│ Temporal Model│
└───────┬───────┘
        ↓
 Future Activity
        │
        ├────────► Prediction
        │
        └────────► Uncertainty
                         │
                         ▼
                  ┌────────────┐
                  │    BAPS    │
                  └────────────┘
```

BAPS therefore does not simply react to the previous scan.

It uses the **current belief state + predicted activity + uncertainty** to determine the next sensing action.

---

# 📡 Signal Intelligence Layer

```text
        RF Environment
              │
              ▼
          ESM Receiver
              │
              ▼
             PDWs
              │
              ▼
       Temporal Model
          / Transformer
              │
              ▼
       Feature Representation
              │
              ▼
           HDBSCAN
              │
              ▼
      Signal Grouping /
       Deinterleaving
```

This creates the downstream intelligence layer after adaptive sensing.

---

# 🧩 Complete AKASH CHAKRA Architecture

```text
                         ⚡ AKASH CHAKRA
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
   RF SIMULATION           ESM RECEIVER            SCENARIOS
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                ▼
                              PDWs
                                │
                                ▼
                     ┌────────────────────┐
                     │       BAPS         │
                     │                    │
                     │ Belief             │
                     │ Prediction         │
                     │ Uncertainty        │
                     │ Information Gain   │
                     │ Revisit Urgency    │
                     └─────────┬──────────┘
                               │
                               ▼
                       Adaptive Scan
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
                  HIT                   MISS
                    │                     │
                    └──────────┬──────────┘
                               ▼
                          Belief Update
                               │
                               └─────────► 🔄
```

---

# 🖥️ Prototype

The current prototype provides:

```text
🎛️ Operator Console
      │
      ├── 🌈 Spectrum Heatmap
      ├── 🧠 BAPS Decision Engine
      ├── 📡 Radar
      ├── 🌊 SIGINT Waterfall
      ├── 📈 Oscilloscope
      ├── 🎯 Current Scan
      ├── 📍 Track Summary
      ├── 📝 Event Timeline
      ├── ⚖️ Baseline Comparison
      ├── 🧮 Belief State
      ├── 🔄 Closed-Loop Reasoning
      └── 📤 Run Export
```

The prototype also supports configurable scenarios including **mixed/agile, periodic, frequency hopping, emerging emitter and dense multi-emitter** conditions.

---

# 🧪 Simulation Scenarios

```text
🚀 AGILE MIXED
      ↓
🦘 FREQUENCY HOPPING
      ↓
📡 PERIODIC EMITTER
      ↓
🌊 DENSE MULTI-EMITTER
      ↓
⚠️ EMERGING EMITTER
```

These scenarios allow BAPS to be tested under different temporal spectrum behaviors.

---

# 🛠️ Technology Stack

```text
                    AKASH CHAKRA
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
      Python           PyTorch          Flask
        │                │                │
        │          Prediction            API
        │
        ├── NumPy
        ├── HDBSCAN
        └── Simulation
                         │
                         ▼
                HTML / CSS / JS
                         │
                         ▼
                  OPERATOR UI
```

---

# 📁 Repository Structure

```text
AKASH-CHAKRA/
│
├── 📄 README.md
├── 📄 requirements.txt
│
├── 📁 backend/
│   ├── app.py
│   │
│   ├── 📁 baps/
│   │   ├── belief.py
│   │   ├── predictor.py
│   │   ├── scoring.py
│   │   └── scheduler.py
│   │
│   ├── 📁 environment/
│   │   ├── rf_environment.py
│   │   └── emitters.py
│   │
│   ├── 📁 signal/
│   │   ├── pdw.py
│   │   ├── transformer.py
│   │   └── deinterleaving.py
│   │
│   └── 📁 baselines/
│       ├── sequential.py
│       ├── random.py
│       └── greedy.py
│
├── 📁 frontend/
│   ├── index.html
│   ├── style.css
│   └── dashboard.js
│
├── 📁 simulation/
│   ├── environment.py
│   ├── scenarios.py
│   └── generate_data.py
│
├── 📁 experiments/
│   ├── evaluate_baps.py
│   ├── compare_baselines.py
│   └── metrics.py
│
├── 📁 models/
│   └── transformer/
│
├── 📁 results/
│   ├── figures/
│   ├── metrics/
│   └── logs/
│
└── 📁 docs/
    ├── architecture.md
    ├── methodology.md
    └── experiments.md
```

---

# 🚀 Quick Start

```bash
git clone <YOUR-REPOSITORY-URL>

cd AKASH-CHAKRA

pip install -r requirements.txt

python backend/app.py
```

Then open:

```text
http://localhost:5000
```

---

# 🔬 Research Roadmap

```text
                 CURRENT
                    │
                    ▼
             Simulation World
                    │
                    ▼
                BAPS v1
                    │
                    ▼
           Dashboard Prototype
                    │
                    ▼
          Baseline Evaluation
                    │
                    ▼
              ┌───────────┐
              │   NEXT    │
              └─────┬─────┘
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
     POMDP         OOD        Ablation
       │            │            │
       └────────────┼────────────┘
                    ▼
          Uncertainty-Aware
             BAPS v2
                    │
                    ▼
              SDR / RF Test
```

---

# 🎯 Vision

### From

```text
SCAN → DETECT
```

### To

```text
OBSERVE
   ↓
UNDERSTAND
   ↓
PREDICT
   ↓
DECIDE
   ↓
SCAN
   ↓
LEARN
   ↺
```

**AKASH CHAKRA** aims to turn spectrum sensing from a largely reactive scanning process into an **adaptive, belief-aware and prediction-guided sensing loop**.

---

# ⚠️ Research Prototype Notice

AKASH CHAKRA is a **simulation/research prototype**.

The current dashboard models RF activity and receiver behavior for experimentation and evaluation. Prototype values should not be interpreted as measurements from a deployed operational EW system.

---

# 📚 Keywords

`Akash Chakra` · `BAPS` · `Electronic Warfare` · `Spectrum Intelligence` · `Adaptive Spectrum Sensing` · `Predictive Scheduling` · `RF Environment` · `ESM` · `PDW` · `Transformer` · `HDBSCAN` · `Signal Deinterleaving` · `Belief State` · `Uncertainty` · `POMDP` · `Machine Learning`

---

# ⭐ AKASH CHAKRA

```text
╔══════════════════════════════════════════════╗
║                                              ║
║             ⚡ AKASH CHAKRA ⚡                ║
║                                              ║
║       BELIEVE • PREDICT • ADAPT • LEARN      ║
║                                              ║
║              Powered by BAPS                 ║
║                                              ║
╚══════════════════════════════════════════════╝
```

> **BAPS is the brain.
> The RF environment is the world.
> The receiver is the sensor.
> AKASH CHAKRA is the complete adaptive intelligence loop.**
