from file_importer import FileImporter

def get_dif_inds(str1, str2): 
    ''' get a list of indices where differences occur between each string '''
    difs = []

    for j in range(len(str1)):                       # Assume both are same length
        if str1[j] != str2[j]:
            difs.append(j)
        
        if len(difs) == 2:                           # Break early for efficiency, we only care if > 1
            break
    
    return difs


ids = FileImporter.get_input("/../input/2.txt").split("\n")

for i in range(0, len(ids)): 
    for j in range(i + 1, len(ids)):                # Compare each string with each other one moving down the list
        
        dif_inds = get_dif_inds(ids[i], ids[j])     # Get the indices of all differences in their characters
        
        if len(dif_inds) == 1:                      # If there's only one, this is our one. Remove the char at that index
            answer = ids[i]
            ind_remove = dif_inds[0]
            print(answer[:ind_remove] + answer[ind_remove+1:])

    