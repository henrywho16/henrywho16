import csv
import glob, os
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
import hashlib
steam_data = []
faq_data = []
all_company = set()
def standard_time(input_string):
    if input_string == '':
        return [None,None]
    try:
        objDate = datetime.strptime(input_string, '%m/%d/%y')
    except ValueError:
        try:
            objDate = datetime.strptime(input_string, '%d %b, %Y')
        except ValueError:
            try:
                objDate = datetime.strptime(input_string, '%m/%d/%Y')
            except ValueError:
                try:
                    objDate = datetime.strptime(input_string, '%b %d, %Y')
                except ValueError:
                    objDate = datetime.strptime(input_string, '%b %Y')
    return [objDate,datetime.strftime(objDate,'%b %d, %Y')]
##perform preprocessing on strings.
##Remove special characters with relevance. Some character from other lanauge should be replaced with the english counterpart.
##instead of removed completely. The list is generated iteratively observation, for each iteration, change is applied to
##game names with high similarity. The result is compared between iteration.
def remove_meaningless_company_version(target):
    target =target.lower()
    replace_list = ['*','.',',','-','games','game','▲','™','!','_']
    target = target.replace('é','e')
    target = target.replace('ł','l')
    target = target.replace('ś','s')
    for i in replace_list:
        target = target.replace(i,' ')

    target_list = target.split(' ')
    ##based on obervation these short forms tends to have negative effect on the comparsion.
    list_of_target = ['digital','foundry', 'spc','ab','na','sa','bv','llc','designs','design','','gmbh', 'game','inc','ltd','ltd','games','studios','studio','software','vr','entertainment','interactive','the','productions','production','(japan)','plc','technologies','technologie']
    for i in list_of_target:
        if i in target_list:
            target_list.remove(i)
    output = ''
    for i in target_list:
        output = output + i
    output = output.replace(' ','')
    return output
def remove_meaningless(target):
    target = target.lower()
    replace_list = ['*','.',',','-','▲','™','!','_',":",'®','hd','—','the']
    target = target.replace('é','e')
    target = target.replace('ł','l')
    target = target.replace('ś','s')
    for i in replace_list:
        target = target.replace(i,' ')
    output = target.replace(' ','')
    return output

def remove_meaningless_s(target):
    replace_list = ['*','.',',','-','games','game','▲','™','!','_',"'"]
    target = target.replace('é','e')
    target = target.replace('ł','l')
    target = target.replace('ś','s')
    target = target.replace('ö','o')
    for i in replace_list:
        target = target.replace(i,' ')
    target_list = target.split(' ')
    list_of_target = ['international','sp','co','digital','foundry', 'spc','ab','na','sa','bv','llc','designs','design','','gmbh', 'game','inc','ltd','ltd','games','studios','studio','software','vr','entertainment','interactive','the','productions','production','(japan)','plc','technologies','technologie']
    for i in list_of_target:
        if i in target_list:
            target_list.remove(i)
    output = ''
    for i in target_list:
        output = output + i
    output = output.replace(' ','')
    return output
def compare_game(Steam_game_name,Steam_developer,Steam_publisher,Console_name,Console_developer,Console_publisher):
    score = 80* similar(Steam_game_name,Console_name) 
    developer_publisher_score =  20
    max(SequenceMatcher(Steam_developer,Console_developer),SequenceMatcher(Steam_publisher,Console_publisher))
    return (score + developer_publisher_score)

def checktime(list1, steam,faq):
    time = ''
    if list1[0] =='steam':
        for i in steam:
            if list1[2] ==i[1] and list1[1] == i[0]:
                time = i[5]
                break
    else:
        for i in faq:
            if list1[1] ==i[0] and list1[2] == i[4]:
                time = i[1]
                break
    return time

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
dir1 =os.getcwd()
##find all company names between all games
def get_all_company(steam_data,faq_data):
    all_company = set()
    counter = 0
    for i in steam_data:
        if i[0] == 'appid':
            continue
        all_company.add(i[3])
        all_company.add(i[4])
    for i in faq_data:
        if i[0] =='name':
            continue
        all_company.add(i[2])
        all_company.add(i[3])
    all_company = list(all_company)
    return all_company

