import sqlite3, io, xlwt


def download_report():
  conn = sqlite3.connect('doceriah.db')
  cursor = conn.cursor()
   
  cursor.execute("SELECT * FROM Contas")
  result = cursor.fetchall()
   
  #output in bytes
  output = io.BytesIO()
  #create WorkBook object
  workbook = xlwt.Workbook()
  #add a sheet
  sh = workbook.add_sheet('Report Contas')
   
  #add headers
  sh.write(0, 0, 'Emp Id')
  sh.write(0, 1, 'Emp First Name')
  sh.write(0, 2, 'Emp Last Name')
  sh.write(0, 3, 'Designation')
  sh.write(0, 4, 'Emp Id')
  sh.write(0, 5, 'Emp First Name')
  sh.write(0, 6, 'Emp Last Name')


   
  idx = 0
  for row in result:
   sh.write(idx+1, 0, row[0])
   sh.write(idx+1, 1, row[1])
   sh.write(idx+1, 2, row[2])
   sh.write(idx+1, 3, row[3])
   sh.write(idx+1, 4, row[4])
   sh.write(idx+1, 5, row[5])
   sh.write(idx+1, 6, row[6])
   sh.write(idx+1, 7, row[7])
   idx += 1
   
  workbook.save(output)
  output.seek(0)
   
  return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=employee_report.xls"})

download_report()