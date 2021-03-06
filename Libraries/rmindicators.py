import sqlite3,re
import sys, getpass, os, csv
import datetime
import csv

from functools import reduce
from rmsqlfunctions import *

##################################################
#### table Algebra for sum/div/prod operations
##################################################
## Default algebra tables
algebra_sum = {'a': {'a': 'a', 'm': 'a', 'n': 'a','x':'a', 'value':'a'},
               'm': {'a': 'a', 'm': 'm', 'n': 'm','x':'m', 'value':'m'},
               'n': {'a': 'a', 'm': 'm', 'n': 'n','x':'m', 'value':'value'},
               'x': {'a': 'a', 'm': 'm', 'n': 'm','x':'m', 'value': 'm' }, 
               'value': {'a': 'a', 'm': 'm', 'n' :'value','x':'m', 'value':'value'}}
algebra_prod = algebra_sum
algebra_div  = algebra_sum

def read_algebra():
    """  Rewrites global operations (sum/div/prod) algebra tables from csv files.

    The files are:
    RMS/Libraries/algebra-div.csv
    RMS/Libraries/algebra-prod.csv
    RMS/Libraries/algebra-sum.csv
    """

    algfiles = ['algebra-sum.csv', 'algebra-prod.csv','algebra-div.csv']
    algop = ['Sum', 'Prod', 'Div']

    
    if os.path.isfile('Libraries/'+algfiles[0]):
        print('File {0} found, reading algebra..'.format(algfiles[0]))
        data = csv.DictReader(open('Libraries/'+ algfiles[0]))
        global algebra_sum
        algebra_sum  = arrange_algebra_dist(data,algop[0])
    if os.path.isfile('Libraries/'+algfiles[1]):
        print('File {0} found, reading algebra..'.format(algfiles[1]))
        data = csv.DictReader(open('Libraries/'+algfiles[1]))
        global algebra_prod
        algebra_prod  = arrange_algebra_dist(data,algop[1])
    if os.path.isfile('Libraries/'+ algfiles[2]):
        print('File {0} found, reading algebra..'.format(algfiles[2]))
        data = csv.DictReader(open('Libraries/'+algfiles[2]))
        global algebra_div
        algebra_div  = arrange_algebra_dist(data,algop[2])

def arrange_algebra_dist(data, op= 'Sum'):
    """ Re-orderd from a read csv file to dictionary as seen in the global variables.

        The left corner of the table in the csv file should be the op, case sensitive.
    """
    result = {}
    for row in data:
        key = row.pop(op)
        if key in result:
            # implement your duplicate row handling here
            pass
        result[key] = row
    return(result)

## Reads new algebra tables
read_algebra()
##################################################

##################################################
##### Generic mathematical operators
##################################################           
def sum(x,y):
    """
    Sums two tupels x = (fig, mg_symbol), y = (fig, mg_symbol).

    Returns a tupple (fig, symbol), where symbol is 
    the result of the algebra tables and
    fig is '' is symbol is n, m ,a or x.

    Algebra Table 
    Sum,a, m,n,x, value
    a,a, m,n,x, value
    m,m, m,m,m,m
    n,n, m,n,x, value
    x,x, m, x,x, x
    value, value, m, value,x, value
    """
    global algebra_sum
    algeb = algebra_sum[x[1]][y[1]]
    if algeb =='value':
        return([round((x[0] or 0 ) + (y[0] or 0),4),'value'])
    return(['',algeb])

def neg(x,y):
    """ 
    Negation of two tuppels x = (fig, mg_symbol), y = (fig, mg_symbol).

    Returns a tupple (fig, symbol), where symbol 
    is the result of the algebra tables, 
    fig is '' is symbol is n, m ,a or x.
    """
    if y[1]=='value':
        y[0] = -y[0]
    return(sum(x,y))

def prod(x,y):
    """
    Product of two tuppels x = (fig, mg_symbol), y = (fig, mg_symbol).
    
    Returns a tupple (fig, symbol), where symbol is 
    the result of the algebra tables, 
    fig is '' is symbol is n, m ,a or x.

    Algebra Table 
    Prod,a, m,n,x, value
    a,a, m,n,x, value
    m,m, m,m,m,m
    n,n, m,n,x, value
    x,x, m, x,x, x
    value, value, m, value,x, value
    """
    global algebra_prod
    algeb = algebra_prod[x[1]][y[1]]
    if algeb =='value':
        return([round((x[0] or 0)*(y[0] or 0),4),'value'])
    return(['',algeb])

def div(x,y):
    """
    A Git test.
    Division of two tuppels x = (fig, mg_symbol), y = (fig, mg_symbol).

    Returns a tupple (fig, symbol), where symbol 
    is the result of the algebra tables, 
    fig is '' is symbol is n, m ,a or x.
    
    Algebra Table 
    Div,a, m,n,x, value
    a,a, m,n,x, value
    m,m, m,m,m,m
    n,n, m,n,x, value
    x,x, m, x,x, x
    value, value, m, value,x, value
    """
    global algebra_div
    algeb = algebra_div[x[1]][y[1]]
    if algeb == 'value':
        return([round((x[0] or 0)/(y[0] or 0),4),'value'])
    return(['',algeb])

def op2col(col1, col2, op):
    """Operation (sum/div/prod) of two columns."""
    return  list(map(lambda x,y: op(x, y), col1, col2))

def min_sp(lala):
    """Used to find the minimum value of a list or region indicators.

    Used in computing min indicators.
    """
    def auxf(x,y):
        if(x[1]=='m' or y[1]=='m'): return(['', 'm'])
        if ( (type(x[0]) in [int,float]) and (type(y[0]) in [int,float]) ):
            return ( [min(x[0],y[0]),x[1]] )
        elif (type(x[0]) in [int,float]):
            return (x)
        else:
            return(y)
    return(reduce(auxf,lala[1:])) # lala[1:] because the first element
                                  # corresponds to the country value
                                  # and we only want it for the
                                  # regions.