def company_and_game(steam_data,faq_data,all_company):
    output = []
    for i in all_company:
        company = i
        temp =[company]
        if company == '':
            continue
        for j in steam_data:
            if j[0] == 'appid':
                continue
            if company == j[3] or company == j[4]:
                temp.append('steam')
                temp.append(j[0]) 
                temp.append(j[1])    
        for j in faq_data:
            if j[0] =='name':
                continue
            if company == j[2] or company == j[3]:
                temp.append('faq')
                temp.append(j[0])
                temp.append(j[4])
        output.append(temp)
    return output
def similar1(all_company):
    counter = 0
    output = []
    for i in all_company:
        counter = counter + 1
        company_name = i
        if company_name == "":
            continue
        temp_counter = 0
        for j in all_company:
            if temp_counter == counter :
                
                continue
            else:
                temp_counter = temp_counter + 1
                similar_rate = similar(company_name , j)*100
                if similar_rate > 80:
                    temp_left = i.lower()
                    temp_right = j.lower()
                    left = remove_meaningless_s(temp_left)
                    right = remove_meaningless_s(temp_right)
                    score = similar(left,right)*100
                   ## print(str(counter)+" : "+left +' , '+right)
                    if score >95:
                        output.append([i,j,score])
    return output
def company_and_game_final(all_company,combine):
    output = []
    company_list = []
    temp_list = []
    for i in combine:
        company_list.append(i[0])
        company_list.append(i[1])
    for i in all_company:
        company = i[0]
        if company in company_list:
            temp_list.append(i)
        else:
            output.append(i)
    remove_counter = 0
    for i in temp_list:
        company = i[0]
        possible_pair = []
        possible_match = []
        outcome = i
        for j in combine:
            pair = ''
            if j[0] == company :
                pair = j[1]
            elif  j[1] == company:
                pair = j[0]
            if pair !='':
                possible_pair.append(pair)
        for j  in possible_pair:
            for m in temp_list:
                if m[0] == j:
                    possible_match.append(m)
        for j in possible_match:
            remove_counter = remove_counter +1
            temp_list.remove(j)
            outcome = i +j[1:]
        output.append(outcome)
        return(output)
##find games with similar names
def compare_game_names(steam_data,faq_data):
    possible_match = []
    possible_match1 = []
    counter = 0
    game_name = []
    game_name_handled = []
    remove = []
    steam_remove = []
    for i in faq_data:
        if i[1] =='datePublished':
            continue
        game_name.append(i[0].lower())
    for i in faq_data:
        if i[1] =='datePublished':
            continue
        game_name_handled.append(remove_meaningless(i[0]))
    for i in steam_data:
        game_name1 = i[1].lower()
        game_name_handled1 = remove_meaningless(game_name1)
        counter = counter +1
        if i[0] == 'appid':
            continue
        if game_name1 in game_name or game_name_handled1 in game_name_handled:
            score = 0
            try:
                place = game_name.index(game_name1)+1
            except ValueError:
                place = game_name_handled.index(game_name_handled1)+1
            j = faq_data[place]
            score = 100*max(similar(remove_meaningless_company_version(i[4]),remove_meaningless_company_version(j[2])),
                            similar(remove_meaningless_company_version(i[4]),remove_meaningless_company_version(j[3])),
                            similar(remove_meaningless_company_version(i[3]),remove_meaningless_company_version(j[3])),
                            similar(remove_meaningless_company_version(i[3]),remove_meaningless_company_version(j[2])))
            score_cross = 100 * max(similar(remove_meaningless_company_version(i[3]),remove_meaningless_company_version(j[2])),similar(remove_meaningless_company_version(i[4]),remove_meaningless_company_version(j[3])))
            score_normal = 100 * max(similar(remove_meaningless_company_version(i[3]),remove_meaningless_company_version(j[3])),similar(remove_meaningless_company_version(i[4]),remove_meaningless_company_version(j[2])))
            faq_time = standard_time(j[1])
            steam_time = standard_time(i[5])
            if steam_time[0] == None or   faq_time[0]==None:
                continue
            elif  steam_time[0] < faq_time[0]:
                remove.append(place)
                steam_remove.append(counter-1)
                if score>=80:
                    possible_match.append([i[0],i[1],i[3],i[4],j[0],j[3],j[2],score,steam_time[1],j[4],faq_time[1]])
            elif steam_time[0] > faq_time[0]:
                remove.append(place)
                steam_remove.append(counter-1)
                if score>=80:
                    possible_match1.append([i[0],i[1],i[3],i[4],j[0],j[3],j[2],score,steam_time[1],j[4],faq_time[1]])

    
    return possible_match,possible_match1

