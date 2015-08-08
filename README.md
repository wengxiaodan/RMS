# Regional Module processing software
A Regional Module data management system created using Python and SQLite. Using the simply designed graphical user interface(GUI) `RM_GUI.py`, users are able to:

* import filled Excel questionnaires to the SQLite database;
* export country specific data points and complete questionnaire tables back to Excel;
* modify and clean the data in Excel and re-import then back in the SQLite database;
* create different copies of country specific data, one to hold the original data, one for cleaning and one for dissemination.

For a complete GUI user guide see [user guide](./Documentation/User_guide.html)

## Installation (on windows)
### Required packages:

* Python-64 $>=3.4$ . 
* [xlsxWriter](https://xlsxwriter.readthedocs.org/), tested under version 0.7.3.
* [xlrd](https://pypi.python.org/pypi/xlrd), tested under version 0.9.4. However
  xlrd has some issues in processing comments. A fix patch is submitted to the maintainer, but has not been integrated yet. Therefore, until the patch is integrated please use the xlrd 0.9.4 version in the following GitHub [repo](https://github.com/python-excel/xlrd).

All those packages could be installed using [Pip](https://pypi.python.org/pypi/pip). To install Pip download the [get-pip.py](get-pip.py) and run the following in the terminal where `get-pip.py` exist. (for more details see [this](https://pip.pypa.io/en/stable/installing.html#install-pip))

```
python get-pip.py
```
Once Pip is installed run the following in your terminal to install all required packages.

```
pip install xlsxwriter
pip install https://github.com/melmasri/xlrd.zip
```

### Installation of the main package
To installation options are available:

* **Downloading**: download and extract the following [zip file.](https://github.com/melmasri/RMS/archive/master.zip).
* **Git cloning**: in your terminal run `git clone https://github.com/melmasri/RMS`

Move the downloaded/cloned folder to your desired destination and then create a shortcut to `RM_GUI.py`.

To start double-click on the `RM_GUI.py` shortcut and the GUI should pop-up.

For more details refer to
* Python scripts documentation.
* Python help files

## Issues and extra features <sup>[1](#myfootnote1)</sup>
Report issues and suggest features and improvements on the [GitHub issue tracker.]
(https://github.com/melmasri/RMS/issues)


<a name="myfootnote1">1</a>: The addition of new features are at the developers discretion.




