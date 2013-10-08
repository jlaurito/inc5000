'''
    clean data:
        -add headers which I forgot to do earlier
        -add rev/employee
        -re-order columns to fit google-viz requirements
        -only select certain industries
'''
import csv


'''
    little function to append a quotient to the end of a row
'''
def get_record_average(row, 
                       num_index, 
                       denom_index,
                       zero_denom=None):
    try:
        if row[num_index] == '':
            n = 0.0
        else:
            n = float(row[num_index])

        if row[denom_index] == '':
            d = 0.0
        else:
            d = float(row[denom_index])
        r = n/d

    except ValueError:
        print 'Error: not numbers:', row[denom_index], row[num_index]
    except ZeroDivisionError:
        r = zero_denom

    return r



'flip_cols flips the order of two columns in an array'
def flip_cols(array, col1_index, col2_index):
    for row in array:
        row[col1_index], row[col2_index] = row[col2_index], row[col1_index] 
    return array



'insert_cols puts a col into an array at a specified index'
def insert_col(array, col_index, col):
    for rownum, row in enumerate(array):
        row.insert(col_index,col[rownum])
    return array



if __name__ == '__main__':

    infile  = open('inc5000data.csv', 'rb')
    reader  = csv.reader(infile)
    outfile = open('inc5000data_cleaned.csv', 'wb')
    writer  = csv.writer(outfile, delimiter=',', quotechar='"')
    data_in = []



    header_row =['Name', 'Date', 'Rank', '3yr Rev Growth %', 
                 'Revenue', 'Industry', 
                 'Employees', 'City', 'State', 'Rev./Employee']



    'fix cols with 0 denom, calc averages'
    for row in reader:
        for col in row:
            if col == '':
                col = 'null'
        out = get_record_average(row, 3, 5, zero_denom='null')
        row.append(out)
        data_in.append(row)



    'need to make name the first column and add date'
    flip_cols(data_in, 0, 1)
    date_col = ['new Date(2013,1,1)' for r in data_in]
    insert_col(data_in, 1, date_col )


    
    'write to file when rows are in right industry'
    writer.writerow(header_row)

    for row in data_in:
        if row[5] in ["Advertising & Marketing",
                      "Media",
                      "Software"]:
            writer.writerow(row)

    infile.close()
    outfile.close()