def max_sp(lala):
    """Used to find the maximum value of a list or region indicators.

    Used in computing max indicators.
    """
    def auxf(x,y):
        if(x[1]=='m' or y[1]=='m'): return(['', 'm'])
        if ( (type(x[0]) in [int,float]) and (type(y[0]) in [int,float]) ):
            return ( [max(x[0],y[0]),x[1]] )
        elif (type(x[0]) in [int,float]):
            return (x)
        else:
            return(y)
    return(reduce(auxf,lala[1:]))


def inverse_mg_id(x):
    """Converts from mg_id to symbol."""
    if type(x) in [int,float]:
        return('')
    elif x==3:
        return('X')
    elif x==6:
        return('A')
    elif x=="D":
        return("m")

def none_emptytr(x):
    """ Returns 'value' if x=None."""
    if x==None:
       return('value')
    else:
        return(x)
    
class indicators():
    def set_database_connection(self,database_file):
        """Sets the connection to the database."""
        self.conn=sqlite3.connect(database_file)

    def read_sql(self,sql_str):
        """ Reads from sql database."""
        database_cursor = self.conn.cursor()
        try:
            aux = database_cursor.execute(sql_str)    
            aux = database_cursor.fetchall()
            database_cursor.close()
            return aux
        except sqlite3.Error as e:
            print(sql_str)
            print ("An SQL error occurred:", e.args[0])


    def write_many_sql(self, sql_str, value_tupple):
        """ Write a tupple to SQL."""
        cursor=self.conn.cursor()
        cursor.executemany(sql_str, value_tupple)
        self.conn.commit()
        cursor.close()
        
    def write_sql(self, sql_str):
        """ Excute a single SQL query."""
        cursor=self.conn.cursor()
        cursor.execute(sql_str)
        self.conn.commit()
        cursor.close()
        
    def write_indic_sql(self,dic):
        """ 
        Inserts the a tuple or dictionary of indicators in SQL EDU_INDICATOR_EST
        Dictionary: must have the keys as the indicator name and the value as a list of
        lists with each sub-list for a region, must be ordered ascendingly.
        """
        if(type(dic)==dict):
            sql_tupple = ()
            ##"IND_ID,CO_CODE,IND_YEAR,FRM_ID,QUAL,FIG, MAGN,ADM_CODE"
            year = self.emco_year
            co_code = self.country_code
            for key, value in dic.items():
                sql_tupple  = sql_tupple + tuple(map(lambda x,y:(key, co_code,y, year,1,1)+tuple(x), value, range(len(value))))
                ## Write to SQL
                if sql_tupple:
                   self.write_many_sql(("INSERT OR REPLACE INTO EDU_INDICATOR_EST "
                                        "(IND_ID,CO_CODE,ADM_CODE,IND_YEAR,FRM_ID,QUAL,FIG,MAGN) "
                                        "VALUES (?,?,?,?,?,?,?,?)"), sql_tupple )

                    
    def write_indic_sql_no_regions(self,indicator_name, value_pair):
        """It is similar to write_indic_sql, but it only inserts an indicator
        for the country level instead of doing it for all the regions.

        """
        sql_tupple=( (indicator_name  ,self.country_code,0,self.emco_year,1,value_pair[0] ,1, value_pair[1] ), )
        self.write_many_sql(("INSERT OR REPLACE INTO EDU_INDICATOR_EST "
                             "(IND_ID,CO_CODE,ADM_CODE,IND_YEAR,FRM_ID,FIG,QUAL,MAGN) "
                             "VALUES (?,?,?,?,?,?,?,?)"),sql_tupple)

        
    def get_nadm1(self):
        """Gets the number of regions."""
        nadm1= self.read_sql(("select count(ADM_CODE) from regions "
                              "where co_code={} and ADM_CODE>0 and MC_YEAR={}".format(self.country_code, self.emco_year)))
       
    def get_country_code(self):
        """Sets the country code by looking in the COUNTRY table.

        This function searches the country code in the COUNTRY table
        using the self.country_name variable of the class. It assumes
        that there will be an exact match up to case. If this is not
        the case it returns None.
        """
        name=self.country_name.upper()
        # The following is necessary for compatibility with sql syntax
        name="'"+re.sub("'","''",name)+"'"
        ##cursor=self.conn.cursor()
        #The following is not working so I am using .format, but this is not secure
