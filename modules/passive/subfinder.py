from pathlib import Path


def execute(context, runner, logger, raw_dir: Path, refined_dir: Path):
    """
    Run Subfinder and update context with discovered subdomains.
    """

    logger.start_phase("Subfinder")

    output_file = raw_dir / "subfinder.txt"

    # -------------------------
    # RUN TOOL
    # -------------------------
    result = runner.run(
        f"subfinder -d {context.target}",
        output_file
    )

    # -------------------------
    # PROCESS OUTPUT
    # -------------------------
    subdomains = []

    if result:
        for line in result.splitlines():
            sub = line.strip()
            if sub:
                subdomains.append(sub)

    # -------------------------
    # UPDATE CONTEXT
    # -------------------------
    context.add_subdomains(subdomains)

    # -------------------------
    # SAVE REFINED OUTPUT
    # -------------------------
    refined_file = refined_dir / "subs.txt"

    with open(refined_file, "w") as f:
        for sub in context.subdomains:
            f.write(sub + "\n")

    logger.success(f"Subfinder found {len(context.subdomains)} subdomains")
    logger.end_phase("Subfinder")