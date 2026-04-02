from pathlib import Path


def execute(context, runner, logger, raw_dir: Path, refined_dir: Path):
    """
    Run HTTPX to identify live hosts and technologies.
    """

    logger.start_phase("HTTPX")

    input_file = refined_dir / "subs.txt"
    output_file = raw_dir / "httpx.txt"

    # -------------------------
    # RUN TOOL
    # -------------------------
    result = runner.run(
        f"httpx -tech -silent -l {input_file}",
        output_file
    )

    alive_hosts = []
    tech_map = {}

    # -------------------------
    # PROCESS OUTPUT
    # -------------------------
    if result:
        for line in result.splitlines():
            parts = line.strip().split(" ")

            if not parts:
                continue

            url = parts[0]
            tech = " ".join(parts[1:]) if len(parts) > 1 else ""

            alive_hosts.append(url)
            tech_map[url] = tech

    # Deduplicate
    alive_hosts = list(set(alive_hosts))

    # -------------------------
    # UPDATE CONTEXT
    # -------------------------
    context.add_alive(alive_hosts)
    context.add_tech(tech_map)

    # -------------------------
    # SAVE REFINED OUTPUT
    # -------------------------
    refined_file = refined_dir / "alive.txt"

    with open(refined_file, "w") as f:
        for host in context.alive:
            f.write(host + "\n")

    logger.success(f"HTTPX found {len(context.alive)} alive hosts")
    logger.end_phase("HTTPX")