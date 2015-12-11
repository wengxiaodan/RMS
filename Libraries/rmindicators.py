import sqlite3,re
import sys, getpass, os, csv
import csv

##################################################
#### table Algebra for sum/div/prod operations
##################################################

## Default algebra tables
algebra_sum = {'a': {'a': 'a', 'm': 'm', 'n': 'n','x':'x', '':''},
               'm': {'a': 'm', 'm': 'm', 'n': 'm','x':'m', '':'m'},
               'n': {'a': 'n', 'm': 'm', 'n': 'n','x':'x', '':''},
               'x': {'a': 'x', 'm': 'm', 'n': 'x','x':'x', '': 'x' }, 
               '': {'a': '', 'm': 'm', 'n' :'','x':'x', '':''}}
algebra_prod = algebra_sum
algebra_div  = algebra_sum

def read_algebra():
    """  Read an algebra table from a csv file and convert to a dictionary
    """
    # Reading sum algebra
    algfiles = ['sum.csv', 'prod.csv','div.csv']
    algop = ['Sum', 'Prod', 'Div']
    if os.path.isfile(algfiles[0]):
        data = csv.DictReader(open(algfiles[0]))
        global algebra_sum
        algebra_sum  = arrange_algebra_dist(data,algop[0])
    if os.path.isfile(algfiles[1]):
        data = csv.DictReader(open(algfiles[1]))
        global algebra_prod
        algebra_sum  = arrange_algebra_dist(data,algop[1])
    if os.path.isfile(algfiles[2]):
        data = csv.DictReader(open(algfiles[2]))
        global algebra_div
        algebra_sum  = arrange_algebra_dist(data,algop[2])


def arrange_algebra_dist(data, op= 'Sum'):
    """ Arranging algebra from a csv file read in data based os an operation (op) in a dictionary as seen in the global variables.
        The left corner of the table in the csv file should be the op, case sensitive
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

def sum_list(x):
    """ Sums a single list recursively """
    if len(x)==2:
        return(sum(x[0], x[1]))
    else:
       return(sum_list(x[2:]+[sum(x[0],x[1])]))
        
        
def sum(x,y):
    """ 
    Sums two tuppels x = (fig, mg_symbol), y = (fig, mg_symbol). 
    Returns a tupple (fig, symbol), where symbol is the result of the multiplication tables, fig is '' is symbol is n, m ,a or x.

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
    if algeb =='':
        return([(x[0] or 0 ) + (y[0] or 0),''])
    return(['',algeb])

def prod(x,y):
    """ 
    Product of two tuppels x = (fig, mg_symbol), y = (fig, mg_symbol). 
    Returns a tupple (fig, symbol), where symbol is the result of the multiplication tables, fig is '' is symbol is n, m ,a or x.

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
    if algeb =='':
        return([(x[0] or 0)*(y[0] or 0),''])
    return(['',algeb])

def div(x,y):
    """ 
    Division of two tuppels x = (fig, mg_symbol), y = (fig, mg_symbol). 
    Returns a tupple (fig, symbol), where symbol is the result of the multiplication tables, fig is '' is symbol is n, m ,a or x.
    
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
    if algeb =='':
        return([(x[0] or 0)/(y[0] or 0),''])
    return(['',algeb])

def op2col(col1, col2, op):
    """ Returns the op(sum/div/prod) of two columns"""
    return  list(map(lambda x,y: op(x, y), col1, col2))
##################################################

##################################################
#### Highest level of EdAttain
##################################################
def highestEA_list(level, indic, offset=0):
    """ Returns the ratio of the highest level of EdAttain given the level
        offset is the year, 0 for current year assigned by indic, -1 is N-1 year
        indic an instance of indicator class"""
    ac_pop = 'Pop.Ag0t99'
    if len(level) ==1:
        a = indic.column_operation([level[0], offset], [ac_pop,offset], lambda x,y: div(x,y)) 
    else:    
        b = list(map(lambda x: indic.column_operation([x, offset], [ac_pop,offset], lambda x,y: div(x,y)), level))
        a = reduce(lambda x,y: op2col(x, y, sum), b)
    return(a)

def highestEA(schoolLevel,  indic, offset=0):
    """ 
    Returns a dictionary of the indicator EA(x)PT.(y).(z), where
    x is 2m, 3, 4, or 5p as the attainment levels
    y is the parameter schoolLevel defined by ['1', '2.GPV', '3.GPV', '23.GPV']
    z is ['', '.Pu', '.Pr']
    
    The key of the dictionary is the indicator name EA(x)PT.(y).(z) and the value is
    a list of calculated figures for each region. 
    
    indic is an instance of indicator class,
    offset is the year offset, 0 as current year defined in indicator class indic, and -1, is the N-1 year.
    """
    if schoolLevel not in ['1', '2.GPV', '3.GPV', '23.GPV']:
        print("The only schoolLevel allowed is ['1', '2.GPV', '3.GPV', '23.GPV'] ")
        return
    
    dic_level = {'2m':['T.x.EA.2m'] , '3':['T.x.EA.3'], '4': ['T.x.EA.4'], '5p':['T.x.EA.5', 'T.x.EA.6','T.x.EA.7','T.x.EA.8'], 'uk':['T.x.EA.uk'] }
    typeSchool  = ['', '.Pu', '.Pr']
    EA_dic = {}
    for key, value in dic_level.items():
        for t in typeSchool:
            name = 'EA' + key + 'PT.' + s + t
            level_list = list(map(lambda x: x.replace('x', s+t), dic_level[key]))
            EA_dic.update({name:highestEA_list(level_list, indic, offset)})
    return EA_dic

##################################################
##################################################

