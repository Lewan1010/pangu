
void initUnionFindSet(int *pre, int size) {
    int i;
    for (i = 0; i < size; i++) {
        pre[i] = i;
    }
    return;
}
int findRoot(int *pre, int size, int e) {
    int root = e;
    while(root != pre[root]) {
        root = pre[root];
    }
    return root;
}

void unionRoot(int *pre, int size, int e1, int e2) {
    int r1 = findRoot(pre, size, e1);
    int r2 = findRoot(pre, size, e2);
    pre[r2] = r1;
    return;
}

void reconstruct(int *pre, int size, int e) {
    int temp;
    int tempPre;
    int root = findRoot(pre, size, e);

    tempPre = e;
    while(tempPre != pre[tempPre]) {
        temp = pre[tempPre];
        pre[tempPre] = root;
        tempPre = temp;
    }    
    return;
}
