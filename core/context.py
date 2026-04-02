# core/context.py

class Context:
    def __init__(self, target: str):
        self.target = target

        # =========================
        # RAW DISCOVERY DATA
        # =========================
        self.subdomains = []       # from subfinder
        self.urls = []             # from wayback
        self.alive = []            # from httpx
        self.ports = []            # from nmap

        # =========================
        # ENRICHED DATA
        # =========================
        self.tech = {}             # {url: tech stack}
        self.endpoints = []        # extracted endpoints (future)

        # =========================
        # INTELLIGENCE
        # =========================
        self.score = {}            # {url: score}
        self.interesting = []      # key findings

    # =========================
    # HELPER METHODS
    # =========================

    def add_subdomains(self, subs):
        self.subdomains.extend(subs)
        self.subdomains = list(set(self.subdomains))

    def add_urls(self, urls):
        self.urls.extend(urls)
        self.urls = list(set(self.urls))

    def add_alive(self, hosts):
        self.alive.extend(hosts)
        self.alive = list(set(self.alive))

    def add_ports(self, ports):
        self.ports.extend(ports)
        self.ports = list(set(self.ports))

    def add_tech(self, tech_map):
        self.tech.update(tech_map)

    def add_interesting(self, item):
        self.interesting.append(item)

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