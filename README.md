# BCI Feedback Module

This package contains the feedback module for a Brain-Computer Interface (BCI) based on the CVSA (Covert Visuospatial Attention) paradigm. It manages the experimental protocol, visual/audio stimuli presentation, and user reaction time logging.

The system is built on **ROS** and utilizes `rosneuro` and `neurodraw` libraries for signal management and graphical rendering.

---

## 📦 Dependencies

Before compiling, ensure you have the necessary audio libraries installed for the feedback generation systems:

```bash
sudo apt-get install libao-dev libsndfile1-dev
```

---

## 🚀 System Architecture

The package consists of two main active nodes:

### 1. Main Node: `trainingCVSA_node`
This C++ node orchestrates the entire BCI protocol. It subscribes to the classifier's predictions (`/cvsa/neuroprediction/integrated`) and publishes state events (`/events/bus`).

* **Feedback Engine:** Generates continuous audio feedback using `libao` and visual feedback using `neurodraw`.
* **Operating Modes**:
    * **Calibration:** Uses an internal **Autopilot** (Linear or Sine wave) to simulate input signals and gather training data.
    * **Evaluation:** Uses real-time classifier output to control the feedback.
* **Hardware Integration:** Can optionally trigger a **UR5 Robot**, synchronize with an **IMU**, or manage **Eye-tracker** calibration.

### 2. Reaction Logger: `reaction_logger`
A standalone Python node (`keyboard_node.py`) designed to measure user alertness.

* **Trigger:** Listens for "Boom" events (codes 897, 898, 899) on the event bus.
* **Action:** Records the timestamp when the user presses the **Spacebar**.
* **Output:** Saves reaction times to a CSV file (e.g., `reaction_time_YYYYMMDD.csv`) in the user's home directory (or specified path).

---

## 🧠 Protocol Workflow

Each trial follows a strict timing sequence managed by `TrainingCVSA.cpp`:

1.  **Fixation:** A cross appears; the user focuses on the center.
2.  **Cue:** An audio or visual cue indicates the required attention direction (Left/Right).
3.  **Continuous Feedback (CF):**
    * The user hears a sound (pitch/volume changes based on the `audio_increasing` parameter).
    * Visual feedback (center cursor) is displayed.
    * This phase ends when a threshold is reached or a timeout occurs.
4.  **The "Boom" & Reaction Time:**
    * A visual target (dot) appears in the detected direction (Left/Right).
    * **User Task:** Press the **Spacebar** immediately upon hearing the Boom/seeing the target.
    * **Constraint:** The valid window for this reaction is strictly limited to the **duration of the boom sound** (default: 1.5s). If the user presses the key after this window, the reaction is not recorded or considered invalid.

---

## ⚙️ Configuration Parameters

The system is highly configurable via ROS parameters (usually loaded via `.launch` files).

### General Settings
* `classes`: List of class IDs (e.g., `[730, 731]`).
* `modality`: Operation mode, either `"calibration"` or `"evaluation"`.
* `thresholds`: Probability thresholds (0.0 - 1.0) to trigger a selection.
* `trials`: Number of trials per class.

### Audio Feedback
* `audio_path`: Directory containing the `.wav` files.
* `audio_increasing`:
    * `true`: Audio intensity increases with classifier confidence.
    * `false`: Audio intensity decreases or logic is inverted.
* `audio_cue`: If `true`, uses sound instead of visual squares for cues.

### Visual Layout
* `circlePositions`: Matrix defining the X/Y coordinates for the targets.

### Durations (ms)
Defined under the `~duration/` namespace:
* `fixation`: Time for the fixation cross (Default: 2000).
* `cue`: Duration of the instruction cue (Default: 1000).
* `boom`: Duration of the final feedback/reaction window (Default: 1500).
* `timeout`: Max time allowed for a decision in evaluation (Default: 10000).

---

## 📊 Data Output

* **Events:** Published on `/events/bus` for EEG synchronization (Start, Fixation, Cue, CF, Hit/Miss, Stop).
* **CSV Logs:** Reaction times are stored in `~/reaction_time_<timestamp>.csv` formatted as:
    ```csv
    trial,Reaction_Time_Sec
    1,0.453200
    2,0.612000
    ```

## 🕹️ Usage

1.  **Launch the System:**
    Use the provided launch files (in the `launchers_bci` repo) to start the `trainingCVSA_node` with your desired configuration.

2.  **Operation:**
    * Follow the audio/visual cues.
    * When the **Boom** sound plays and the target appears, press **Spacebar** as fast as possible within the 1.5s window.