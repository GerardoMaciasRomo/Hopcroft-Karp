from copy import deepcopy


class HopcroftKarp(object):
    def __init__(self, graph):

        self._matching = {}
        self._dfs_paths = []
        self._dfs_parent = {}

        self._graph = deepcopy(graph)
        self._left = set(self._graph.keys())
        self._right = set()

        for value in self._graph.values():
            self._right.update(value)
        for vertex in self._left:
            for neighbour in self._graph[vertex]:
                if neighbour not in self._graph:
                    self._graph[neighbour] = set()
                    self._graph[neighbour].add(vertex)
                else:
                    self._graph[neighbour].add(vertex)

    def __bfs(self):
        layers = []
        layer = set()
        for vertex in self._left:
            if vertex not in self._matching:
                layer.add(vertex)
        layers.append(layer)
        visited = set()
        while True:

            layer = layers[-1]
            new_layer = set()
            for vertex in layer:
                if vertex in self._left:
                    visited.add(vertex)
                    for neighbour in self._graph[vertex]:
                        if neighbour not in visited and (
                            vertex not in self._matching
                            or neighbour != self._matching[vertex]
                        ):
                            new_layer.add(neighbour)
                else:
                    visited.add(vertex)
                    for neighbour in self._graph[vertex]:

                        if neighbour not in visited and (
                            vertex in self._matching
                            and neighbour == self._matching[vertex]
                        ):
                            new_layer.add(neighbour)
            layers.append(new_layer)

            if len(new_layer) == 0:
                return layers

            if any(
                vertex in self._right and vertex not in self._matching
                for vertex in new_layer
            ):
                return layers

    def __dfs(self, v, index, layers):

        if index == 0:
            path = [v]
            while self._dfs_parent[v] != v:
                path.append(self._dfs_parent[v])
                v = self._dfs_parent[v]
            self._dfs_paths.append(path)
            return True
        for neighbour in self._graph[v]:
            if neighbour in layers[index - 1]:
                if neighbour in self._dfs_parent:
                    continue
                if (
                    neighbour in self._left
                    and (v not in self._matching or neighbour != self._matching[v])
                ) or (
                    neighbour in self._right
                    and (v in self._matching and neighbour == self._matching[v])
                ):
                    self._dfs_parent[neighbour] = v
                    if self.__dfs(neighbour, index - 1, layers):
                        return True
        return False

    def maximum_matching(self, keys_only=False):
        while True:
            layers = self.__bfs()
            if len(layers[-1]) == 0:
                break
            free_vertex = set(
                [vertex for vertex in layers[-1] if vertex not in self._matching]
            )

            del self._dfs_paths[:]
            self._dfs_parent.clear()

            for vertex in free_vertex:

                self._dfs_parent[vertex] = vertex
                self.__dfs(vertex, len(layers) - 1, layers)

            if len(self._dfs_paths) == 0:
                break

            for path in self._dfs_paths:
                for i in range(len(path)):
                    if i % 2 == 0:
                        self._matching[path[i]] = path[i + 1]
                        self._matching[path[i + 1]] = path[i]
        if keys_only:
            self._matching = {
                k: v for k, v in self._matching.items() if k in self._left
            }
        return self._matching
