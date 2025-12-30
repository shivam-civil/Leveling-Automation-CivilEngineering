 
def CleanData(rawdata,cp):
    """
    Rawdata and cp only acceptable in list type
    require no modules 
    """    
    readings=[]
    cp_count=0                                    

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
            
        elif index in cp:                              # FOR CHANGE POINTS 
            cp_count += 1
            row["station"]="CP"+str(cp_count)  
            row["type"]="FS"
            row["value"]=float(data)
            
        elif index==len(rawdata):                      # FOR LAST READINGS
            row["station"]="P"+str(index-cp_count)
            row["type"]="FS"
            row["value"]=float(data)
            
        else :
            for cp_point in cp :
                status=False
                if index-cp_point==1:                   # FOR BS POINTS AFTER CHANGE POINTS
                    row["station"]="CP"+str(cp_count)
                    row["type"]="BS"
                    row["value"]=float(data)
                    status=True
                    break
                    
            if status==False:                            # FOR IS READINGS   
                row["station"]="P"+str(index-cp_count)
                row["type"]="IS"
                row["value"]=float(data)
        readings.append(row)    
    return readings  


  
 
   

