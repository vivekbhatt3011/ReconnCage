class Context:
    def __init__(self, target: str):
        self.target = target

        # Discovery
        self.subdomains = []
        self.urls = []
        self.alive = []
        self.ports = []

        # Enrichment
        self.tech = {}
        self.endpoints = []

        # Intelligence
        self.score = {}
        self.interesting = []

    # -------------------------
    # ADDERS (clean + dedup)
    # -------------------------

    def add_subdomains(self, data):
        self.subdomains = list(set(self.subdomains + data))

    def add_urls(self, data):
        self.urls = list(set(self.urls + data))

    def add_alive(self, data):
        self.alive = list(set(self.alive + data))

    def add_ports(self, data):
        self.ports = list(set(self.ports + data))

    def add_tech(self, data: dict):
        self.tech.update(data)

    def add_interesting(self, item):
        self.interesting.append(item)

    # -------------------------
    # EXPORT
    # -------------------------

    def to_dict(self):
        return {
            "target": self.target,
            "subdomains": self.subdomains,
            "urls": self.urls,
            "alive": self.alive,
            "ports": self.ports,
            "tech": self.tech,
            "score": self.score,
            "interesting": self.interesting
        }