def company_side_compare(steam,faq):
    all_company = []
    output = []
    output1 = []
    with open(dir1+"\\company and game+.csv",encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        all_company.extend(data)
    checker = 0
    for i in all_company:
        checker = checker +1
        company = i[0]
        temp_games = []
        if len(i) == 4:
            continue
        for j in range(1,len(i)-2,3):
            if j ==0:
                continue
            temp_games.append([i[j],i[j+1],i[j+2]])
        counter = 0
        for j in temp_games:
            name = remove_meaningless(j[2])
            counter = counter +1
            counter1 = 0
            for k in temp_games:
                possible_match = []
                score = 0
                if counter1 <counter:
                    counter1 = counter1+1
                    continue
                if j[0] == k[0]:
                    continue
                score = similar(name,remove_meaningless(k[1]))*100
                if score ==100:
                    possible_match = [company]
                    temp = j.copy()
                    steam_time = standard_time(checktime(temp,steam,faq))
                    temp.append(steam_time[1])
                    possible_match= possible_match +temp
                    temp = k.copy()
                    faq_time = standard_time(checktime(temp,steam,faq))
                    temp.append(faq_time[1])
                    possible_match= possible_match +temp
                    possible_match.append(score)
                    if possible_match not in output:
                        if steam_time[0]==None or faq_time[0]==None:
                            continue
                        elif steam_time[0]<faq_time[0]:
                           output.append((possible_match))
                        elif steam_time[0]>faq_time[0]:
                           output1.append((possible_match))

    
    output2 = []
    for i in output1:
        if i not in  output2:
            output2.append(i)
    return output,output2

def combine_info(company_PC,name_PC,company_CP,name_CP):
    game_pair_PC = []
    game_pair_CP = []

    for i in name_PC:
        game_pair_PC.append([i[1],i[2],i[3],i[0],'',i[8],i[7],i[6],i[0],'',i[4],i[9]])
    for i in company_PC :
        if i[0] != 'appid':
            game_pair_PC.append(['steam',i[0],i[1],i[2],i[3],i[10],i[9],i[4],i[5],i[6],i[8],i[7]])
    for i in  name_CP :
        game_pair_CP.append([i[1],i[2],i[3],i[0],'',i[8],i[7],i[6],i[0],'',i[9],i[4]])

    for i in company_CP:
        if i[0] != 'appid':
            game_pair_CP.append(['steam',i[0],i[1],i[2],i[3],i[10],i[9],i[4],i[5],i[6],i[8],i[7]])
    ex = []
##load the manal checked data
    with open(dir1+"\\confirm.csv",encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        ex.extend(data)
    print(len(game_pair_PC))
    print(len(game_pair_CP))
    game_brief= []
    for i in  game_pair_PC  :
        game_brief.append([i[0],i[1],i[2],i[3],i[4],i[5],'PC->Console'])
        game_brief.append([i[6],'',i[7],i[8],i[9],i[10],'PC->Console'])
    for i in game_pair_CP :
        game_brief.append([i[0],i[1],i[2],i[3],i[4],i[5],'console->PC'])
        game_brief.append([i[6],'',i[7],i[8],i[9],i[10],'console->PC'])
    for i in ex:
        game_brief.append([i[0],i[1],i[2],i[3],i[4],i[5],'console->PC'])
        game_brief.append([i[6],'',i[7],i[8],i[9],i[10],'console->PC'])
    counter =0
    remove = []
    for i in game_brief:
        counter = counter +1
        place = 0
        for j in game_brief:
            place = place +1
            if place <= counter:
                continue
            if i[0] ==j[0]:
                if i[2]==j[2]:
                    if i[5]==j[5]:
                        remove.append(place)
    remove_counter = 0
    remove = list(set(remove))
    for i in remove:
        game_brief.pop(i-remove_counter-1)
        remove_counter = remove_counter+1
    
    return game_brief
##load extra data
def extrat_detail(steam,faq,brief):
    console_counter = 0
    steam_counter= 0
    detialed = [['index','platform','steam_id','game name','developer','publisher','genres','release date','description','normalized name','normalized dev','normalized developer']]
    for i in brief:
        platform = i[0]
        link = i[1]
        game_name = i[2]
        dev = i[3]
        publisher = i[4]
        direction = i[6]
        detail_info = []
        if platform == 'steam':
            steam_counter = steam_counter +1
            index = 's'+str(steam_counter).zfill(5)
            for j in steam:
                if link == j[0] and game_name == j[1]:
                    release = standard_time (j[5])
                    detail_info = [index,platform,link,game_name,j[3],j[4],j[6],release,j[7],remove_meaningless(game_name),remove_meaningless_company_version(j[3]),remove_meaningless_company_version(j[4])]
                    detialed.append(detail_info)
                    break
        else:
            console_counter = console_counter+1
            index = 'c'+str(console_counter).zfill(5)
            for j in faq:
                
                if game_name == j[0] and platform ==j[4]:
                    release = standard_time (j[1])
                    detail_info = [index,platform,link,game_name,j[2],j[3],j[8],release,j[9],remove_meaningless(game_name),remove_meaningless_company_version(j[2]),remove_meaningless_company_version(j[3])]
                    detialed.append(detail_info)
                    break
    output = []
    temp = []
    for i in detialed:
        if i[1] == 'steam':
            if i[2] not in temp:
                temp.append(i[2])
                output.append(i)
        else:
            output.append(i)
    print(len(detialed))
    print(len(output))
    return output

##generate a list of company name and crossponding games.
def find_company_pair(steam_release,faq_data):

    print("Find all company names")
    all_company = get_all_company(steam_release,faq_data)
    print("Find corssponding game for each company")
    company_and_games = company_and_game(steam_release,faq_data,all_company)
    print("Determine similar company names")
    similar_company = similar1(all_company)
    print("Putting everything togerther, 1 company -> crossponding games")
    company_and_game_final1 = []
    company_and_game_final1 = company_and_game_final(company_and_games,similar_company)
    print("Company data processing complete")
    return company_and_game_final1
##compare game name between platforms
##two methods are used to find game compare

def name_compare(steam_release,faq_data):
    ##assume games with identical names are possible game pair. It has lower tolarance for game name difference and high tolarance for difference between developer name.
    pc_console , console_pc = compare_game_names(steam_release,faq_data)
    ##this method used a different apporach, assume 2 games developed by the same company is highly likely to be the same game.

    Company_game_PC, Company_game_CP = company_side_compare(steam_release,faq_data)
    ##putting together information from both apporaches into one list and removing duplcate
    game_brief = combine_info(pc_console,Company_game_PC,console_pc,Company_game_CP) 
    ##adding detail to the generated game pairs.
    detailed = extrat_detail(steam_release,faq_data,game_brief)
    with open(os.getcwd()+"\\detialed123.csv", 'w', encoding='utf-8-sig', newline='') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        for i in detailed:
            wr.writerows([i])
        csvfile.close()

def main():
    print("Load Data")
    steam_release = []
    faq_data = []
    ##load steam game info
    with open(dir1+"\\info_game_released.csv",encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        steam_release.extend(data)
    ##load console game info
    with open(dir1+"\\gamefaq_output1.csv",encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        faq_data.extend(data)

    print("Find similar company")
    ##find_company_pair(steam_release,faq_data)
    name_compare(steam_release,faq_data)
    
main()
