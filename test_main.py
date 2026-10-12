
import unittest


def kruskal(locations, edges):
    parent = {location: location for location in locations}

    def find(location):
        if parent[location] != location:
            parent[location] = find(parent[location])
        return parent[location]

    mst = []
    total = 0

    for cost, start, end in sorted(edges):
        root_start = find(start)
        root_end = find(end)

        if root_start != root_end:
            parent[root_start] = root_end
            mst.append((start, end, cost))
            total += cost

            if len(mst) == len(locations) - 1:
                break

    if len(mst) != len(locations) - 1:
        raise ValueError("Graph is disconnected")

    return mst, total


class TestKruskal(unittest.TestCase):

    def test_sample_graph(self):
        locations=[
            "divili",
            "virava",
            "mallam",
            "pullimeru",
            "gorinta"
        ]
        edges = [
            (4,"gorinta","pullimeru"),
            (2,"pullimeru","divili"),
            (3,"divili","virava"),
            (2.5,"virava","mallam"),
            (3,"mallam","gorinta"),
            (2,"pullimeru","virava")
        ]

        mst, total = kruskal(locations, edges)

        self.assertEqual(len(mst), 4)
        self.assertEqual(total, 9.5)

    def test_disconnected_graph(self):
        locations = ["divili", "virava", "mallam"]
        edges = [(3, "divili", "virava")]

        with self.assertRaises(ValueError):
            kruskal(locations, edges)

    def test_cycle_is_avoided(self):
        locations = ["divili", "virava", "mallam"]
        edges = [
            (1, "divili", "virava"),
            (2, "virava", "mallam"),
            (3, "divili", "mallam"),
        ]

        mst, total = kruskal(locations, edges)

        self.assertEqual(len(mst), 2)
        self.assertEqual(total, 3)


if __name__ == "__main__":
    unittest.main()
