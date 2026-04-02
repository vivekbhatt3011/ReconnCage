from pathlib import Path


def execute(context, runner, logger, raw_dir: Path, refined_dir: Path, safe_mode: bool):
    """
    Run Nmap initial scan (all ports).
    """

    logger.start_phase("Nmap Phase 1")

    output_file = raw_dir / "nmap.txt"

    # -------------------------
    # BACKGROUND OR SEQUENTIAL
    # -------------------------
    if safe_mode:
        runner.run(
            f"nmap -p- {context.target}",
            output_file
        )
        process = None
    else:
        process = runner.run_background(
            f"nmap -p- {context.target}",
            output_file
        )

    logger.info("Nmap Phase 1 started")

    return process


def process_results(context, runner, logger, raw_dir: Path, refined_dir: Path):
    """
    Extract open ports and run detailed scan.
    """

    logger.start_phase("Nmap Processing")

    nmap_file = raw_dir / "nmap.txt"
    ports = []

    # -------------------------
    # PARSE OUTPUT
    # -------------------------
    try:
        with open(nmap_file, "r") as f:
            for line in f:
                if "open" in line:
                    port = line.split("/")[0]
                    ports.append(port)
    except FileNotFoundError:
        logger.error("Nmap output not found")
        return

    ports = list(set(ports))

    # -------------------------
    # UPDATE CONTEXT
    # -------------------------
    context.add_ports(ports)

    # -------------------------
    # SAVE REFINED OUTPUT
    # -------------------------
    refined_file = refined_dir / "ports.txt"

    with open(refined_file, "w") as f:
        for port in context.ports:
            f.write(port + "\n")

    logger.success(f"Found {len(context.ports)} open ports")

    # -------------------------
    # DETAILED SCAN (PHASE 2)
    # -------------------------
    if ports:
        ports_str = ",".join(ports)

        runner.run(
            f"nmap -p {ports_str} -sC -sV {context.target}",
            raw_dir / "nmap_detailed.txt"
        )

        logger.success("Nmap detailed scan completed")

    logger.end_phase("Nmap Processing")