class LeafSegmentCounter:
    def __init__(self, name: str, documentation: str):
        self.name = name
        self.documentation = documentation


leaf_segments = LeafSegmentCounter("leaf_segments_total", "Not a Prometheus metric")
