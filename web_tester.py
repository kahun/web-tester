#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Script para la automatización de tests de páginas web.'''

__version__ = "1.0"

import os
import re
import glob
import datetime
import csv
import xml.etree.ElementTree as ET

# Variables
EMAIL_FROM      = ''
EMAIL_TO        = ['']
sst_path        = '/usr/local/bin'
sst_bin         = 'sst-run'
sst_num_process = '3'                        # Número de tests que se ejecutarán a la vez
sst_dir         = 'web_tests'                # Directorio que almacena los tests y los resultados
sst_tests       = 'tests'                    # Nombre del directorio que contiene los tests
sst_stats       = 'statistics'               # Directorio dónde se almacenarán las estadísticas para cada dominio
sst_options     = ' -q -s -c ' + sst_num_process + ' -r xml -b PhantomJS -d ' + sst_tests

def send_mail_attach(subject, text, files=[]):
  """Envía un email con el asunto, el texto y los adjuntos dados"""
  assert type(files)==list
  msg            = MIMEMultipart()
  msg['From']    = EMAIL_FROM
  msg['To']      = ', '.join(EMAIL_TO)
  msg['Subject'] = subject
  msg.attach( MIMEText(text) )
  for f in files:
      part = MIMEBase('application', "octet-stream")
      part.set_payload( open(f,"rb").read() )
      Encoders.encode_base64(part)
      part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
      msg.attach(part)
  server = smtplib.SMTP(EMAIL_SERVER)
  server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
  server.quit()

# Extendemos el PATH para que funcione el script en el entorno del crontab
if not re.search(sst_path, os.environ['PATH']):
  os.environ['PATH'] = os.environ['PATH'] + ':' + sst_path

# Nos movemos al directorio del sst y lanzamos el comando
os.chdir(sst_dir)
os.system(sst_bin + sst_options)

# Obtenemos los totales del resultado
tree           = ET.parse('results/results.xml')
root           = tree.getroot()
total_failures = root.get('failures')
total_tests    = root.get('tests')
total_time     = root.get('time')

# Preparamos el email a enviar por si hay errores
subject = '[Web tests] {0} web tests failed'.format(total_failures)
message = 'RESULT: {0} fails of {1} tests (Time: {2})\n\n'.format(total_failures,total_tests,total_time)

# Comprobamos que exista el directorio de estadísticas
if not os.path.isdir(sst_stats):
  os.mkdir(sst_stats, 0755)

# Analizamos los tests
for test in root.findall('testcase'):
  name   = test.get('name')
  time   = test.get('time')
  # Guardamos las estadísticas para cada test
  stats  = open(sst_stats + '/' + name + '.csv', "a")
  writer = csv.writer(stats, delimiter=',')
  writer.writerow([datetime.datetime.now(), time])
  stats.close()
  # Comprobamos si falló algún test
  fail = test.findall('failure')
  # Si hay fallos almacenamos los errores
  if fail:
    error   = re.search('AssertionError: (.*)', fail[0].text).group(1)
    message += "TEST: {0} (Time: {1})\nERROR: {2}\n\n".format(name, time, error)

# Si hay errores envíamos un email con el mensaje de error y la captura de la página
if int(total_failures) > 0:
  screenshots = glob.glob('results/*.png')
  print message
  send_mail_attach(subject, message, screenshots)
