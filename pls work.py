import csv

def data(filename):
    temp_item_desc = {}
    with open(f"{filename}.csv", "r", encoding='utf-8') as file:
        content = csv.reader(file)
        header = next(content) 
        temp = 0
        for row in content:
            if row[1] not in temp_item_desc: #Adds data if not present
                temp_item_desc[row[1]] = 0
                i = 2
                while i < len(row):
                    temp_item_desc[row[1]] += int(row[i])
                    i += 1
            else:
                i = 2
                while i < len(row):
                    temp_item_desc[row[1]] += int(row[i])
                    i += 1
            temp+=1
            # print(temp)
        return temp_item_desc

religion_distribution = dict(sorted(data("127_enr1").items(), key=lambda item: item[1]))
age_distribution = dict(sorted(data("127_enr2").items(), key=lambda item: item[1]))
print(religion_distribution, age_distribution)


"""
{'Parsi': 4129, 'Total repeaters': 25856, 'Sikh': 26883, 'Christian': 113401, 'Jain': 133976,
'Total CWSN': 280574, 'Buddhist': 671100, 'Others': 985664, 'BPL': 2039632, 'ST': 2500542, 'SC': 2867571,
'Muslim': 2948642, 'OBC': 7315864, 'General': 9827862, 'Aadhar': 17963677}

{'Age<5': 5206, 'Age22': 7074, 'Age23': 10092, 'Age21': 12912, 'Age20': 41918, 'Age5': 70497,
'Age19': 152488, 'Age18': 632116, 'Age17': 1204118, 'Age16': 1512992, 'Age6': 1514045,
'Age15': 1747968, 'Age10': 1792393, 'Age13': 1814318, 'Age14': 1815536, 'Age7': 1827558,
'Age11': 1906791, 'Age8': 1942557, 'Age12': 1950551, 'Age9': 1953777}
"""