#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<memory.h>
#include<stdarg.h>
#define INVALID_NUM  -1
#define memset_s(buffer, sizea, value, sizeb) memset(buffer, value, sizea)

#define sprintf_s(_buffer, len, fmt, args...) sprintf(_buffer, fmt, args)
#define sprintf_s1(_buffer, len, fmt, args...) sprintf(_buffer, fmt, ##args)
#define sprintf_s2(_buffer, len, fmt, ...) sprintf(_buffer, fmt, ##__VA_ARGS__)

int IsDigit(char a)
{
    return ('0' <= a && a <= '9');
}


int IsUpperCase(char a)
{
    return ('A' <= a && a <= 'Z');
}

int IsLowerCase(char a)
{
    return ('a' <= a && a <= 'z');
}

int IsAlphabet(char a)
{
    return (IsUpperCase(a) || IsLowerCase(a));
}

int IsTargetAlphabet(char src, char key)
{
    return src == key;
}

int Char2Digit(char a)
{
    if (!IsDigit(a)) {
        return INVALID_NUM;
    }
    return (a - '0');
}

#define DECIMAL_BASE  10
int Chars2NumsReverse(const char *str)
{
    int i;
    int num;
    int base;
    int size;

    num = 0;
    size = strlen(str);
    for (i = 0, base = 1; i < size; i++) {
        num += Char2Digit(str[i]) * base;
        base *= DECIMAL_BASE;
    }
    return num;
}

int Chars2Nums(const char *str)
{
    int i;
    int num;
    int base;
    int size;

    num = 0;
    size = strlen(str);
    for (i = size - 1, base = 1; i >= 0; i--) {
        num += Char2Digit(str[i]) * base;
        base *= DECIMAL_BASE;
    }
    return num;
}

/* 
提取特定字符串
outLen >= size 用户保证, size = strlen(str) + 1 
*/
void StringExtract(const char *str, int size, 
                   int (*IsTarget)(char a), 
                   char *outStr, int outLen)
{
    int i;
    int top;
    top = 0;
    for (i = 0; i < size; i++) {
        if (IsTarget(str[i])) {
            outStr[top++] = str[i];
        }
    }
    outStr[top] = 0;
    return;
}

/* 统计特定字符的数量 */
int StringStat(const char *str, int size, 
               int (*IsTarget)(char a))
{
    int i;
    int num;
    num = 0;
    for (i = 0; i < size; i++) {
        if (IsTarget(str[i])) {
            num++;
        }
    }
    return num;
}

int StringString(const char *str, int inLen, const char *key, int outLen)
{
    int i;
    int j;
    int cmpEnd;
    int pos;
    pos = 0;
    cmpEnd == inLen - outLen;
    for (i = 0; i < cmpEnd; i++) {
        pos = 0;
        for (j = 0; j < outLen; j++) {
            if (str[i + j] == key[j]) {
                pos++;
            }
        }
        if (pos == outLen) {
            break;
        }
    }
    return i;
}

/* 二维字符串系列转换成1维,
不需要连接符，connector[0] = 0
 */
#define MAC_BUFFER_LEN  32
void StringsUnion(char strs[][MAC_BUFFER_LEN], int n, char *connector, char *outStr, int outLen)
{
    int i;
    int startPos;
    startPos = 0;
    for (i = 0; i < n; i++) {
        startPos += sprintf_s(outStr + startPos, outLen - startPos,"%s%s", strs[i], connector);
    }
    outStr[strlen(outStr) - strlen(connector) - 1] = 0;
    return;
}

/* 待调试 */
int StringsSpilit(char *inStr, int inLen, char *connector, char strs[][MAC_BUFFER_LEN], int *outN)
{
    int i;
    int n;
    int j;
    int pos;
    int top;
    int startPos;
    int nextPos;
    int notFoundFlag;
    int connnectLen;
    int tempLen;

    n = 0;
    connnectLen = strlen(connector) + 1;
    notFoundFlag = inLen - connnectLen;
    if (notFoundFlag <= 0) {
        return -1;
    }

    top++;
    startPos = 0;
    nextPos = -connnectLen;
    for (i = 0; i < inLen; i++) {
        startPos += nextPos + connnectLen;
        nextPos = StringString(inStr + startPos, inLen - startPos, connector, connnectLen);
        if (nextPos >= (inLen - startPos)) {
            /* not found */
            break;
        }
        if ((nextPos - startPos) >= MAC_BUFFER_LEN) {
            return -1;
        }
        for (j = startPos; j < nextPos; j++) {
            strs[top][j - startPos] = inStr[j];
        }
        strs[top][j - startPos] = 0;
        top++;
    }
    return 0;
}

int main()
{
    int top;
    char *src = "a3[da3[ac]435] bgd887 AAA9";
    char *dst = "a3[da3[ac]435] bgd887 AAA";
    char d2src[10][MAC_BUFFER_LEN] = {"123a", "fadf345", "453526", "dgga  fdffd", "daffaf", "afddfa"};
    char decodestr1[5000] = {0xFF};
    char decodestr2[5000] = {0xFF};
    char connect[1];
    int result[100];

    StringExtract(src, strlen(src) + 1, IsDigit, decodestr1, sizeof(decodestr1));
    // printf("\r\nsrc:%s \r\ndecode1:%s \r\ndecode2:%s", s, decodestr1, decodestr2);
    printf("\n%s %u", decodestr1, Chars2Nums(decodestr1));
    top = 0;
    result[top++] = StringStat(src, strlen(src) + 1, IsDigit);
    result[top++] = StringStat(src, strlen(src) + 1, IsAlphabet);
    result[top++] = StringStat(src, strlen(src) + 1, IsLowerCase);
    result[top++] = StringStat(src, strlen(src) + 1, IsUpperCase);
    printf("\n %u %u %u %u", result[0], result[1], result[2], result[3]);

    decodestr2[0] = 0;
    connect[0] = 0;
    StringsUnion(d2src, 7, "-", decodestr2, sizeof(decodestr2));
    printf("\n%s", decodestr2);
    //getchar();
    return 0;
}