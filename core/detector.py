from core.runner import Runner


class Detector:
    def __init__(self, runner: Runner, logger=None):
        self.runner = runner
        self.logger = logger

    # =========================
    # MAIN DETECTION LOGIC
    # =========================
    def detect_protection(self, target: str, raw_dir):
        """
        Detect WAF / rate limiting and decide execution mode.
        Returns True → SAFE MODE
                False → NORMAL MODE
        """

        if self.logger:
            self.logger.start_phase("WAF / Rate Detection")

        safe_mode = False

        # -------------------------
        # 1. WAF Detection (wafw00f)
        # -------------------------
        waf_output = self.runner.run(
            f"wafw00f {target}",
            raw_dir / "waf.txt"
        )

        if "WAF" in waf_output or "firewall" in waf_output:
            safe_mode = True
            if self.logger:
                self.logger.warning("WAF detected via wafw00f")

        # -------------------------
        # 2. Header Check (curl)
        # -------------------------
        header_output = self.runner.run(
            f"curl -I https://{target}",
            raw_dir / "headers.txt"
        )

        if any(code in header_output for code in ["403", "429"]):
            safe_mode = True
            if self.logger:
                self.logger.warning("Potential rate limiting detected (403/429)")

        # -------------------------
        # 3. Basic Heuristic Check
        # -------------------------
        if "cloudflare" in header_output.lower():
            safe_mode = True
            if self.logger:
                self.logger.warning("Cloudflare detected")

        # -------------------------
        # FINAL DECISION
        # -------------------------
        if safe_mode:
            if self.logger:
                self.logger.warning("SAFE MODE ENABLED (sequential execution)")
        else:
            if self.logger:
                self.logger.success("NORMAL MODE (parallel execution allowed)")

        if self.logger:
            self.logger.end_phase("WAF / Rate Detection")

        return safe_mode