#        cursor.execute(u'SELECT CO_CODE FROM COUNTRY  WHERE UPPER(CO_LONG_NAME) IS ?', (name,) )
        country_code = self.read_sql(("SELECT CO_CODE FROM COUNTRY "
                                      "WHERE UPPER(CO_LONG_NAME) IS {0} limit 1;".format(name)))
        if(country_code==None):
            self.country_code=0
        else:
            self.country_code=country_code[0][0]

        
    def column_operation(self,info1,info2=[],operation=lambda x,y: x ):
        """Perform column operations given ACs and year.
        
        This function returns a vector with an operation applied to
        two columns. infoi is a vector [ACi,yeari], where ACi is an
        alphanumeric code and year is the year for which that
        alphanumeric code is going to be computed. operation is a
        function that receives two arguments. This is the operation
        that is going to be applied element by element to both colums.
        The years should be zero or -1. If info2 and operation are
        omited, it returns the values of the columns corresponding to
        [AC1,year1]. If data for one of the selected year and AC has
        not been entered in the database, an empty list is returned.

        """
        if(type(info1[0])!=list):
            AC1=info1[0]
            year1=info1[1]
            emc_id1 = self.read_sql("SELECT EMC_ID FROM RM_Mapping WHERE AC='{0}' AND CUR_YEAR={1} LIMIT 1".format(AC1,year1))
            if not emc_id1:
                return([])
            emc_id1= emc_id1[0][0]
            values1= self.read_sql(("select a.EM_FIG,b.SYMBOL from EDU_METER97_EST AS a "
                                    "LEFT JOIN MAGNITUDE AS b ON ( a.mg_id = b.mg_id) "
                                    "WHERE a.CO_CODE={0} and a.emc_id={1} AND a.emco_year={2} "
                                    "ORDER BY ADM_CODE ASC".format(self.country_code,emc_id1,self.emco_year+year1)))
            values1= list(map( lambda x: [x[0],none_emptytr(x[1])],values1 ))
        else:
            values1 = info1
        ## We allow info2 to be the empty list in case we only want one column
        if(info2 and type(info2[0])!=list):
            AC2=info2[0]
            year2=info2[1]
            emc_id2 = self.read_sql("SELECT EMC_ID FROM RM_Mapping WHERE AC='{0}' AND CUR_YEAR={1} LIMIT 1".format(AC2,year2))
            if not emc_id2:
                return([])
            emc_id2 = emc_id2[0][0]
            values2= self.read_sql(("select a.EM_FIG,b.SYMBOL from EDU_METER97_EST AS a "
                                    "LEFT JOIN MAGNITUDE AS b ON ( a.mg_id = b.mg_id) "
                                    "WHERE a.CO_CODE={0} and a.emc_id={1} "
                                    "AND a.emco_year={2} ORDER BY ADM_CODE "
                                    "ASC".format(self.country_code,emc_id2,self.emco_year+year2)))
            values2= list(map( lambda x: [x[0],none_emptytr(x[1])],values2 ))
        else:
            values2=info2
        if values2:
            column_operation_result=list(map(operation,values1,values2))
        else:
            column_operation_result=values1
        return column_operation_result

    
        
 
    def compute_percentages(self,indexes_dict,highest_and_lowest=True, On100=True):
        """Generic function for computing percentages of columns and computing
        the maximum and minimum if necessary.

        The keys of indexes dict has to be the AC code of the
        indicator to compute, the value should be a list with two
        pairs that go in the column operation function.        
        """
        values_dict={}
        maximum_dict={}
        minimum_dict={}
        max_min_dict = {}
        for indicator_AC in indexes_dict.keys():
            lista1=indexes_dict[indicator_AC][0]
            lista2=indexes_dict[indicator_AC][1]
            if On100:
                values_dict[indicator_AC]=self.column_operation(lista1,lista2,lambda x,y: prod(div(x,y),[100,'value'])  )
            else:
                values_dict[indicator_AC]=self.column_operation(lista1,lista2,lambda x,y: div(x,y))
            
        self.write_indic_sql(values_dict)
        
        if highest_and_lowest:
            for indicator_AC in indexes_dict.keys():
                max_values = max_sp(values_dict[indicator_AC])
                min_values = min_sp(values_dict[indicator_AC])
                maximum_dict[indicator_AC]=max_values
                minimum_dict[indicator_AC]=min_values
                max_min_dict[indicator_AC] = div(max_values, min_values)
                self.write_indic_sql_no_regions(indicator_AC + ".Max",maximum_dict[indicator_AC])
                self.write_indic_sql_no_regions(indicator_AC + ".Min",minimum_dict[indicator_AC])
                self.write_indic_sql_no_regions(indicator_AC + ".Max.Min",max_min_dict[indicator_AC])

                
    def pupils_teachers_ratio(self):
        """ Computes the PTRHC indicators."""
        variables_dict={ "PTRHC.1" : [["E.1",0],["T.1",0]],
                         "PTRHC.2.GPV": [["E.2.GPV",0],["T.2.GPV",0]],
                         "PTRHC.3.GPV": [["E.3.GPV",0],["T.3.GPV",0]],

                         "PTRHC.1.Pu" : [["E.1.Pu",0],["T.1.Pu",0]],
                         "PTRHC.2.GPV.Pu": [["E.2.GPV.Pu",0],["T.2.GPV.Pu",0]],
                         "PTRHC.3.GPV.Pu": [["E.3.GPV.Pu",0],["T.3.GPV.Pu",0]],

                         "PTRHC.1.Pr" : [["E.1.Pr",0],["T.1.Pr",0]],
                         "PTRHC.2.GPV.Pr": [["E.2.GPV.Pr",0],["T.2.GPV.Pr",0]],
                         "PTRHC.3.GPV.Pr": [["E.3.GPV.Pr",0],["T.3.GPV.Pr",0]]                         
        }
        self.compute_percentages(variables_dict,True, False)
        ## Now we add the 2t3 undicators. It could not be done with
        ## the dictionary at the beginning because there is no ISCED23
        ## information for Pupils.
        values_dict={}
        maximum_dict={}
        minimum_dict={}
        ## PTRHC.2t3.GPV
        indicator_base="PTRHC.2t3.GPV"
        for suffix in ['','.Pu','.Pr']:
            numerator_list1=self.column_operation(["E.2.GPV" + suffix ,0])
            numerator_list2=self.column_operation(["E.3.GPV" + suffix ,0])
            numerator_list=list( map(lambda x,y: sum(x,y),numerator_list1,numerator_list2))
            denominator_list=self.column_operation(["T.2t3.GPV" + suffix ,0])
            values=list(map( lambda x,y: div(x,y), numerator_list,denominator_list))
            values_dict[indicator_base + suffix]=values
            amax = max_sp(values)
            amin = min_sp(values)
            self.write_indic_sql_no_regions(indicator_base + suffix + ".Max",amax)
            self.write_indic_sql_no_regions(indicator_base + suffix + ".Min",amin)
            self.write_indic_sql_no_regions(indicator_base + suffix + ".Max.Min",div(amax,amin))
        self.write_indic_sql(values_dict)
            

        

    def newly_recruited_teachers(self):
        """Computes the NTP indicators."""
        variables_dict={"NTP.1" : [["NT.1",0],["T.1",0]],
                        "NTP.2.GPV":[["NT.2.GPV",0],["T.2.GPV",0]],
                        "NTP.3.GPV" : [["NT.3.GPV",0],["T.3.GPV",0]],
                        "NTP.2t3.GPV" : [["NT.2t3.GPV",0],["T.2t3.GPV",0]],

                        "NTP.1.Pu" : [["NT.1.Pu",0],["T.1.Pu",0]],
                        "NTP.2.GPV.Pu":[["NT.2.GPV.Pu",0],["T.2.GPV.Pu",0]],
                        "NTP.3.GPV.Pu" : [["NT.3.GPV.Pu",0],["T.3.GPV.Pu",0]],
                        "NTP.2t3.GPV.Pu" : [["NT.2t3.GPV.Pu",0],["T.2t3.GPV.Pu",0]],

                        "NTP.1.Pr" : [["NT.1.Pr",0],["T.1.Pr",0]],
                        "NTP.2.GPV.Pr":[["NT.2.GPV.Pr",0],["T.2.GPV.Pr",0]],
                        "NTP.3.GPV.Pr" : [["NT.3.GPV.Pr",0],["T.3.GPV.Pr",0]],
                        "NTP.2t3.GPV.Pr" : [["NT.2t3.GPV.Pr",0],["T.2t3.GPV.Pr",0]]
        }
        
        self.compute_percentages(variables_dict)

    def teachers_percentage_female(self):
        """Computes FTP indicators."""
        variables_dict={ "FTP.1":[["T.1.F",0],["T.1",0]],
                         "FTP.2.GPV":[["T.2.GPV.F",0],["T.2.GPV",0]],
                         "FTP.3.GPV" : [["T.3.GPV.F",0],["T.3.GPV",0]],
                         "FTP.2t3.GPV" : [["T.2t3.GPV.F",0],["T.2t3.GPV",0]],
                         
                         "FTP.1.Pu":[["T.1.Pu.F",0],["T.1.Pu",0]],
                         "FTP.2.GPV.Pu":[["T.2.GPV.Pu.F",0],["T.2.GPV.Pu",0]],
                         "FTP.3.GPV.Pu" : [["T.3.GPV.Pu.F",0],["T.3.GPV.Pu",0]],
                         "FTP.2t3.GPV.Pu" : [["T.2t3.GPV.Pu.F",0],["T.2t3.GPV.Pu",0]],

                         "FTP.1.Pr":[["T.1.Pr.F",0],["T.1.Pr",0]],
                         "FTP.2.GPV.Pr":[["T.2.GPV.Pr.F",0],["T.2.GPV.Pr",0]],
                         "FTP.3.GPV.Pr" : [["T.3.GPV.Pr.F",0],["T.3.GPV.Pr",0]],
                         "FTP.2t3.GPV.Pr" : [["T.2t3.GPV.Pr.F",0],["T.2t3.GPV.Pr",0]]
                         }
        
        self.compute_percentages(variables_dict)

    def percentage_trained_teachers(self):
        """Computes TRTP indicators. """
        variables_dict1={"TRTP.1": [["T.1.trained",0 ],["T.1",0] ],
                         "TRTP.2.GPV": [["T.2.GPV.trained",0 ],["T.2.GPV",0]],
                         "TRTP.3.GPV" : [["T.3.GPV.trained",0],["T.3.GPV",0]],
                         "TRTP.2t3.GPV": [["T.2t3.GPV.trained",0 ],["T.2t3.GPV",0] ],

                         "TRTP.1.Pu": [["T.1.Pu.trained",0 ],["T.1.Pu",0] ],
                         "TRTP.2.GPV.Pu": [["T.2.GPV.Pu.trained",0 ],["T.2.GPV.Pu",0]],
                         "TRTP.3.GPV.Pu" : [["T.3.GPV.Pu.trained",0],["T.3.GPV.Pu",0]],
                         "TRTP.2t3.GPV.Pu": [["T.2t3.GPV.Pu.trained",0 ],["T.2t3.GPV.Pu",0] ],

                         "TRTP.1.Pr": [["T.1.Pr.trained",0 ],["T.1.Pr",0] ],
                         "TRTP.2.GPV.Pr": [["T.2.GPV.Pr.trained",0 ],["T.2.GPV.Pr",0]],
                         "TRTP.3.GPV.Pr" : [["T.3.GPV.Pr.trained",0],["T.3.GPV.Pr",0]],
                         "TRTP.2t3.GPV.Pr": [["T.2t3.GPV.Pr.trained",0 ],["T.2t3.GPV.Pr",0] ]                         
        }
        variables_dict2={"TrNTP.1": [["NT.1.trained",0],["NT.1",0]],
                         "TrNTP.2.GPV":[["NT.2.GPV.trained",0],["NT.2.GPV",0]],
                         "TrNTP.3.GPV":[["NT.3.GPV.trained",0],["NT.3.GPV",0]],
                         "TrNTP.2t3.GPV": [["NT.2t3.GPV.trained",0],["NT.2t3.GPV",0]],

                         "TrNTP.1.Pu": [["NT.1.Pu.trained",0],["NT.1.Pu",0]],
                         "TrNTP.2.GPV.Pu":[["NT.2.GPV.Pu.trained",0],["NT.2.GPV.Pu",0]],
                         "TrNTP.3.GPV.Pu":[["NT.3.GPV.Pu.trained",0],["NT.3.GPV.Pu",0]],
                         "TrNTP.2t3.GPV.Pu": [["NT.2t3.GPV.Pu.trained",0],["NT.2t3.GPV.Pu",0]],

                         "TrNTP.1.Pr": [["NT.1.Pr.trained",0],["NT.1.Pr",0]],
                         "TrNTP.2.GPV.Pr":[["NT.2.GPV.Pr.trained",0],["NT.2.GPV.Pr",0]],
                         "TrNTP.3.GPV.Pr":[["NT.3.GPV.Pr.trained",0],["NT.3.GPV.Pr",0]],
                         "TrNTP.2t3.GPV.Pr": [["NT.2t3.GPV.Pr.trained",0],["NT.2t3.GPV.Pr",0]]

        }
        self.compute_percentages(variables_dict1)
        self.compute_percentages(variables_dict2)

    def percentage_private_teachers(self):
        """Computes PrTP indicators. """
        variables_dict={"PrTP.1":[["T.1.Pr",0],["T.1",0]],
                        "PrTP.2.GPV":[["T.2.GPV.Pr",0],["T.2.GPV",0]],
                        "PrTP.3.GPV":[["T.3.GPV.Pr",0],["T.3.GPV",0]],
                        "PrTP.2t3.GPV": [["T.2t3.GPV.Pr",0],["T.2t3.GPV",0]], }
        self.compute_percentages(variables_dict)

    def percentage_non_permanent_teachers(self):
        """Computes FixTP indicators."""
        variables_dict_private={"FixTP.1.Pr":[["T.1.Pr.Fix",0],["T.1.Pr",0]],
                                "FixTP.2.GPV.Pr": [["T.2.GPV.Pr.Fix",0],["T.2.GPV.Pr",0]],
                                "FixTP.3.GPV.Pr": [["T.3.GPV.Pr.Fix",0],["T.3.GPV.Pr",0]],
                                "FixTP.2t3.GPV.Pr" : [ ["T.2t3.GPV.Pr.Fix",0],["T.2t3.GPV.Pr",0] ]
                            }
                                    
        variables_dict_public={"FixTP.1.Pu":[["T.1.Pu.Fix",0],["T.1.Pu",0]],
                               "FixTP.2.GPV.Pu": [["T.2.GPV.Pu.Fix",0],["T.2.GPV.Pu",0]],
                               "FixTP.3.GPV.Pu": [["T.3.GPV.Pu.Fix",0],["T.3.GPV.Pu",0]],
                               "FixTP.2t3.GPV.Pu" : [ ["T.2t3.GPV.Pu.Fix",0],["T.2t3.GPV.Pu",0] ]
                           }
        
        self.compute_percentages(variables_dict_public,False)
        self.compute_percentages(variables_dict_private,False)
                                    
        ## Now we compute the one that includes both private and public
        priv_and_pu_dict={}
        for keys in [["FixTP.1.Pr","FixTP.1.Pu" ],["FixTP.2.GPV.Pr","FixTP.2.GPV.Pu"],["FixTP.3.GPV.Pr","FixTP.3.GPV.Pu"],["FixTP.2t3.GPV.Pr","FixTP.2t3.GPV.Pu"]]:
            numerator=self.column_operation(variables_dict_private[keys[0]][0],variables_dict_public[keys[1]][0],sum  )
            denominator=self.column_operation(variables_dict_private[keys[0]][1],variables_dict_public[keys[1]][1],sum  )
            values=list(map(lambda x,y: prod(div(x,y),[100,'value']),numerator,denominator))
            indicator=keys[0]
            indicator=indicator.replace(".Pr",'')
            priv_and_pu_dict[indicator]=values
        self.write_indic_sql(priv_and_pu_dict)

    def percentage_permanent_teachers(self):
        """Computes PermTP indicators."""
        variables_dict_private={"PermTP.1.Pr":[["T.1.Pr.Perm",0],["T.1.Pr",0]],
                                "PermTP.2.GPV.Pr": [["T.2.GPV.Pr.Perm",0],["T.2.GPV.Pr",0]],
                                "PermTP.3.GPV.Pr": [["T.3.GPV.Pr.Perm",0],["T.3.GPV.Pr",0]],
                                "PermTP.2t3.GPV.Pr" : [ ["T.2t3.GPV.Pr.Perm",0],["T.2t3.GPV.Pr",0] ]
                            }
                                    
        variables_dict_public={"PermTP.1.Pu":[["T.1.Pu.Perm",0],["T.1.Pu",0]],
                               "PermTP.2.GPV.Pu": [["T.2.GPV.Pu.Perm",0],["T.2.GPV.Pu",0]],
                               "PermTP.3.GPV.Pu": [["T.3.GPV.Pu.Perm",0],["T.3.GPV.Pu",0]],
                               "PermTP.2t3.GPV.Pu" : [ ["T.2t3.GPV.Pu.Perm",0],["T.2t3.GPV.Pu",0] ]
                           }
        
        self.compute_percentages(variables_dict_public,False)
        self.compute_percentages(variables_dict_private,False)
                                    
        ## Now we compute the one that includes both private and public
        priv_and_pu_dict={}
        for keys in [["PermTP.1.Pr","PermTP.1.Pu" ],["PermTP.2.GPV.Pr","PermTP.2.GPV.Pu"],["PermTP.3.GPV.Pr","PermTP.3.GPV.Pu"],["PermTP.2t3.GPV.Pr","PermTP.2t3.GPV.Pu"]]:
            numerator=self.column_operation(variables_dict_private[keys[0]][0],variables_dict_public[keys[1]][0],sum  )
            denominator=self.column_operation(variables_dict_private[keys[0]][1],variables_dict_public[keys[1]][1],sum  )
            values=list(map(lambda x,y: prod(div(x,y),[100,'value']),numerator,denominator))
            indicator=keys[0]
            indicator=indicator.replace(".Pr",'')
            priv_and_pu_dict[indicator]=values
        self.write_indic_sql(priv_and_pu_dict)
        
    def attrition_rate(self):
        """Copmutes TAttrR indicators."""
        ind_dict={}
        indicator_name_base="TAttrR"        
        for indicator_suffix in [".1",".2.GPV",".3.GPV",".2t3.GPV"]:
            number_of_teachers_previous_year=self.column_operation(["T" + indicator_suffix,-1])
            if not number_of_teachers_previous_year:
                number_of_teachers_previous_year=self.column_operation(["T" + indicator_suffix + ".m1",0])
            newly_recruited_teachers=self.column_operation(["NT" + indicator_suffix,0 ])
            number_of_teachers_current_year=self.column_operation(["T" + indicator_suffix,0])            
            ind_dict[indicator_name_base + indicator_suffix]=list ( map ( lambda x,y,z: prod( div( neg( sum(x,y) , z) , x) ,[100,'value']),
                                                                          number_of_teachers_previous_year,
                                                                          newly_recruited_teachers,
                                                                          number_of_teachers_current_year) )
        self.write_indic_sql(ind_dict)
        ## print(ind_dict)


    def mean_category(self, codes, midpoints, ac_pop, DivBySum = False):
        """ Calculates a generic mean by category given the category and a list of indicators

        Returns the mean category by ADM.
        If DivBySum = True is divides by the sum of the category, otherwise by ac_pop.
        length of AC codes an midpoints should be the same.
        """
        if len(midpoints)!=len(codes):
            print("Length of midpoints doesn't equal length of codes!")
            return
        if DivBySum:
            denom = list(map(lambda u: self.column_operation([u,0], [u,0], lambda x,y:x),codes))
            denom = reduce(lambda x,y: op2col(x,y,sum), denom)
            temp = list(map(lambda x,z: self.column_operation([x,0], [x, 0], lambda u,v: prod(u, z)),codes, midpoints))        
        else:   
            temp = list(map(lambda z,v: self.column_operation([z,0], [ac_pop, 0], lambda x,y: prod(div(x,y), v)),codes, midpoints))
        temp =  list(map(list, zip(*temp)))
        temp = list(map(lambda l: reduce(lambda x,y: sum(x,y), l), temp))
        if DivBySum: temp = op2col(temp, denom, div)
        return(temp)

    def mean_age_level(self,level):
        """ 
        Given a level in ['T.1', 'T.2.GPV', 'T.3.GPV', 'T.2t3.GPV'], returns mean age (MAge) for total, public and private.

        Return is a dictionary format, with indicator names as key of the dictionary.
        The average is calculated by using the midpoint ages 
        defined in the midpoint variable below in a ascending order. 
        """
        if level not in ['T.1', 'T.2.GPV', 'T.3.GPV', 'T.2t3.GPV']:
            print("The only levels allowed are ['T.1', 'T.2.GPV', 'T.3.GPV', 'T.2t3.GPV']")
            return
        midpoints = [[20,'value'], [24.5,'value'], [34.5,'value'], [44.5,'value'],[54.5,'value'], [60,'value']]
        levelsExt = ['x.Ag20m','x.Ag20t29','x.Ag30t39','x.Ag40t49','x.Ag50t59','x.Ag60p']
        typeSchool  = ['', '.Pu', '.Pr']
        MAge = {}
        for t in typeSchool:
            name = 'MAge' + level + t
            ac = level + t
            codes = list(map(lambda x: x.replace('x', ac), levelsExt))
            MAge.update({name:self.mean_category(codes,midpoints, ac, DivBySum=True)})
        return MAge
        
    def mean_exp_level(self, level):
        """ 
        Given a level in ['T.1', 'T.2.GPV', 'T.3.GPV', 'T.2t3.GPV'], returns mean expireince (MExp) for total, public and private.

        Return is a dictionary format, with indicator names as key of the dictionary.
        The average is calculated by using the midpoint ages 
        defined in the midpoint variable below in a ascending order. 
        """
        if level not in ['T.1', 'T.2.GPV', 'T.3.GPV', 'T.2t3.GPV']:
            print("The only levels allowed are ['T.1', 'T.2.GPV', 'T.3.GPV', 'T.2t3.GPV']")
            return

        midpoints = [[0.5,'value'],[1.5,'value'], [4,'value'], [8,'value'], [13,'value'],[17,'value']] ## midpoint years of experience for each level.
        levelsExt = ['Nz','z.Exp1t2', 'z.Exp3t5','z.Exp6t10', 'z.Exp11t15', 'z.Exp15p']
        typeSchool  = ['', '.Pu', '.Pr']
        MExp = {}
        for t in typeSchool:
            name = 'MExp' + level + t
            ac = level + t      
            codes = list(map(lambda x: x.replace('z', level+t), levelsExt))
            MExp.update({name:self.mean_category(codes,midpoints, ac, DivBySum=True)})
        return MExp

    def mean_level(self, levelFun,ret= False):
        """
        Calculates the mean of age/exp/... for the following levels ['T.1', 'T.2.GPV', 'T.3.GPV', 'T.2t3.GPV'],by passing levelFun(indic, level) as in mean_age_level or mean_exp_level. 
        
        """
        isced = ['T.1', 'T.2.GPV', 'T.3.GPV', 'T.2t3.GPV']       
        if ret:
            M = {}
            for s in isced:
                M.update({s: levelFun(s)})
            return M
        else:
            for s in isced:
                self.write_indic_sql(levelFun(s))

    def percentage_teachers_attainment(self):
        """ ComputesEA2mPT, EA3PT, EA4PT, EA5pPT, EAukPT indicators."""
        isced = ['T.1', 'T.2.GPV', 'T.3.GPV', 'T.2t3.GPV']
        suffix1 = ['', '.Pu', '.Pr']
        temp = {"EA2mPX": ['X.EA.2m'], "EA3PX": ['X.EA.3'],
                "EA4PX": ['X.EA.4'],"EAukPX": ['X.EA.uk']}
        dict_i = {}
        for s in suffix1:   
            for i in isced:
                l = i+s
                for key, value in temp.items():
                    key1 = key.replace('X', l)
                    dict_i.update({key1:[[value[0].replace('X', l),0 ],[l,0]]})
                ## Writing 5p indicator
                l5p = op2col(self.column_operation([l + '.EA.5', 0], [l + '.EA.6',0], lambda x, y: sum(x, y)),
                             self.column_operation([l + '.EA.7', 0], [l + '.EA.8',0], lambda x, y: sum(x, y)), sum)
                #denom = self.column_operation(l5p, [l,0],div )
                denom = self.column_operation(l5p,[l,0],lambda x,y: prod(div(x,y),[100,'value'])  )
                self.write_indic_sql({'EA5pP'+  l :denom})
        self.compute_percentages(dict_i, False)

    def percentage_teachers_exp(self):
        """ Computes Exp1t2, Exp3t5, Exp6t10, Exp11t15, Exp15p, Expuk indicators. """
        isced = ['T.1', 'T.2.GPV', 'T.3.GPV', 'T.2t3.GPV']
        suffix1 = ['', '.Pu', '.Pr']
        temp = {"Exp1t2PY": ['Y.Exp1t2'], "Exp3t5PY": ['Y.Exp3t5'],
                "Exp6t10PY": ['Y.Exp6t10'],"Exp11t15PY": ['Y.Exp11t15'],
                "Exp15pPY":['Y.Exp15p'], "ExpukPY":['Y.Expuk']}
        dict_i = {}
        
        for s in suffix1:   
            for i in isced:
                l = i+s
                for key, value in temp.items():
                    key1 = key.replace('Y', l)
                    dict_i.update({key1:[[value[0].replace('Y', l),0 ],[l,0]]})
        self.compute_percentages(dict_i, False)

    def percentage_teachers_age(self):
        """Computes Ag20mPT, Ag20t29PT, Ag30t39PT, Ag40t49PT, Ag50t59PT, Ag60pPT, AgukPT indicators."""
        isced = ['T.1', 'T.2.GPV', 'T.3.GPV', 'T.2t3.GPV']
        suffix1 = ['', '.Pu', '.Pr']
        temp ={"Ag20mPY":['Y.Ag20m'],"Ag20t29PY":['Y.Ag20t29'],
               "Ag30t39PY":['Y.Ag30t39'],"Ag40t49PY":['Y.Ag40t49'],
               "Ag50t59PY":['Y.Ag50t59'],"Ag60pPY":['Y.Ag60p'], "AgukPY":['Y.Aguk']}
        dict_i = {}
        for s in suffix1:   
            for i in isced:
                l = i+s
                for key, value in temp.items():
                    key1 = key.replace('Y', l)
                    dict_i.update({key1:[[value[0].replace('Y', l),0 ],[l,0]]})
        self.compute_percentages(dict_i, False)

    def dissimilarity_index_single(self,AC , AC_year=0, benchAC='Pop.Ag0t99', bench_year=0):
        """ Calculates the dissimilarity index between AC and a benchmark AC.

        Using the formula 0.5*SUM_adm|AC_adm/AC_national - benchAC_adm/bench_national|, 
        where adm = administrative divisions.
        year should be 0 for current year or -1 for previous one.
        """
        if(type(benchAC)==list):
            benchSum = reduce(lambda x,y: self.column_operation(x, y, sum),list(map(lambda x: [x,bench_year],benchAC)))
        else:
            benchSum = [benchAC, bench_year]
                    
        if(type(AC)==dict):
            for key, value in AC.items():
                IndicName = 'DInd' + key
                AC1 = list(map(lambda x: [x,AC_year],value))
                value1= reduce(lambda x,y: self.column_operation(x, y, sum), AC1)
                value = self.column_operation(benchSum,value1,lambda x,y:[x,y])
        else:
            value = self.column_operation(benchSum,[AC,AC_year],lambda x,y:[x,y])
            IndicName = 'DInd' + AC
        national = value[0]
        value = value[1:]
        disInd = list(map(lambda x: neg(div(x[0],national[0]),div(x[1],national[1])),value))
        disInd = list(map(lambda x: [abs(x[0]),x[1]] if x[1]=='value' else x, disInd))
        disInd = prod(reduce(sum, disInd), [0.5, 'value'])
    
        self.write_indic_sql_no_regions(IndicName, disInd)

    def dissimilarity_index(self):
        """ Lists all to be computed dissimilarity indices by ISCED level, and computes them."""
        
        tb1 = ['T.1', 'T.1.F', {'T.1.Ag50p':['T.1.Ag50t59','T.1.Ag60p']},'NT.1',
               'T.1.trained', 'NT.1.trained', 'T.1.EA.2m',
               {'T.1.EA.3p':['T.1.EA.3','T.1.EA.4','T.1.EA.5','T.1.EA.6','T.1.EA.7','T.1.EA.8' ]},
               {'T.1.Exp2m':['NT.1','T.1.Exp1t2']},
               {'T.1.Exp10p':['T.1.Exp11t15', 'T.1.Exp15p']},
               'T.1.Pr', {'T.1.Fix' : ['T.1.Pr.Fix', 'T.1.Pu.Fix']}]

        list(map(lambda x: self.dissimilarity_index_single(x, benchAC = 'E.1'), tb1))
        self.dissimilarity_index_single('T.1.Pr.Fix', benchAC = 'E.1.Pr')
        self.dissimilarity_index_single('T.1.Pu.Fix', benchAC = 'E.1.Pu')
        tb2 = ['T.2.GPV', 'T.2.GPV.F',
               {'T.2.GPV.Ag50p':['T.2.GPV.Ag50t59', 'T.2.GPV.Ag60p']},'NT.2.GPV',
               'T.2.GPV.trained', 'NT.2.GPV.trained',
               {'T.2.GPV.EA.3m':['T.2.GPV.EA.2m', 'T.2.GPV.EA.3']},
               {'T.2.GPV.EA.4p':['T.2.GPV.EA.4','T.2.GPV.EA.5','T.2.GPV.EA.6','T.2.GPV.EA.7','T.2.GPV.EA.8' ]},
               {'T.2.GPV.Exp2m':['NT.2.GPV','T.2.GPV.Exp1t2']},
               {'T.2.GPV.Exp10p':['T.2.GPV.Exp11t15', 'T.2.GPV.Exp15p']},
               'T.2.GPV.Pr',{'T.2.GPV.Fix':['T.2.GPV.Pr.Fix', 'T.2.GPV.Pu.Fix']}]

        list(map(lambda x: self.dissimilarity_index_single(x, benchAC = 'E.2.GPV'), tb2))
        self.dissimilarity_index_single('T.2.GPV.Pr.Fix', benchAC = 'E.2.GPV.Pr')
        self.dissimilarity_index_single('T.2.GPV.Pu.Fix', benchAC = 'E.2.GPV.Pu')
        tb3 = ['T.3.GPV', 'T.3.GPV.F',
              {'T.3.GPV.Ag50p':['T.3.GPV.Ag50t59', 'T.3.GPV.Ag60p']},'NT.3.GPV',
               'T.3.GPV.trained', 'NT.3.GPV.trained',
               {'T.3.GPV.EA.4m':['T.3.GPV.EA.2m', 'T.3.GPV.EA.3', 'T.3.GPV.EA.4']},
               {'T.3.GPV.EA.5p':['T.3.GPV.EA.5','T.3.GPV.EA.6','T.3.GPV.EA.7','T.3.GPV.EA.8' ]},
               {'T.3.GPV.Exp2m':['NT.3.GPV','T.3.GPV.Exp1t2']},
               {'T.3.GPV.Exp10p':['T.3.GPV.Exp11t15', 'T.3.GPV.Exp15p']},
               'T.3.GPV.Pr',{'T.3.GPV.Fix':['T.3.GPV.Pr.Fix', 'T.3.GPV.Pu.Fix']}]

        list(map(lambda x: self.dissimilarity_index_single(x, benchAC = 'E.3.GPV'), tb3))
        self.dissimilarity_index_single('T.3.GPV.Pr.Fix', benchAC = 'E.3.GPV.Pr')
        self.dissimilarity_index_single('T.3.GPV.Pu.Fix', benchAC = 'E.3.GPV.Pu')
        
        tb23 = ['T.2t3.GPV', 'T.2t3.GPV.F',
                {'T.2t3.GPV.Ag50p':['T.2t3.GPV.Ag50t59', 'T.2t3.GPV.Ag60p']},
                'NT.2t3.GPV','T.2t3.GPV.Math', 'T.2t3.GPV.Read',
                'T.2t3.GPV.trained', 'NT.2t3.GPV.trained',
                {'T.2t3.GPV.EA.4m':['T.2t3.GPV.EA.2m', 'T.2t3.GPV.EA.3', 'T.2t3.GPV.EA.4']},
                {'T.2t3.GPV.EA.5p':['T.2t3.GPV.EA.5','T.2t3.GPV.EA.6','T.2t3.GPV.EA.7','T.2t3.GPV.EA.8' ]},
                {'T.2t3.GPV.Exp2m':['NT.2t3.GPV','T.2t3.GPV.Exp1t2']},
                {'T.2t3.GPV.Exp10p':['T.2t3.GPV.Exp11t15', 'T.2t3.GPV.Exp15p']},
                'T.2t3.GPV.Pr',{'T.2t3.GPV.Fix':['T.2t3.GPV.Pr.Fix', 'T.2t3.GPV.Pu.Fix']},
                'T.2t3.GPV.Pr.Fix', 'T.2t3.GPV.Pu.Fix']
        list(map(lambda x: self.dissimilarity_index_single(x, benchAC = ['E.2.GPV','E.3.GPV']), tb23))
        self.dissimilarity_index_single('T.2t3.GPV.Pr.Fix', benchAC = ['E.2.GPV.Pr','E.3.GPV.Pr'])
        self.dissimilarity_index_single('T.2t3.GPV.Pu.Fix', benchAC = ['E.2.GPV.Pu','E.3.GPV.Pu'])
        

    def audit_trail(self,temp_table = True):
        """ Records the changes of indicators in the INDICATORS_AUDIT_TRAIL SQL table."""
        if(temp_table):
            self.write_sql("DELETE FROM METER_AUDIT_TEMP")
            self.write_sql(("INSERT INTO METER_AUDIT_TEMP "
                            "(MC_ID, CO_CODE, ADM_CODE, MC_YEAR, EM_FIG_OLD, MQ_ID_OLD, MG_ID_OLD, USER_NAME, SERIES) "
                            "SELECT IND_ID, CO_CODE, ADM_CODE, IND_YEAR, FIG, QUAL, MAGN, '{2}', 'EST' "
                            "from EDU_INDICATOR_EST "
                            "WHERE CO_CODE = {0} and IND_YEAR = {1}".format(self.country_code,self.emco_year, self.username)))
        else:
            self.write_sql(("INSERT INTO INDICATOR_AUDIT_TRAIL " 
                            "(IND_ID, CO_CODE, ADM_CODE, IND_YEAR, FIG_OLD, QUAL_OLD, "
                            "MAGN_OLD, USER_NAME, SERIES,FIG_NEW, QUAL_NEW, MAGN_NEW) " 
                            "SELECT a.MC_ID, a.CO_CODE, a.ADM_CODE, a.MC_YEAR, " 
                            "a.EM_FIG_OLD, a.MQ_ID_OLD, a.MG_ID_OLD, " 
                            "a.USER_NAME, a.SERIES, b.FIG, b.QUAL, b.MAGN "
                            "from  METER_AUDIT_TEMP as a "
                            "join EDU_INDICATOR_EST as b on a.MC_ID = b.IND_ID "
                            "and a.CO_CODE = b.CO_CODE and a.ADM_CODE = b.ADM_CODE "
                            "and a.MC_YEAR = b.IND_YEAR AND "
                            "(a.EM_FIG_OLD !=b.FIG OR a.MQ_ID_OLD != b.QUAL OR a.MG_ID_OLD != b.MAGN)"))
            self.write_sql("DELETE FROM METER_AUDIT_TEMP")

    def check_est_values(self):
        """ Checks if any values exist in the Est series before computing indicators."""
        values = self.read_sql(("SELECT * FROM EDU_METER97_EST WHERE CO_CODE={} "
                                "AND EMCO_YEAR={}".format(self.country_code,self.emco_year)))
        return(True if values else False)

    def compute_all_indicators(self):
        """ Excute functions to calculate indicators."""
        ### Moving data to Audit Temp
        
        self.audit_trail()
        ##### Calculating indicators
        self.pupils_teachers_ratio()
        self.newly_recruited_teachers()
        self.teachers_percentage_female()
        self.percentage_trained_teachers()
        self.percentage_private_teachers()
        self.percentage_non_permanent_teachers()
        self.percentage_permanent_teachers()
        self.attrition_rate()
        self.percentage_teachers_attainment()
        self.percentage_teachers_exp()
        self.percentage_teachers_age()
        self.mean_level(self.mean_exp_level)
        self.mean_level(self.mean_age_level)
        self.dissimilarity_index()
        ## Moving changed values to Audut trail
        self.audit_trail(False)
   
    def __init__ (self,database_file,emco_year,country_name, username):
        self.set_database_connection(database_file)
        self.emco_year=emco_year
        self.country_name=country_name
        self.get_country_code()
        self.username = username