def EA_all(indic, offset=0):
    """
    Calculates the highest EdAttain for for levels  ['1', '2.GPV', '3.GPV', '23.GPV']
    returns a dictionary of dictionaries. The first level is of size 4, as for each level
    and the second levels is a dictionary creates by highestEA_list  as:
    
    A dictionary of the indicator EA(x)PT.(y).(z), where
    x is 2m, 3, 4, or 5p as the attainment levels
    y is the parameter schoolLevel defined by ['1', '2.GPV', '3.GPV', '23.GPV']
    z is ['', '.Pu', '.Pr']
    
    The key of the dictionary is the indicator name EA(x)PT.(y).(z) and the value is
    a list of calculated figures for each region. 
    """
    ea = {} 
    isced = ['1', '2.GPV', '3.GPV', '23.GPV']
    for s in isced:
        ea.update({s : highestEA(s,  indic, offset) })
    return(ea)    


def mean_age(indic, codes):
    """ Calculates the mean age for a given list of codes"""
    midpoint = [[20,''], [24,''], [34,''], [44,''],[54,''], [65,'']]
    ac_pop = 'Pop.Ag0t99'
    temp = list(map(lambda z,v: indic.column_operation([z,0], [ac_pop, 0], lambda x,y:   prod(div(x,y), v)),codes, midpoint))
    temp = list(map(sum_list, temp))
    return(temp)


def inverse_mg_id(x):
    if type(x) in [int,float]:
        return('')
    elif x==3:
        return('X')
    elif x==6:
        return('A')
    elif x=="D":
        return("m")

def none_emptytr(x):
    if x==None:
       return('')
    else:
        return(x)

def fix_ac_code_symbol(x):
    y=x
    y[1]=none_emptytr(y[1])
    return (y)

class indicators():
    def get_nadm1(self):
        """Gets the number of regions"""
        cursor=self.conn.cursor()
        cursor.execute("select count(ADM_CODE) from regions where co_code={} and ADM_CODE>0".format(self.country_code))
        nadm1=cursor.fetchone()
        
    def set_database_connection(self,database_file):
        """Sets the connection to the database"""
        self.conn=sqlite3.connect(database_file)
        
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
        cursor=self.conn.cursor()
        #The following is not working so I am using .format, but this is not secure
#        cursor.execute(u'SELECT CO_CODE FROM COUNTRY  WHERE UPPER(CO_LONG_NAME) IS ?', (name,) )
        cursor.execute("SELECT CO_CODE FROM COUNTRY  WHERE UPPER(CO_LONG_NAME) IS {0};".format(name) )
        country_code=cursor.fetchone()
        if(country_code==None):
            self.country_code=0
        else:
            self.country_code=country_code[0]
        cursor.close()

        
    def column_operation(self,info1,info2,operation):
        """Perform column operations given ACs and year.
        
        This function returns a vector with an operation applied to
        two columns. infoi is a vector [ACi,yeari], where ACi is an
        alphanumeric code and year is the year for which that
        alphanumeric code is going to be computed. operation is a
        function that receives two arguments. This is the operation
        that is going to be applied element by element to both colums.
        The years should be zero or -1.
        """
        AC1=info1[0]
        year1=info1[1]
        AC2=info2[0]
        year2=info2[1]
        cursor=self.conn.cursor()
        cursor.execute("SELECT EMC_ID FROM RM_Mapping WHERE AC='{0}' AND CUR_YEAR={1} LIMIT 1".format(AC1,year1))
        emc_id1=cursor.fetchone()[0]
        cursor.execute("SELECT EMC_ID FROM RM_Mapping WHERE AC='{0}' AND CUR_YEAR={1} LIMIT 1".format(AC2,year2))
        emc_id2=cursor.fetchone()[0]
        #cursor.execute("select EM_FIG,MG_ID from EDU_METER97_REP where CO_CODE={} and emc_id={} and emco_year={}".format(self.country_code,emc_id1,self.emco_year+year1))
        cursor.execute("select a.EM_FIG,b.SYMBOL from EDU_METER97_REP AS a LEFT JOIN MAGNITUDE AS b ON ( a.mg_id = b.mg_id) WHERE a.CO_CODE={} and a.emc_id={} AND a.emco_year={}".format(self.country_code,emc_id1,self.emco_year+year1));
        values1=cursor.fetchall()  #list(map(lambda x: x[0],cursor.fetchall() ))
        values1= list(map( lambda x: [x[0],none_emptytr(x[1])],values1 ))
        #values1=list(map(lambda x: aux(x[0]),values1 ))
        #cursor.execute("select EM_FIG,MG_ID from EDU_METER97_REP where CO_CODE={} and emc_id={} and emco_year={}".format(self.country_code,emc_id2,self.emco_year+year2))
        cursor.execute("select a.EM_FIG,b.SYMBOL from EDU_METER97_REP AS a LEFT JOIN MAGNITUDE AS b ON ( a.mg_id = b.mg_id) WHERE a.CO_CODE={} and a.emc_id={} AND a.emco_year={}".format(self.country_code,emc_id2,self.emco_year+year2));
        values2=cursor.fetchall() #list(map(lambda x: x[0],cursor.fetchall() ))
        values2= list(map( lambda x: [x[0],none_emptytr(x[1])],values2 ))
        #values2=list(map(lambda x: aux(x[0]),values2 ))
        column_operation_result=list(map(operation,values1,values2))
        cursor.close()
        return column_operation_result
        
        
    def indicator_number_of_teachers():
        cursor=self.conn.cursor()
        cursor.execute("SELECT EMC_ID FROM RM_Mapping WHERE AC='T.1' AND CUR_YEAR=0")
        
    def __init__ (self,database_file,emco_year,country_name):
        self.set_database_connection(database_file)
        self.emco_year=emco_year
        self.country_name=country_name
        self.get_country_code()
