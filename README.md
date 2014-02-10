Web Tester
==========

Python script that uses SST - Web Test Framework and the headless WebKit PhantomJS to run functional tests.

Ejecuta una serie de tests, guarda las estadísticas en cada ejecución y en caso de error envía un email con el resultado del test y una captura de pantalla.

Para ello hace uso de un pequeño framework en python para Selenium además de un navegador headless para poder ejecutarse en consola sin necesidad de un navegador.

El siguiente software es necesario para poder ejecutarse:

* SST - Web Test Framework: http://testutils.org/sst/
apt-get install python-pip
pip install -U sst

* PhantomJS: http://phantomjs.org
Descargamos el binario precompilado desde su página web: http://phantomjs.org/download.html

La acciones disponibles para escribir los tests se pueden encontrar en: http://testutils.org/sst/actions.html
