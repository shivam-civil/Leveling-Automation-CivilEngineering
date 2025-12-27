import json
def clean_data(rawdata,cg):
    """
    Rawdata and cg only acceptable in list type
    """    
    readings=[]
    cg_count=0                                    

    for index,data in enumerate(rawdata,start=1):
        row={
            "station":"",
            "type":"",
            "value":""
        }
        if index==1:                                  # FOR FIRST READING 
            row["station"]="BM"
            row["type"]="BS"
            row["value"]=float(data)
            
        elif index in cg:                              # FOR CHANGE POINTS 
            cg_count += 1
            row["station"]="CP"+str(cg_count)  
            row["type"]="FS"
            row["value"]=float(data)
            
        elif index==len(rawdata):                      # FOR LAST READINGS
            row["station"]="P"+str(index-cg_count)
            row["type"]="FS"
            row["value"]=float(data)
            
        else :
            for cg_point in cg :
                status=False
                if index-cg_point==1:                   # FOR BS POINTS AFTER CHANGE POINTS
                    row["station"]="CP"+str(cg_count)
                    row["type"]="BS"
                    row["value"]=float(data)
                    status=True
                    break
                    
            if status==False:                            # FOR IS READINGS   
                row["station"]="P"+str(index-cg_count)
                row["type"]="IS"
                row["value"]=float(data)
        readings.append(row)    
    return readings  
"""
rawdata=[1,2,3,4,5,6,7,8,9,10]
cg=[3,7]
readings=clean_data(rawdata,cg)
with open("data.json","w") as f:
    json.dump(readings,f,indent=4)
"""    
   

