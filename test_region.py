import pulp as pl

import random
import pickle
# 参数设置

def test_region_number(num_areas,max_deploy_per_area):
    num_developers = 5
    c = [2, 3, 4]  # 部署成本
     #= 35  # 每个区域的最大部署数量


    # 假设数据
    r = [[5, 6, 7, 8, 9],   # 区域1对每个开发商的额外收益
         [7, 6, 5, 9, 10],  # 区域2
         [4, 5, 6, 7, 8]]   # 区域3

    p = [[1, 1.2, 1.4, 1.1, 1.3],  # 区域1的维护成本
         [1.5, 1.6, 1.5, 1.2, 1.1],  # 区域2
         [2, 1.8, 1.7, 1.9, 1.5]]  # 区域3

    #r = [[random.randint(0,9) for i in range(num_developers)] for j in range(num_areas)]
    #p = [[random.uniform(1,2) for i in range(num_developers)] for j in range(num_areas)]

    r_ap = [random.randint(3,9) for i in range(num_developers)]
    p_ap = [round(random.uniform(1,2), 1) for i in range(num_developers)]
    c_ap = random.randint(2,4)
    for q in range(num_areas - len(r)):
        r.append(r_ap)
        p.append(p_ap)
        c.append(c_ap)

    print(p)
    print(r)
    print(c)

    f1 = open('p3.pckl','wb')
    pickle.dump(p,f1)
    f2 = open('r3.pckl','wb')
    pickle.dump(r, f2)
    f3 = open('c3.pckl','wb')
    pickle.dump(c, f3)


    # 创建模型
    model = pl.LpProblem("RIS_Auction", pl.LpMaximize)

    # 决策变量
    x = pl.LpVariable.dicts("x", range(num_areas), lowBound=0, cat='Continuous')
    b = pl.LpVariable.dicts("b", (range(num_areas), range(num_developers)), lowBound=0, cat='Continuous')
    y = pl.LpVariable.dicts("y", (range(num_areas), range(num_developers)), cat='Binary')

    # 目标函数
    model += pl.lpSum(b[i][j] for i in range(num_areas) for j in range(num_developers)) - pl.lpSum(x[i] * c[i] for i in range(num_areas))

    # 约束
    model += pl.lpSum(x[i] for i in range(num_areas)) == 90  # 总部署量为90
    for i in range(num_areas):
        model += x[i] <= max_deploy_per_area
        model += pl.lpSum(y[i][j] for j in range(num_developers)) == 1  # 每个区域只能选择一个开发商
        for j in range(num_developers):
            model += b[i][j] <= (r[i][j] - p[i][j]) * x[i]  # 出价受到预期净收益的限制
            model += b[i][j] <= 1000 * y[i][j]  # 确保只有选中的开发商才有出价

    # 求解模型
    model.solve()

    profit = 0

    # 输出结果
    print("Solution Status:", pl.LpStatus[model.status])
    if pl.LpStatus[model.status] == "Optimal":
        for i in range(num_areas):
            print(f"Area {i+1}: {x[i].value()} RIS units")
            for j in range(num_developers):
                if y[i][j].value() == 1:
                    print(f"   Developer {j+1}: Bid {b[i][j].value()} - SELECTED")

                else:
                    print(f"   Developer {j+1}: Bid {b[i][j].value()} - NOT SELECTED")
    elif pl.LpStatus[model.status] == "Infeasible":
        print("No feasible solution exists.")
    elif pl.LpStatus[model.status] == "Unbounded":
        print("The model is unbounded.")
    else:
        print("Some other error occurred.")
    return model.objective.value()


optimal_result = []

num_areas = [3,4,5,6,7,8,9,10]

for i in num_areas:
    optimal_result.append(test_region_number(i,90/i + i))

print(optimal_result)
f4 = open('optimal_result3.pckl','wb')
pickle.dump(optimal_result, f4)
