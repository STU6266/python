
import math


# function for windchill calculation in fahrenheit
def windspeed_calculation_f ():
    for speed in range (0, 60, 5 ):
        speed += 5  
        fah_cel == "F"
        wind_chill = 35.74 + (0.6215*temperature) - (35.75* (speed**0.16)) + (0.4275*temperature*(speed**0.16))
        print (f"At temperature {temperature}F, and wind speed at {speed}MPH. The windchill is: {wind_chill:.2f}F. ")
        

# function for windchll calculation if typed in celsius
def windspeed_calculation_c ():
    for speed in range (0, 60, 5 ):
        speed += 5         
        fah_cel == "C"
          # calculation from celsius to fahrenheit
        temperature_new = (temperature *1.8) + 32
        wind_chill = 35.74 + (0.6215*temperature_new) - 35.75*(speed**0.16) + (0.4275*temperature_new *(speed**0.16))
        print (f"At temperature {temperature_new}F, wind speed at {speed}MPH. The windchill is: {wind_chill:.2f}F")

       
temperature = float(input("What is the temperature? "))
fah_cel = input ("Fahrenheit or Celsius (F/C)? " ).upper()
print()

# calling the functions and loop if no F or C
while fah_cel != 'F''C':
  if fah_cel.upper() == 'F':
    windspeed_calculation_f ()
    break
  elif fah_cel.upper() == 'C':
    windspeed_calculation_c ()
    break
  else:
    fah_cel = input ("Fahrenheit or Celsius (F/C)? " ).upper()
    


