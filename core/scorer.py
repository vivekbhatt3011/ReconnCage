import json

class Scorer:
    def __init__(self, logger=None):
        self.logger = logger

    # =========================
    # MAIN SCORING FUNCTION
    # =========================
    def score_targets(self, context, intel_dir):
        """
        Assign scores to alive targets based on heuristics.
        """

        if self.logger:
            self.logger.start_phase("Target Scoring")

        scores = {}

        for url in context.alive:
            score = 0

            # -------------------------
            # 1. High-value keywords
            # -------------------------
            if any(k in url.lower() for k in ["admin", "login", "dashboard"]):
                score += 5

            # -------------------------
            # 2. Technology-based scoring
            # -------------------------
            tech = context.tech.get(url, "").lower()

            if "wordpress" in tech:
                score += 3

            if "php" in tech:
                score += 2

            # -------------------------
            # 3. Port-based scoring
            # -------------------------
            if context.ports:
                score += len(context.ports)

            # -------------------------
            # 4. Depth / complexity (basic)
            # -------------------------
            if url.count("/") > 3:
                score += 1

            scores[url] = score

        context.score = scores

        # -------------------------
        # SAVE OUTPUT
        # -------------------------
        with open(intel_dir / "scores.json", "w") as f:
            json.dump(scores, f, indent=4)

        # -------------------------
        # HIGH VALUE TARGETS
        # -------------------------
        high_value = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        with open(intel_dir / "high_value.txt", "w") as f:
            for url, score in high_value:
                f.write(f"{url} -> {score}\n")

        if self.logger:
            self.logger.success("Scoring completed")

        if self.logger:
            self.logger.end_phase("Target Scoring")