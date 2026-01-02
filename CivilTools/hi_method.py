

def HiMethod(readings,bm_rl):           # READINGS AS LIST AND BM_RL IS BENCHMARK OF 1ST READING 
    import pandas as pd
    results=[]                                          # STORE ALL OUTPUTS
    current_rl=bm_rl                                    # 1ST READING BENCHMARK 
    i=0

    while i < len(readings):                            # LOOP FOR ALL READNGS AND SKIPPING BS OF CP 
        r=readings[i]
        rstation=r["station"]
        rtype=r["type"]
        rvalue=r["value"]


        row={                                           # ROW FOR TABLE FORMAT 
            "STATION":rstation,
            "BS":"",
            "IS":"",
            "FS":"",
            "HI":"",
            "RL":"",
            "Remarks":""
        }

        if rstation=="BM" :                               # FOR BENCHMARK OR FIRST READING 
            current_hi=current_rl+rvalue
            row["BS"]=rvalue
            row["HI"]=round(current_hi,3)
            row["RL"]=current_rl
        elif rtype=="IS":                               # FOR IS POINT 
            current_rl=current_hi-rvalue
            row["IS"]=rvalue
            row["RL"]=round(current_rl,3)
        elif rtype=="FS" and rstation.startswith("CP"):     # FOR CHANGE POINT 
            if i+1 < len(readings) and readings[i+1]["type"]=="BS" and readings[i+1]["station"].startswith("CP") :                             # CHECKS THE NEXT READING 
                fs_value=rvalue
                bs_value=readings[i+1]["value"]
                current_rl=current_hi - fs_value
                current_hi=current_rl+bs_value
                row["BS"]=round(bs_value,3)
                row["FS"]=round(fs_value,3)
                row["HI"]=round(current_hi,3)
                row["RL"]=round(current_rl,3)
                row["Remarks"]=rstation
                i += 1                               # SKIP NEXT 1 READING 
        elif rtype=="FS" :                                       # FOR LAST FS   
            current_rl = current_hi - rvalue 
            row["FS"]=rvalue
            row["RL"]=current_rl
            row["Remarks"]="LastFS"
            
        i += 1                                        # CONTINUES THE LOOP
        results.append(row)                           # APPEND EVERY CALCULATED ROW 
    return pd.DataFrame(results)                      # RETURNS THE RESULTS IN PANDAS DATAFRAME 

