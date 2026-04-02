from pathlib import Path

# Core
from core.context import Context
from core.runner import Runner
from core.logger import Logger
from core.detector import Detector
from core.scorer import Scorer

# Modules
from modules.passive import subfinder, wayback
from modules.active import httpx, nuclei, ffuf, nmap


def create_directories(base_path: Path):
    """
    Create runtime directory structure.
    """

    raw = base_path / "raw"
    refined = base_path / "refined"
    intel = base_path / "intel"
    logs = base_path / "logs"

    for d in [raw, refined, intel, logs]:
        d.mkdir(parents=True, exist_ok=True)

    return raw, refined, intel, logs


def main():
    # =========================
    # INPUT
    # =========================
    target = input("Enter target domain: ").strip()

    # =========================
    # RUNTIME PATH
    # =========================
    base_path = Path.cwd() / target

    raw_dir, refined_dir, intel_dir, logs_dir = create_directories(base_path)

    log_file = logs_dir / f"{target}.txt"

    # =========================
    # INIT CORE COMPONENTS
    # =========================
    logger = Logger(log_file)
    runner = Runner(logger)
    context = Context(target)

    detector = Detector(runner, logger)
    scorer = Scorer(logger)

    logger.info(f"Recon started for {target}")

    # =========================
    # DETECTION PHASE
    # =========================
    safe_mode = detector.detect_protection(target, raw_dir)

    # =========================
    # PASSIVE RECON
    # =========================
    subfinder.execute(context, runner, logger, raw_dir, refined_dir)
    wayback.execute(context, runner, logger, raw_dir, refined_dir)

    # =========================
    # ACTIVE RECON
    # =========================
    nmap_proc = nmap.execute(context, runner, logger, raw_dir, refined_dir, safe_mode)

    httpx.execute(context, runner, logger, raw_dir, refined_dir)
    nuclei.execute(context, runner, logger, raw_dir, refined_dir)
    ffuf.execute(context, runner, logger, raw_dir, refined_dir)

    # Wait for Nmap if running in background
    if nmap_proc:
        runner.wait(nmap_proc)

    nmap.process_results(context, runner, logger, raw_dir, refined_dir)

    # =========================
    # INTELLIGENCE
    # =========================
    scorer.score_targets(context, intel_dir)

    # Save full context
    import json
    with open(intel_dir / "context.json", "w") as f:
        json.dump(context.to_dict(), f, indent=4)

    logger.success("Recon completed successfully")


# =========================
if __name__ == "__main__":
    main()