import pandas as pd
from utils import sta_infos, write_txt

keys = ["studentId", "skill", "problemId"]

def read_data_from_csv(read_file, write_file):
    df = pd.read_csv(read_file, encoding='utf-8', low_memory=False)
    
    #统计原始数据集情况
    print(
        f"original interaction num: {df.shape[0]}, user num: {df['studentId'].nunique()}, question num: {df['problemId'].nunique()}, "
        f"concept num: {df['skill'].nunique()}")

    df = df.dropna(subset=["studentId","problemId","correct","skill","timeTaken","endTime"])
    df = df[df['correct'].isin([0,1])]      #filter responses
    df['correct'] = df['correct'].astype(int)

    print(
        f"after dropout interaction num: {df.shape[0]}, user num: {df['studentId'].nunique()}, question num: {df['problemId'].nunique()}, "
        f"concept num: {df['skill'].nunique()}")

    df2 = df[["studentId", "problemId","skill","correct","timeTaken","endTime"]]
    #df2["index"] = range(df.shape[0])
    stu_df = df2.groupby(['studentId'], sort=False)

    stu_inter = []
    for stu in stu_df:
        stu_id, tmp_inter = stu[0], stu[1]  #tmp_inter 单独学生所有交互dataframe
        tmp_inter = tmp_inter.sort_values(by=['endTime'])
        seq_len = len(tmp_inter)
        seq_skills = tmp_inter['skill'].astype(str)
        seq_ans = tmp_inter['correct'].astype(str)
        seq_problems = tmp_inter['problemId'].astype(str)
        seq_submit_time = tmp_inter['endTime'].astype(str)
        seq_response_cost = tmp_inter['timeTaken'].astype(str)

        assert seq_len == len(seq_skills) == len(seq_ans)

        stu_inter.append(
            [[str(stu_id), str(seq_len)], seq_problems, seq_skills, seq_ans, seq_submit_time, seq_response_cost])
        #print(stu[1])
        #break

    write_txt(write_file, stu_inter)


if __name__ == "__main__":

    read_data_from_csv('anonymized_full_release_competition_dataset.csv','data.txt')
