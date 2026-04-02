from pathlib import Path


def execute(context, runner, logger, raw_dir: Path, refined_dir: Path):
    """
    Run Nuclei scan on alive hosts using optional tech-based filtering.
    """

    logger.start_phase("Nuclei")

    input_file = refined_dir / "alive.txt"
    output_file = raw_dir / "nuclei.txt"

    # -------------------------
    # BUILD TAG FILTER (SMART)
    # -------------------------
    tags = set()

    for tech in context.tech.values():
        tech_lower = tech.lower()

        if "wordpress" in tech_lower:
            tags.add("wordpress")

        if "php" in tech_lower:
            tags.add("php")

        if "apache" in tech_lower:
            tags.add("apache")

    tag_flag = ""

    if tags:
        tag_flag = f"-tags {','.join(tags)}"
        logger.info(f"Using Nuclei tags: {tag_flag}")

    # -------------------------
    # RUN TOOL
    # -------------------------
    command = f"nuclei -l {input_file} {tag_flag}"

    runner.run(command, output_file)

    logger.success("Nuclei scan completed")
    logger.end_phase("Nuclei")