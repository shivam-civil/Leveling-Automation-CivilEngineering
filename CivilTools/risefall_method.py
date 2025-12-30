

def RiseFallMethod(readings,bm_rl):
    """
    readings parameter -- list 
    bm_rl -- float (RL of first point )
    require pandas module 

    """
    import pandas as pd
    results=[]
    current_rl=bm_rl                       # RL OF BENCHMARK 
    prev_type=None
    prev_reading=None
    cp_count=1

    i=0
    while i < len(readings):
        r=readings[i]
        rstation=r["station"]
        rtype=r["type"]
        rvalue=r["value"]

        row={                                     # ROW FOR OUTPUT TABLE FOR EACH READINGS
            "STATION":rstation,
            "BS":"",
            "IS":"",
            "FS":"",
            "RISE":"",
            "FALL":"",
            "RL":"",
            "REMARKS":""
        }
        if i==0:                            # 1ST READING AS BENCHMARK
            row["BS"]=rvalue
            row["RL"]=round(current_rl,3)
            row["REMARKS"]=rstation
            prev_type=rtype
            prev_reading=rvalue
            results.append(row)
            i +=1
            continue
        if (                                  # FOR CHANGE POINT ( FS AND BS IN SAME ROW )
            i +1 < len(readings)
            and readings[i+1]["type"]=="BS"
            and readings[i+1]["station"].startswith("CP")
            and rstation.startswith("CP")
            ):
            fs_value=rvalue
            bs_value=readings[i+1]["value"]

            # RISE/FALL BASED ON DIFF
            diff=prev_reading-fs_value
            if diff > 0 :
                row["RISE"]=round(diff,3)
                current_rl += diff
            elif diff < 0 :
                row["FALL"]=round(abs(diff),3)
                current_rl -= abs(diff)
            row["BS"]=round(bs_value,3) 
            row["FS"]=round(fs_value,3)
            row["RL"]=round(current_rl,3)
            row["REMARKS"]="CP"+str(cp_count)
            
            prev_reading=bs_value
            cp_count += 1                         # FOR CHANGE POINT COUNT 
            i += 2                                # SKIPS THE NEXT 1 READING 
            results.append(row)
            continue 

        # ------- FOR NORMAL POINTS ------
        diff=prev_reading - rvalue 
        if diff > 0: 
            row["RISE"]=round(diff,3)
            current_rl += diff
        elif diff < 0 : 
            row["FALL"]=round(abs(diff),3)
            current_rl -= abs(diff)
        if rtype=="BS":
            row["BS"]=rvalue 
        elif rtype=="IS":
            row["IS"]=rvalue
        elif rtype=="FS":
            row["FS"]=rvalue
            row["REMARKS"]="LAST FS"

        row["RL"]=round(current_rl,3)
        prev_reading=rvalue
        i += 1
        results.append(row)
    return pd.DataFrame(results)             # RETURN AD DATAFRAME FOR FURTHER TASKS  



