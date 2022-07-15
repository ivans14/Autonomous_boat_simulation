def matrix_combinator(a,b):
    result =  []
    for i in range(len(a)):
        row = []
        for j in range(len(a[i])):
            row.append([0,0])
        result.append(row)
    
    for i in range(len(a)):
        for j in range(len(a[i])):
            result[i][j] = [a[i][j][0]+b[i][j][0], a[i][j][1]+b[i][j][1]]
    return result
    
def gyre_generator(dimensions, old_matrix):
    r = dimensions
    c = dimensions

    original_row = 5
    original_column = 10
    
    r2 = int(r/original_row)
    c2 = int(r/original_column)

    matrix = [] 

    for i in range(original_row):
        a =[] 
        for j in range(original_column):
            for k in range(c2):
                a.append(old_matrix[i][j]) 
    
        for l in range(r2):
            matrix.append(a)
    return matrix
