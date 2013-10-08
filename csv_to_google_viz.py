'''
    takes a csv, simply throws the data into a 
    google viz using code from google's api sandbox.
    https://code.google.com/apis/ajax/playground/

'''
import sys, getopt, argparse
import csv
import json
import re



'turn list of tuples into dict'
def tuple_list_to_dict(tuple_list):
    out_dict = {}
    for t in tuple_list:
        if t != [] and len(t) == 2:
            out_dict[t[0]] = t[1]
        elif t != [] and len(t) >= 2:
            out_dict[t[0]] = [el for el in t[1:]]
    return out_dict



'read_cli_args reads input -i and output -o'
def read_cli_args(argv):
    for arg in getopt.getopt(argv[1:], 'i:o:n:'):
        cli_args = tuple_list_to_dict(arg)
        return cli_args



google_html_code = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Google Visualization API Sample</title>
  <script type="text/javascript" src="//www.google.com/jsapi"></script>
  <script type="text/javascript">
    google.load('visualization', '1', {packages: ['motionchart']});
    function drawVisualization() {
      var data = new google.visualization.DataTable();
      COL_NAMES
      data.addRows( [ MY_DATA ] );
      var motionchart = new google.visualization.MotionChart(
          document.getElementById('visualization'));
      motionchart.draw(data, {'width': 800, 'height': 400});
    }
    google.setOnLoadCallback(drawVisualization);
  </script>
</head>
<body style="font-family: Arial;border: 0 none;">
<div id="visualization" style="width: 800px; height: 400px;"></div>
</body>
</html>
'''



if __name__ == '__main__':

    'read cmd inputs'
    cmd_inputs = read_cli_args(sys.argv)
    if cmd_inputs.get('-i') == None or \
       cmd_inputs.get('-o') == None or \
       cmd_inputs.get('-n') == None:
        raise Exception('missing input file -i, output file -o,'+\
                        ' or numeric col list -n') 

    infile  = open(cmd_inputs.get('-i'), 'rb')
    outfile = open(cmd_inputs.get('-o'), 'w')
    numeric = [int(n) for n in cmd_inputs.get('-n').split(',')]



    'read data, assumes headers in file'
    reader = csv.reader(infile)

    data_array = []
    counter = 0
    for row in reader:
        if counter == 0:
            header_row = row
        else:
            out = []
            for k, v in enumerate(row):
                if k in numeric:
                    try:
                        out.append(float(v))
                    except ValueError:
                        print 'string found in a numeric field:' +\
                              ' may be a null value'
                        out.append(v)
                else:
                    out.append(v)
            data_array.append(out)
        counter += 1



    'write main data- messy to remove quotes around date for js'
    main_data = []
    for row in data_array:
        row_string   = json.dumps(row)
        split_point  = len(row[0]) + 3
        clean_string = row_string[:split_point] + \
                       row_string[split_point:].replace('"','', 2)
        main_data.append(clean_string)

    data_string      = ',\n'.join(main_data)
    google_html_code = google_html_code.replace('MY_DATA', data_string)



    'write headers, clean up nulls, and write file'
    cols = []
    for k,v in enumerate(header_row):
        if k in numeric:
            t = 'number'
        elif v.lower().find('date') > -1:
            t = 'date'
        else:
            t = 'string'
        cols.append("data.addColumn( '{0}', '{1}');".format(t, v))
    google_html_code = google_html_code.replace('COL_NAMES', ' '.join(cols))
    google_html_code = google_html_code.replace('""', 'null')
    google_html_code = google_html_code.replace('"null"', 'null')

    outfile.write(google_html_code)
    outfile.close()