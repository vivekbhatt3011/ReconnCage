from pathlib import Path


def execute(context, runner, logger, raw_dir: Path, refined_dir: Path):
    """
    Run Wayback URLs and update context with discovered URLs.
    """

    logger.start_phase("Wayback URLs")

    output_file = raw_dir / "wayback.txt"

    # -------------------------
    # RUN TOOL
    # -------------------------
    result = runner.run(
        f"waybackurls {context.target}",
        output_file
    )

    # -------------------------
    # PROCESS OUTPUT
    # -------------------------
    urls = []

    if result:
        for line in result.splitlines():
            url = line.strip()
            if url:
                urls.append(url)

    # Deduplicate
    urls = list(set(urls))

    # -------------------------
    # UPDATE CONTEXT
    # -------------------------
    context.add_urls(urls)

    # -------------------------
    # SAVE REFINED OUTPUT
    # -------------------------
    refined_file = refined_dir / "urls.txt"

    with open(refined_file, "w") as f:
        for url in context.urls:
            f.write(url + "\n")

    logger.success(f"Wayback found {len(context.urls)} unique URLs")
    logger.end_phase("Wayback URLs")