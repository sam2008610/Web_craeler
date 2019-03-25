# 求出平面中距离最近的点对（若存在多对，仅需求出一对）
import random
import math

# 计算两点的距离


def calDis(seq):
    dis = math.sqrt((seq[0][0]-seq[1][0])**2+(seq[0][1]-seq[1][1])**2)
    return dis

# 生成器：生成横跨跨两个点集的候选点，由于点集是按纵坐标升序排序，right点集的点的纵坐标必定大于u的纵坐标，故只需检查纵坐标是否大于u[1]+dis，且只需最多检查right点集中纵坐标最小的6个点


def candidateDot(u, right, dis):
    cnt = 0
    for v in right:
        cnt += 1
        if v[1] > u[1]+dis or cnt > 3:
            break
        yield v

# 求出横跨两个部分的点的最小距离


def combine(left, right, resMin):
    med_x = (left[-1][0]-right[0][0])/2
    dis = resMin[1]
    minDis = resMin[1]
    pair = resMin[0]
    for u in left:
        if u[0] < med_x-dis:
            continue
        for v in candidateDot(u, right, dis):
            dis = calDis([u, v])
            if dis < minDis:
                minDis = dis
                pair = [u, v]
    return [pair, minDis]


# 分治求解
def divide(seq):
    # 求序列元素数量
    n = len(seq)
    # 按点的纵坐标升序排序
    seq = sorted(seq, key=lambda y: y[1])
    # 递归开始进行
    if n <= 1:
        return None, float('inf')
    elif n == 2:
        return [seq, calDis(seq)]
    else:
        half = int(n/2)
        left = seq[:half]
        resLeft = divide(left)
        right = seq[half:]
        resRight = divide(right)
        # 获取两集合中距离最短的点对
        if resLeft[1] < resRight[1]:
            resMin = combine(left, right, resLeft)
        else:
            resMin = combine(left, right, resRight)
        pair = resMin[0]
        minDis = resMin[1]
    return [pair, minDis]


cases = input()
for i in range(cases):
    n = input()
    seq = [(input(), input()) for x in range(n)]
    sorted(seq, key=lambda y: y[0])
    print("优化算法", divide(seq))
