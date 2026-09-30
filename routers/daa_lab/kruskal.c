#include <stdio.h>
#include <stdlib.h>

#define MAX 100

struct Edge {
    int u;
    int v;
    int w;
};

int parent[MAX];
int rank[MAX];

/* Find operation */
int find(int x) {
    if (parent[x] != x)
        parent[x] = find(parent[x]);

    return parent[x];
}

/* Union operation */
void unionSet(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);

    if (rootX == rootY)
        return;

    if (rank[rootX] < rank[rootY]) {
        parent[rootX] = rootY;
    }
    else if (rank[rootX] > rank[rootY]) {
        parent[rootY] = rootX;
    }
    else {
        parent[rootY] = rootX;
        rank[rootX]++;
    }
}

/* Compare edges according to weight */
int compare(const void *a, const void *b) {
    struct Edge *e1 = (struct Edge *)a;
    struct Edge *e2 = (struct Edge *)b;

    return e1->w - e2->w;
}

int main() {
    int n, m;
    struct Edge edges[MAX];
    int i;
    int edgeCount = 0;
    int totalCost = 0;

    printf("Enter the Number of Vertices and Edges: ");
    scanf("%d %d", &n, &m);

    printf("Enter the edges (u v w):\n");

    for (i = 0; i < m; i++) {
        scanf("%d %d %d",
              &edges[i].u,
              &edges[i].v,
              &edges[i].w);
    }

    /* Initialize disjoint sets */
    for (i = 1; i <= n; i++) {
        parent[i] = i;
        rank[i] = 0;
    }

    /* Sort edges by weight */
    qsort(edges, m, sizeof(struct Edge), compare);

    printf("\nEdge\tCost\n");

    /* Kruskal's Algorithm */
    for (i = 0; i < m && edgeCount < n - 1; i++) {

        int u = edges[i].u;
        int v = edges[i].v;
        int w = edges[i].w;

        /* Check whether adding edge creates a cycle */
        if (find(u) != find(v)) {

            unionSet(u, v);

            printf("%d--%d\t%d\n", u, v, w);

            totalCost += w;
            edgeCount++;
        }
    }

    printf("\nTotal Weight of the Spanning Tree: %d\n", totalCost);

    return 0;
}