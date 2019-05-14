
# SenseWatch
***
### purpose of the project
This project  can parse the .txt file of SensOmics watch. And we can obtain the conv and raw dataframes from the project.
### environment
**language:**  python3.x  
**packages:**  numpy, pandas, datatime, os, sys.

### File Directory
> _SenseWatch_
>> **.gitignore**  
>> **LICENSE**  
>> **Readme.md**  
>>
>> _senswatchParse_
>>>**senswatch.py(senswatch.pyc)**:&nbsp;&nbsp;&nbsp;Parsing the  data.  
>>>
>>>*test*  
>>>>**test_senswatch.py**:&nbsp;&nbsp;&nbsp; A test sample.  
>>>>**sens_test_data.txt**:&nbsp;&nbsp;&nbsp; A .txt file for testing.

***

## senswatch.py (senswatch.pyc)
In this file, we parse the .txt files obtained from SensOmics watch. And we get three forms of data.

**conv list:** contains time and heart value.  
**raw list:** contains time, ppg and acceleration values.    
**drop list:** contains the broken data.  

## test_senswatch.py  
In this file, we transform the lists obtained from senswatch.py to dataframe format.
So, wen can get three dataframes:

**conv:**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;time: int, Unix timestamp    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hr  : int, Heart rate    
**raw:**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;time: int, Unix timestamp  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ppg : int, Photoplethysmography values  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;acc1: int, Acceleration in x axis  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;acc2: int, Acceleration in y axis  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;acc3: int, Acceleration in z axis  
**drop:**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a list contains dicts consist of the irrational data.
## How to run the project
In the project, you can run the test_senswatch.py directly. And you can change the test file to your files (change the path). Then
 you can get the dataframes. Of course, you can transform the lists obtaned from senswatch.py to other formats sucn as json, h5 and so on.
