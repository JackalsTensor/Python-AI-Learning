"""
混淆矩阵
    描述：用来描述真实值和预测值关系的
图解：
                    预测标签(正例)        预测标签(反例)
    真实标签(正例)    真正例(TP)             伪反例(FN)
    真实标签(反例)    伪正例(FP)             真反例(TN)
1.默认使用分类少充当正例
2.精确率=tp/(tp+fp)
3.召回率=tp/(tp+fn)
4.F1值=2*(精确率*召回率)/(精确率+召回率)
"""
import pandas
from sklearn.metrics import confusion_matrix,precision_score,recall_score,f1_score

#记录样本数据
y_train=['恶性','恶性','恶性','恶性','恶性','恶性','良性','良性','良性','良性']
#模型A预测结果
y_pred_A=['恶性','恶性','恶性','良性','良性','良性','良性','良性','良性','良性']
#模型B预测结果
y_pred_B=['恶性','恶性','恶性','恶性','恶性','恶性','良性','恶性','恶性','恶性']
#用标签标记正例反例
label=['恶性','良性']
df_label=['恶性(正例)','良性(反例)']
#搭建A的混淆矩阵
cm_A=confusion_matrix(y_train,y_pred_A,labels=label)
# print(cm_A)
#转化为DataFrame版本
df_A=pandas.DataFrame(cm_A,index=df_label,columns=df_label)
print(f'混淆矩阵A的DataFrame对象形式:\n{df_A}')
#搭建B的混淆矩阵
cm_B=confusion_matrix(y_train,y_pred_B,labels=label)
# print(cm_B)
#转化为DataFrame版本
df_B=pandas.DataFrame(cm_B,index=df_label,columns=df_label)
print(f'混淆矩阵B的DataFrame对象形式:\n{df_B}')
#计算精确率，准确率，F1值
print(f'模型A的精确率:{precision_score(y_train,y_pred_A,pos_label="恶性")}')
print(f'模型A的召回率:{recall_score(y_train,y_pred_A,pos_label="恶性")}')
print(f'模型A的F1值:{f1_score(y_train,y_pred_A,pos_label="恶性")}')
print(f'模型B的精确率:{precision_score(y_train,y_pred_B,pos_label="恶性")}')
print(f'模型B的召回率:{recall_score(y_train,y_pred_B,pos_label="恶性")}')
print(f'模型B的F1值:{f1_score(y_train,y_pred_B,pos_label="恶性")}')