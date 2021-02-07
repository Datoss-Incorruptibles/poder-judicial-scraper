
import requests
import time 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


import tesserocr # Para hacer OCR
import pytesseract

import numpy as np # Para hacer manipulación básica de imágenes
import matplotlib.pyplot as plt # Para visualizar imágenes
from PIL import Image # Para cambiar el formato de archivos

import json


arrayObjDetalle = []
prohibidos = []

codigosExp = [
["01942","2009","0","0401","JP","CI","01"],
["03891","2001","0","0401","JR","CI","05"],
["03891","2001","54","0401","JR","CI","05"],
["04147","2009","0","0401","JR","CI","03"],
["04149","2008","0","0401","JR","CI","08"],
["08390","2013","0","0401","JP","PE","01"],
["00192","2013","0","0401","JP","LA","04"],
["00919","2003","0","0412","JP","CI","01"],
["00998","2009","0","0401","JP","CI","07"],
["01807","2017","0","0401","JP","CI","06"],
["01815","2016","0","0401","JR","CI","03"],
["03009","2014","0","0405","JR","PE","01"],
["03009","2014","3","0405","JR","PE","01"],
["03009","2014","71","0405","JR","PE","01"],
["03137","2011","0","0401","JR","FC","04"],
["03469","2020","0","0405","JP","PE","01"],
["03476","2000","0","0401","JR","CI","02"],
["03476","2000","54","0401","JR","CI","02"],
["04156","2004","0","0401","JR","CI","05"],
["04156","2004","42","0401","JR","CI","05"],
["04808","2001","0","0401","JR","CI","06"],
["04808","2001","54","0401","JR","CI","06"],
["04808","2001","63","0401","JR","CI","06"],
["04808","2001","68","0401","JR","CI","06"],
["04808","2001","98","0401","JR","CI","06"],
["04835","2011","0","0412","JP","CI","02"],
["06415","2000","0","0401","JR","CI","01"],
["00033","2009","0","0401","JP","CI","01"],
["01005","2019","0","0401","JR","LA","06"],
["01005","2019","30","0401","JR","LA","06"],
["00380","2015","0","0401","JP","CI","02"],
["00840","2019","0","0401","JR","PE","02"],
["01140","2008","0","0401","JP","LA","04"],
["01685","2008","0","0401","JR","LA","01"]]

# codigosExp = [["02635","2006","0","0401","JR","PE","01"],
# ["03134","2011","0","0401","JR","CI","09"],
# ["03134","2011","12","0401","JR","CI","09"]]

# ["00630","2020","0","0401","JP","CI","02"],
# ["03020","2015","0","0401","JP","PE","01"]

urlPJForm = "https://cej.pj.gob.pe/cej/forms/busquedaform.html"
urlPJResult1 = "https://cej.pj.gob.pe/cej/forms/busquedacodform.html"
urlPJResult2 = "https://cej.pj.gob.pe/cej/forms/detalleform.html"

