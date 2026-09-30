#include <stdio.h>
#include <limits.h>

#define MAX 100
#define INF INT_MAX

int main() {
    int n, start;
    int cost[MAX][MAX];
    int distance[MAX], parent[MAX], visited[MAX];
    int i, j, count;

    FILE *fp;

    printf("Enter the Number of Vertices: ");
    scanf("%d", &n);

    if (n < 1 || n > MAX) {
        printf("Error: Number of vertices must be between 1 and %d.\n", MAX);
        return 1;
    }

    printf("Enter the Source Vertex: ");
    scanf("%d", &start);

    /* Open input file */
    fp = fopen("inDiAdjMat1.dat", "r");

    if (fp == NULL) {
        printf("Error: Cannot open inDiAdjMat1.dat\n");
        return 1;
    }

    /* Read adjacency matrix */
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            if (fscanf(fp, "%d", &cost[i][j]) != 1 || cost[i][j] < 0) {
                printf("Error: The input file must contain non-negative integer costs.\n");
                fclose(fp);
                return 1;
            }
        }
    }

    fclose(fp);

    if (start < 1 || start > n) {
        printf("Error: Source vertex must be between 1 and %d.\n", n);
        return 1;
    }

    /* Initialize Dijkstra's arrays. */
    for (i = 0; i < n; i++) {
        distance[i] = INF;
        parent[i] = -1;
        visited[i] = 0;
    }

    /* Convert starting vertex to 0-based */
    start--;

    distance[start] = 0;

    /* Dijkstra's algorithm for a directed graph. */
    for (count = 0; count < n; count++) {
        int u = -1;
        int min = INT_MAX;

        /* Find the unvisited vertex with the smallest known distance. */
        for (i = 0; i < n; i++) {
            if (!visited[i] && distance[i] < min) {
                min = distance[i];
                u = i;
            }
        }

        if (u == -1)
            break;

        visited[u] = 1;

        /* Relax outgoing edges. A zero means that no edge is present. */
        for (j = 0; j < n; j++) {
            if (cost[u][j] != 0 && !visited[j] &&
                distance[u] != INF &&
                distance[u] + cost[u][j] < distance[j]) {
                distance[j] = distance[u] + cost[u][j];
                parent[j] = u;
            }
        }
    }

    printf("\nSource\tDestination\tCost\tPath\n");

    for (i = 0; i < n; i++) {
        printf("%d\t%d\t\t", start + 1, i + 1);

        if (distance[i] == INF) {
            printf("INF\tNo path\n");
            continue;
        }

        printf("%d\t", distance[i]);

        if (i == start) {
            printf("-\n");
            continue;
        }

        /* Print the predecessor chain in source-to-destination order. */
        int path[MAX];
        int pathLength = 0;
        int vertex = i;

        while (vertex != -1 && pathLength < MAX) {
            path[pathLength++] = vertex;
            vertex = parent[vertex];
        }

        for (j = pathLength - 1; j >= 0; j--) {
            printf("%d", path[j] + 1);
            if (j > 0)
                printf("->");
        }
        printf("\n");
    }

    return 0;
}