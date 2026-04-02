from pathlib import Path


def execute(context, runner, logger, raw_dir: Path, refined_dir: Path):
    """
    Run FFUF fuzzing using Wayback URLs as input.
    """

    logger.start_phase("FFUF")

    urls_file = refined_dir / "urls.txt"
    output_file = raw_dir / "ffuf.txt"

    # -------------------------
    # BASIC SAFETY CHECK
    # -------------------------
    if not urls_file.exists():
        logger.warning("No URLs found for FFUF. Skipping...")
        logger.end_phase("FFUF")
        return

    # -------------------------
    # RUN TOOL
    # -------------------------
    command = f"ffuf -w {urls_file} -u FUZZ"

    runner.run(command, output_file)

    logger.success("FFUF scan completed")
    logger.end_phase("FFUF")