driver = webdriver.Chrome(executable_path='./chrome/chromedriver')
url = 'https://cej.pj.gob.pe/cej/forms/busquedaform.html'
counterfinal = 0
for codExp in codigosExp:
  #---------------------------------------------------------------------------------------------------------------------

  print("here we gooo")
  driver.get(url)


  boton_porcodigo = driver.find_element_by_xpath("//div[@class='panel-body']/div/ul/li/a[@href='#tabs-2']")
  boton_porcodigo.click()
  time.sleep(3)

  #---------------------------------Insert Candidato Data---------------------------------------------------------------------------


  input_cod_expediente = driver.find_element_by_xpath("//input[@id='cod_expediente']").send_keys(codExp[0])

  input_cod_anio = driver.find_element_by_xpath("//input[@id='cod_anio']").send_keys(codExp[1])

  input_cod_incidente = driver.find_element_by_xpath("//input[@id='cod_incidente']").send_keys(codExp[2])

  input_cod_distprov = driver.find_element_by_xpath("//input[@id='cod_distprov']").send_keys(codExp[3])

  input_cod_organo = driver.find_element_by_xpath("//input[@id='cod_organo']").send_keys(codExp[4])

  input_cod_especialidad = driver.find_element_by_xpath("//input[@id='cod_especialidad']").send_keys(codExp[5])

  input_cod_instancia = driver.find_element_by_xpath("//input[@id='cod_instancia']").send_keys(codExp[6])

  #-------------------------------------Consultar y comprobar de que no es PROHIBIDO-------------------------------------------------------------------
  boton_consultarExpedientes = driver.find_element_by_xpath("//button[@id='consultarExpedientes']")
  boton_consultarExpedientes.click()
  # time.sleep(2)

  try:
    cod_especialidadNoSoportada = driver.find_element_by_xpath("//span[@style='display: none']")
    print(cod_especialidadNoSoportada)
    print("No eres prohibido  ")


  except:
    print("An exception occurred")
    print("El prohibido here")
    prohibidos.append(codExp)
    # driver.close()
    continue


  #---------------------------------Capture img---------------------------------------------------------------------------
  input_codigoCaptcha = driver.find_element_by_xpath("//img[@id='captcha_image']")
  stado = input_codigoCaptcha.screenshot('captcha.png') 

  #---------------------------------------------------------------------------------------------------------------------

  img = plt.imread('captcha.png')
  img_rgb = img[:,:,:3]
  img_inv = 1 - img_rgb
  img_gr = img_inv.mean(axis=2)
  plt.imshow(img_gr, cmap='Greys_r' )
  img_pil = Image.fromarray(np.uint8(img_gr*255))
  captchaTexto =  pytesseract.image_to_string(img_pil, lang='eng')


  print(captchaTexto.split())

  arrayText = captchaTexto.split()
  print(arrayText)

  if arrayText:
    fisrt = arrayText[0]
  else:
    fisrt = "1234"

  print(fisrt)

  #------------------------------------Write Captcha-----------------------------------------------------------------------

  input_codigoCaptcha = driver.find_element_by_xpath("//input[@id='codigoCaptcha']").send_keys(fisrt)
  print(input_codigoCaptcha)

  #-------------------------------------Consultar-------------------------------------------------------------------
  boton_consultarExpedientes = driver.find_element_by_xpath("//button[@id='consultarExpedientes']")
  boton_consultarExpedientes.click()

  time.sleep(3)


    #-------------------------------------Check URL is correct-------------------------------------------------------------------
  urlPJ = driver.current_url
  print(urlPJ,"outeside urlPJ")

  while urlPJ == urlPJForm:
    input_codigoCaptcha = driver.find_element_by_xpath("//img[@id='captcha_image']")
    stado = input_codigoCaptcha.screenshot('captcha.png') 
    # ---------------------------------------------------------------------------------------------------------------------
    img = plt.imread('captcha.png')
    img_rgb = img[:,:,:3]
    img_inv = 1 - img_rgb
    img_gr = img_inv.mean(axis=2)
    plt.imshow(img_gr, cmap='Greys_r' )
    img_pil = Image.fromarray(np.uint8(img_gr*255))
    captchaTexto =  pytesseract.image_to_string(img_pil, lang='eng')
    arrayText = captchaTexto.split()
    if arrayText:
      fisrt = arrayText[0]
    else:
      fisrt = "1234"
    # ------------------------------------Write Captcha-----------------------------------------------------------------------
    input_codigoCaptcha = driver.find_element_by_xpath("//input[@id='codigoCaptcha']").send_keys(fisrt)
    # -------------------------------------Consultar-------------------------------------------------------------------
    boton_consultarExpedientes = driver.find_element_by_xpath("//button[@id='consultarExpedientes']")
    boton_consultarExpedientes.click()


    time.sleep(2)
    urlPJ = driver.current_url

    print(urlPJ,"inside urlPJ")

    

  # ---------------------------------------------------------------------------------------------------------------------

  boton_verDetallle = driver.find_element_by_xpath("//form[@action='detalleform.html']/button[@type='submit']")
  # print(boton_verDetallle)
  # boton_verDetallle.click()

  driver.execute_script("arguments[0].click();", boton_verDetallle)

  listaDetalle = driver.find_elements_by_xpath("//div[@id='gridRE']/div/div")
  # print(listaDetalle)



  tmpDetalleArray = []
  counter = 0

  for detalle in listaDetalle:
    if counter % 2 == 1:
      textList = detalle.get_attribute('innerText')
      tmpDetalleArray.append(textList)
      print(textList)
    counter = counter + 1

  arrayObjDetalle.append(tmpDetalleArray)
  print(tmpDetalleArray)
  print("--MENOS UNO")
  print(counterfinal)
  counterfinal = counterfinal + 1
  # driver.close()
  dataFinal = json.dumps(arrayObjDetalle)
  dataFinalProh = json.dumps(prohibidos)
  with open('dataFinal3.json', 'w') as file:  # Use file to refer to the file object
    file.write(dataFinal)

  with open('prohibidos3.json', 'w') as file:  # Use file to refer to the file object
    file.write(dataFinalProh)

driver.close()
print("--FINISH")


# dataFinal = json.dumps(arrayObjDetalle)
# dataFinalProh = json.dumps(prohibidos)



# f = open("demofile3.txt", "w")
# f.write("Woops! I have deleted the content!")

# with open('dataFinal.json', 'w') as file:  # Use file to refer to the file object
#   file.write(dataFinal)

# with open('prohibidos.json', 'w') as file:  # Use file to refer to the file object
#   file.write(dataFinalProh)

  # <span id="cod_especialidadNoSoportada" class="msjError" style=""> (*) La búsqueda de la especialidad Penal no está permitida</span>