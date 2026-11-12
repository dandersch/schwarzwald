/* Schwarzwald: macros, types and callbacks; 12345 stays a comment. */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#define MAX_TREES 42u
#define SCALE(value) ((value) * 1.25)
#define FOREST_LOG(...) fprintf(stderr, __VA_ARGS__)

enum canopy { CANOPY_OPEN = 0, CANOPY_DENSE = 1 };
typedef struct forest forest_t;
typedef unsigned (*forest_visit_fn)(const forest_t *forest, void *context);

struct forest {
    const char *name;
    unsigned trees;
    double density;
    enum canopy canopy;
    forest_visit_fn visit;
};

static unsigned count_trees(const forest_t *forest, void *context) {
    unsigned *total = context;
    *total += forest->trees;
    return forest->trees;
}

int main(void) {
    const uint32_t flags = 0x2Au | (1u << 4);
    const unsigned permissions = 0755;
    const double threshold = 6.25e-2;
    const float growth = .5f;
    const char separator = '\n';
    const bool healthy = true;
    forest_t woods[] = {
        {.name = "Schwarzwald", .trees = MAX_TREES, .density = 0.85,
         .canopy = CANOPY_DENSE, .visit = count_trees},
        {.name = "Bannwald 123", .trees = 7, .density = 0.65,
         .canopy = CANOPY_OPEN, .visit = count_trees},
    };
    forest_visit_fn visitor = &count_trees;
    unsigned total = 0;
    for (unsigned i = 0; i < sizeof woods / sizeof woods[0]; ++i) {
        struct forest *current = &woods[i];
        const unsigned count = visitor(current, &total);
        if (healthy && current->density > threshold) {
            printf("%s: %u trees, density %.2f%c", current->name,
                   count, SCALE(current->density), separator);
        }
    }
    FOREST_LOG("total=%u flags=%#x mode=%o growth=%.1f\n",
               total, (unsigned)flags, permissions, (double)growth);
    return total == 49u ? 0 : 1;
}
